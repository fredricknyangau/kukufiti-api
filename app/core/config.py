# pydantic-settings bridges environment variables and Python class attributes.
# On import, it reads every field defined in Settings from the process environment
# (and optionally a .env file), validates their types, and raises a ValidationError
# at startup if any required variable is missing. This fail-fast behaviour is
# intentional: a mis-configured service should crash immediately rather than serve
# requests with broken credentials or missing URLs.
#
# Rule: Never hardcode secret values or connection strings in this file.
# All secrets must come from environment variables injected by Docker / the host.
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# The placeholder value shipped in .env.example for SECRET_KEY.
# If the running process still carries this string it means the operator never
# set a real secret — the validator below catches that and refuses to start.
# Centralising the constant here keeps the validator and any future checks
# consistent without magic string duplication.
_INSECURE_PLACEHOLDER = "change_this_to_a_real_secret_in_production"


class Settings(BaseSettings):
    # ------------------------------------------------------------------ #
    # Database — one DSN (Data Source Name / connection URL) per module.  #
    # ------------------------------------------------------------------ #
    # Each module connects to the same PostgreSQL server but authenticates
    # as a *different role* (e.g. batches_app, finance_app). Those roles
    # hold DML privileges (SELECT/INSERT/UPDATE/DELETE) only on their own
    # schema. This is schema-level isolation enforced at the database layer:
    # even if a bug in the batches module tries to query the finance schema,
    # the database will refuse the connection. The superuser URL (database_url)
    # is only used by the migration runner for DDL (CREATE TABLE, etc.).
    database_url: str       # superuser — migration runner only, never the app
    batches_db_url: str     # batches_app role → batches schema DML
    finance_db_url: str     # finance_app role → finance schema DML
    health_db_url: str      # health_app role  → health schema DML
    auth_db_url: str        # auth_app role    → auth schema DML

    # ------------------------------------------------------------------ #
    # Application metadata                                                 #
    # ------------------------------------------------------------------ #
    # These values are surfaced in the OpenAPI spec (title, version) and in
    # structured log lines so operators can grep by version when debugging
    # a specific deployment. Defaults make local dev work out of the box.
    app_name: str = "kukufiti-api"
    app_version: str = "0.1.0"
    debug: bool = False     # enables FastAPI debug mode; never True in prod
    log_level: str = "info" # case-insensitive; configure_logging uppercases it

    # ------------------------------------------------------------------ #
    # Security                                                             #
    # ------------------------------------------------------------------ #
    # secret_key signs and verifies JWTs. Its value must be random, long
    # (≥ 32 bytes of entropy), and *different in every environment*.
    # If dev and prod share a key, a token issued in dev is valid in prod —
    # a critical security flaw that is invisible at runtime.
    secret_key: str
    # How long an access token remains valid. Short-lived access tokens
    # reduce the window of exposure if a token is stolen; the refresh token
    # provides seamless renewal without re-authentication.
    access_token_expire_minutes: int = 30
    # Refresh tokens live longer so users are not forced to log in every day.
    # They must be stored securely (httpOnly cookies or encrypted storage) and
    # rotated on each use to prevent replay attacks.
    refresh_token_expire_days: int = 7

    # ------------------------------------------------------------------ #
    # M-pesa Daraja API credentials
    # ------------------------------------------------------------------ #
    mpesa_environment: str = "sandbox"
    mpesa_consumer_key: str
    mpesa_consumer_secret: str
    mpesa_shortcode: str
    mpesa_passkey: str
    mpesa_callback_url: str

    @property
    def mpesa_base_url(self) -> str:
        if self.mpesa_environment == "production":
            return "https://api.safaricom.co.ke"
        return "https://sandbox.safaricom.co.ke"

    @field_validator("secret_key")
    @classmethod
    def secret_key_must_not_be_placeholder(cls, v: str) -> str:
        """Refuse to start if SECRET_KEY is still the example placeholder.

        Threat model: if the same placeholder value is used across dev, staging,
        and production, any JWT signed in one environment is cryptographically
        valid in every other environment. An attacker who obtains a dev token
        could replay it against the production API.

        This validator fires at import time (before any request is served),
        so a mis-configured deployment fails loudly during health checks or
        container startup rather than silently serving authenticated requests
        with a known-insecure key.

        To generate a secure secret:
            python -c "import secrets; print(secrets.token_hex(32))"
        """
        if v == _INSECURE_PLACEHOLDER:
            raise ValueError(
                "SECRET_KEY is set to the insecure placeholder value. "
                "Generate a real secret with: python -c \"import secrets; print(secrets.token_hex(32))\""
            )
        return v

    model_config = SettingsConfigDict(
        # Load .env from the current working directory so developers can
        # run the app locally without exporting variables manually.
        # In production (Docker), the container environment takes precedence
        # over any .env file, so this setting is harmless in both contexts.
        env_file=".env",
        env_file_encoding="utf-8",
        # Ignore unknown env vars rather than raising a validation error.
        # This keeps the app compatible with environments that inject extra
        # platform variables (e.g. KUBERNETES_SERVICE_HOST, HOSTNAME, etc.).
        extra="ignore",
    )


# Module-level singleton: imported as `from app.core.config import settings`.
# pydantic-settings reads and validates all values at import time, so any
# missing or invalid variable raises an error before the FastAPI app is created.
settings = Settings()  # type: ignore[call-arg]
