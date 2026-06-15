# Shared Pydantic base model configuration for all request/response schemas.
#
# PURPOSE
# -------
# Every request and response schema in the API inherits from a base model
# that sets common Pydantic configuration. Defining it once here instead of
# repeating `model_config = ConfigDict(...)` on every schema class prevents
# drift: if the shared config needs to change (e.g. to enable camelCase
# aliases), updating this file propagates the change everywhere.
#
# PLANNED BASE CLASS (to be implemented)
# --------------------------------------
#
#   from pydantic import BaseModel, ConfigDict
#
#   class AppBaseModel(BaseModel):
#       model_config = ConfigDict(
#           # from_attributes=True enables Pydantic to construct a schema
#           # instance directly from a Python dataclass or ORM model without
#           # manually converting it to a dict first.  The router calls
#           # BatchResponse.model_validate(batch) where `batch` is a
#           # dataclass from models.py; from_attributes makes that work.
#           from_attributes=True,
#
#           # populate_by_name=True allows both the field name and any
#           # alias to be used when constructing the model.  Without this,
#           # only the alias works when alias_generator or field aliases
#           # are in use.
#           populate_by_name=True,
#
#           # Uncomment to serve camelCase JSON to frontend clients while
#           # keeping Python identifiers in snake_case:
#           # alias_generator=to_camel,
#       )
#
# CURRENTLY
# ---------
# AppBaseModel is defined directly in app/modules/batches/schemas.py.
# When other modules (finance, health, auth) add their own schemas, that
# class should be moved here so all modules share a single definition.
#
# USAGE
# -----
# from app.shared.base_schema import AppBaseModel
#
# class CreateTransactionRequest(AppBaseModel):
#     batch_id: UUID
#     amount_kes: Decimal