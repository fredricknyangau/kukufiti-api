# app/modules/finance/mpesa_client.py
import base64
import hashlib
import logging
from datetime import datetime
from decimal import Decimal

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class MpesaClient:
    """
    Safaricom Daraja API client.

    Two responsibilities only:
    1. Get an OAuth access token
    2. Initiate an STK push

    Everything else (saving to DB, handling callbacks) is done
    by the service and repository layers.
    """

    def __init__(self):
        self._consumer_key = settings.mpesa_consumer_key
        self._consumer_secret = settings.mpesa_consumer_secret
        self._shortcode = settings.mpesa_shortcode
        self._passkey = settings.mpesa_passkey
        self._callback_url = settings.mpesa_callback_url
        self._base_url = settings.mpesa_base_url

    # ── OAUTH TOKEN ────────────────────────────────────────────────────

    async def get_access_token(self) -> str:
        """
        Gets a fresh OAuth token from Daraja.

        WHY base64: Daraja uses HTTP Basic Auth for OAuth.
        Basic Auth requires: base64("consumer_key:consumer_secret")
        sent as: Authorization: Basic <encoded_string>
        """
        credentials = f"{self._consumer_key}:{self._consumer_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self._base_url}/oauth/v1/generate",
                params={"grant_type": "client_credentials"},
                headers={"Authorization": f"Basic {encoded}"},
                timeout=10.0,
            )

        if response.status_code != 200:
            logger.error(
                "M-Pesa OAuth failed",
                extra={
                    "status_code": response.status_code,
                    "response": response.text,
                },
            )
            raise MpesaAuthError(
                f"Failed to get access token: {response.status_code}"
            )

        data = response.json()
        token = data.get("access_token")

        if not token:
            raise MpesaAuthError("Access token missing from Daraja response")

        logger.info("M-Pesa OAuth token obtained successfully")
        return token

    # ── PASSWORD GENERATION ─────────────────────────────────────────────

    def _generate_password(self) -> tuple[str, str]:
        """
        Generates the Daraja API password and timestamp.

        WHY this formula:
        Daraja requires: base64(shortcode + passkey + timestamp)
        The timestamp must match the password — both sent in the request.

        Returns: (password, timestamp)
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        raw = f"{self._shortcode}{self._passkey}{timestamp}"
        password = base64.b64encode(raw.encode()).decode()
        return password, timestamp

    # ── PHONE NORMALISATION ─────────────────────────────────────────────

    def _normalise_phone(self, phone: str) -> str:
        """
        Normalises phone number to 254XXXXXXXXX format.

        Daraja rejects:
        - 07XXXXXXXX  (local format)
        - +2547XXXXXXX (with plus sign)
        - 2547XXXXXXX  (already correct — keep as is)

        Examples:
        0712345678  → 254712345678
        +254712345678 → 254712345678
        254712345678  → 254712345678
        """
        phone = phone.strip().replace(" ", "").replace("-", "")

        if phone.startswith("+"):
            phone = phone[1:]
        elif phone.startswith("0"):
            phone = f"254{phone[1:]}"

        return phone

    # ── STK PUSH ────────────────────────────────────────────────────────

    async def initiate_stk_push(
        self,
        phone_number: str,
        amount: Decimal,
        account_reference: str,
        transaction_desc: str,
    ) -> dict:
        """
        Initiates an STK (SIM Toolkit) Push.

        What happens:
        1. We send this request to Daraja
        2. Daraja sends a PIN prompt to the customer's phone
        3. Customer enters their M-Pesa PIN
        4. Daraja processes the payment
        5. Daraja POSTs the result to our callback_url
        6. We update our database in the callback handler

        Returns the Daraja response containing CheckoutRequestID
        which we use to track this specific STK push.
        """
        token = await self.get_access_token()
        password, timestamp = self._generate_password()
        phone = self._normalise_phone(phone_number)

        # Daraja requires integer amounts (no decimals)
        amount_int = int(amount)
        if amount_int < 1:
            raise MpesaValidationError("M-Pesa minimum transaction is KES 1")

        # Account reference: max 12 characters
        # Transaction desc: max 13 characters
        ref = account_reference[:12]
        desc = transaction_desc[:13]

        payload = {
            "BusinessShortCode": self._shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount_int,
            "PartyA": phone,            # customer phone
            "PartyB": self._shortcode,  # your shortcode (receives the money)
            "PhoneNumber": phone,       # phone to send STK push to
            "CallBackURL": self._callback_url,
            "AccountReference": ref,
            "TransactionDesc": desc,
        }

        logger.info(
            "Initiating M-Pesa STK push",
            extra={
                "phone": f"+254***{phone[-4:]}",  # masked for logs
                "amount_kes": amount_int,
                "account_reference": ref,
            },
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}/mpesa/stkpush/v1/processrequest",
                json=payload,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                timeout=30.0,
            )

        data = response.json()

        # Daraja returns 200 for accepted requests
        # but some errors also return 200 with an errorCode field
        if response.status_code != 200 or "errorCode" in data:
            error_msg = data.get("errorMessage", data.get("ResponseDescription", "Unknown error"))
            logger.error(
                "M-Pesa STK push failed",
                extra={"status_code": response.status_code, "response": data},
            )
            raise MpesaRequestError(error_msg)

        logger.info(
            "M-Pesa STK push accepted",
            extra={"checkout_request_id": data.get("CheckoutRequestID")},
        )

        return data


# ── INTERNAL CLIENT EXCEPTIONS ────────────────────────────────────────────
# These are low-level exceptions raised inside MpesaClient only.
# They are NOT HTTP-mapped — FinanceService catches them and re-raises
# MpesaInitiationError (from finance/exceptions.py) which the global
# handler in main.py converts to an HTTP 502 response.

class MpesaError(Exception):
    """Base for all internal M-Pesa client errors.
    Catch this in FinanceService to handle any Daraja failure uniformly.
    """

class MpesaAuthError(MpesaError):
    """OAuth token acquisition from Daraja failed.
    Raised by get_access_token() on non-200 status or missing token field.
    """

class MpesaRequestError(MpesaError):
    """Daraja rejected the STK push request.
    Raised by initiate_stk_push() on non-200 response or errorCode in body.
    """

class MpesaValidationError(MpesaError):
    """Input failed local validation before calling Daraja.
    Raised by initiate_stk_push() when amount < 1 KES.
    """
