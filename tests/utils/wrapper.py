"""Base SPARQLWrapper instance for testing."""

from SPARQLWrapper import SPARQLWrapper


dne_endpoint: str = "htpps://some.nonexistent.endpoint"
sparql_wrapper: SPARQLWrapper = SPARQLWrapper(endpoint=dne_endpoint)
