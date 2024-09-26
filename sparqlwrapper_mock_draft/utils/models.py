from rdflib import Literal, URIRef

from pydantic import BaseModel, ConfigDict


class VarsModel(BaseModel):
    vars: list[str]


class TripleModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    s: URIRef
    p: URIRef
    o: URIRef | Literal


class BindingsModel(BaseModel):
    bindings: list[TripleModel]


class QueryResultModel(BaseModel):
    head: VarsModel
    results: BindingsModel
