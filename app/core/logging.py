# Structured JSON logging configuration for kukufiti-api.
#
# WHY structlog on top of stdlib logging?
# ---------------------------------------
# Python's stdlib logging module emits plain-text lines by default:
#     2024-01-01 10:00:00 - app.batches - INFO - Created batch xyz
# That works fine for humans reading a terminal but is hard to query in
# log aggregators (Cloud Logging, Datadog, Loki) where each field must
# be a discrete JSON key.
#
# structlog transforms every log call into a structured event dict that
# passes through a *processor pipeline* before being rendered. The final
# processor emits a JSON line:
#     {"event": "Created batch xyz", "logger": "app.batches",
#      "level": "info", "timestamp": "2024-01-01T10:00:00Z"}
#
# HOW the two layers interact:
# structlog is configured with `logger_factory=LoggerFactory()` so it
# delegates the actual I/O to the stdlib logging system. This means:
#   - stdlib handlers (StreamHandler, file handlers) control where output goes.
#   - structlog processors control *format* (adding timestamps, levels, etc.).
#   - Third-party libraries that use stdlib logging automatically get the
#     same level filtering, so their noisy DEBUG lines are suppressed by
#     the same log_level setting.

import logging

import structlog


def configure_logging(log_level: str = "INFO") -> None:
    """Set up stdlib + structlog for structured JSON output.

    Must be called once at application startup (in the lifespan function in
    app/main.py) before any log lines are emitted, so that the processor
    chain is active for the entire lifetime of the process.

    The function is idempotent: calling it multiple times with the same
    level has no side effects, though doing so is wasteful and should be
    avoided.

    Args:
        log_level: Case-insensitive logging threshold. Messages below this
                   level are dropped by the stdlib basicConfig handler before
                   they even reach structlog processors. Accepted values:
                   DEBUG, INFO, WARNING, ERROR, CRITICAL.
                   Sourced from settings.log_level (app/core/config.py).
    """
    # getattr converts the string "INFO" → logging.INFO (= 20).
    # Falls back to logging.INFO if an unrecognised string is passed,
    # so a typo in the env var does not silence all logging.
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Configure the stdlib root logger. Every logger in the process
    # (including third-party libraries) inherits this level and handler
    # unless they explicitly override it.
    logging.basicConfig(
        level=numeric_level,
        # The format string here is only used by the stdlib handler for log
        # records that bypass structlog (e.g. uvicorn's internal access log).
        # structlog-originated records are rendered by JSONRenderer below and
        # arrive at the handler as a pre-formatted JSON string.
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Configure the structlog processor pipeline.
    # Each processor is a callable(logger, method_name, event_dict) → event_dict.
    # They are applied left-to-right; the last processor must return a string.
    structlog.configure(
        processors=[
            # Drop log records whose level is below the configured threshold.
            # This must run first so cheap filtering happens before expensive
            # processors like JSON serialisation.
            structlog.stdlib.filter_by_level,

            # Inject the Python logger name (e.g. "app.modules.batches.service")
            # into the event dict as the "logger" key. Useful for correlating a
            # log line back to the exact module that emitted it.
            structlog.stdlib.add_logger_name,

            # Inject the log level string ("info", "warning", etc.) as "level".
            structlog.stdlib.add_log_level,

            # Expand positional format arguments: log.info("Batch %s created", id)
            # → event_dict["event"] = "Batch abc-123 created".
            # Prefer keyword arguments in new code for clarity, but this keeps
            # old-style % formatting working transparently.
            structlog.stdlib.PositionalArgumentsFormatter(),

            # Inject an ISO-8601 UTC timestamp as "timestamp".
            # Consistent timestamps make cross-service log correlation possible
            # without relying on the log aggregator's ingestion time.
            structlog.processors.TimeStamper(fmt="iso"),

            # If `stack_info=True` is passed to a log call, this processor
            # captures the current Python stack and attaches it to the event
            # dict so it appears in the JSON output alongside the message.
            structlog.processors.StackInfoRenderer(),

            # If an exception is being handled (sys.exc_info() is non-empty),
            # this serialises the traceback into the event dict so the full
            # stack trace appears in the structured JSON output rather than
            # being printed to stderr by the default exception hook.
            structlog.processors.ExceptionRenderer(),

            # Decode bytes values in the event dict to Unicode strings.
            # Prevents JSON serialisation from failing on byte fields returned
            # by asyncpg or other C-extension libraries.
            structlog.processors.UnicodeDecoder(),

            # Final processor: serialise the entire event dict to a JSON string.
            # The resulting string is passed to the stdlib logging handler as the
            # log record's message, which then writes it to stdout/stderr.
            structlog.processors.JSONRenderer(),
        ],
        # Use a plain dict as the thread-local context carrier.
        # In async code (FastAPI / asyncio) this means context is per-call-stack,
        # not per-request — use structlog.contextvars for request-scoped context.
        context_class=dict,
        # Delegate I/O to the stdlib logging system configured above.
        logger_factory=structlog.stdlib.LoggerFactory(),
        # Cache the bound logger after the first log call so the processor
        # chain is not re-evaluated on every subsequent log statement from
        # the same logger object. Safe to enable once configure_logging is
        # called once at startup and not called again.
        cache_logger_on_first_use=True,
    )
