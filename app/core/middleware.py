# HTTP middleware for kukufiti-api: correlation ID injection and request timing.
#
# CORRELATION IDs
# ---------------
# In a distributed system (API → database, API → M-Pesa, API → background jobs)
# a single user action can generate log lines across multiple services and
# multiple async tasks. Without a shared identifier, correlating those lines
# requires tedious timestamp matching.
#
# A correlation ID (also called a request ID or trace ID) is a UUID generated
# for every incoming HTTP request. The middleware:
#   1. Reads the ID from the incoming `X-Request-ID` header (if the client or
#      a load balancer provides one), or generates a fresh UUID if not.
#   2. Stores the ID in a context variable (contextvars.ContextVar) so that
#      every log statement inside that request's async execution tree can
#      include it automatically via the structlog context (see core/logging.py).
#   3. Echoes the ID back in the `X-Request-ID` response header so the client
#      and the load balancer can log the same ID for end-to-end tracing.
#
# REQUEST TIMING
# --------------
# The middleware records the wall-clock time at the start of each request and
# emits a structured log line at the end including:
#   - HTTP method and path
#   - Response status code
#   - Duration in milliseconds
#
# This gives an always-on performance baseline without needing an external APM
# agent. Long requests stand out immediately in log queries:
#   jq 'select(.duration_ms > 500)' app.log
#
# IMPLEMENTATION NOTE
# -------------------
# FastAPI middleware is registered in app/main.py with:
#   app.add_middleware(CorrelationIdMiddleware)
# Middleware runs outside route handlers, so it sees every request including
# those that result in 404 or 422 validation errors.
