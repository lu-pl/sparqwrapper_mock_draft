from collections.abc import Iterable
from contextlib import contextmanager
import json
from unittest.mock import patch

from SPARQLWrapper import SPARQLWrapper
from rdflib import Graph
from rdflib.plugins.sparql.processor import SPARQLResult


def _bindings_to_response_json(bindings: Iterable[dict]) -> str:
    bindings_list: list[dict] = [
        {k: {"value": v}} for binding in bindings for k, v in binding.items()
    ]

    return json.dumps({"results": {"bindings": bindings_list}})


def graph_query_result_to_json_response(sparql_result: SPARQLResult) -> str:
    result_rows: Iterable[dict] = map(
        lambda x: {str(k): str(v) for k, v in x.items()}, sparql_result._genbindings
    )
    json_response = _bindings_to_response_json(result_rows)
    return json_response


data = """
BASE <http://example.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rel: <http://www.perceive.net/schemas/relationship/>

<#green-goblin>
  rel:enemyOf <#spiderman> ;
  a foaf:Person ;    # in the context of the Marvel universe
  foaf:name "Green Goblin" .

<#spiderman>
  rel:enemyOf <#green-goblin> ;
  a foaf:Person ;
  foaf:name "Spiderman" .
"""

graph = Graph().parse(data=data, format="ttl")


def code_under_test():
    s = SPARQLWrapper("https://some.endpoint")
    s.setQuery("select * where {?s ?p ?o .}")

    result = s.query()
    return result


# https://github.com/RDFLib/sparqlwrapper/blob/2a6e2d3ddbc3fe38ca47d6d05f23c9b61ff82366/SPARQLWrapper/Wrapper.py#L667
def update_query_p(query_string: str) -> bool:
    return False


@contextmanager
def sparqlwrapper_graph_target(graph: Graph):
    with (
        patch.object(SPARQLWrapper, "setQuery") as mock_setQuery,
        patch.object(SPARQLWrapper, "query") as mock_query,
    ):

        def mock_query_side_effect():
            if mock_setQuery.call_args is None:
                raise Exception(
                    "SPARQLWrapper.setQuery out of scope.\n"
                    "Code under test must exhibit a local or enclosing call to SPARQLWrapper.setQuery."
                )

            query_string = mock_setQuery.call_args[0][0]
            graph_query_method: str = (
                "update" if update_query_p(query_string) else "query"
            )
            sparql_result: SPARQLResult = getattr(graph, graph_query_method)(
                query_string
            )
            return graph_query_result_to_json_response(sparql_result)

        mock_query.side_effect = mock_query_side_effect
        yield


with sparqlwrapper_graph_target(graph):
    result = code_under_test()
    print("INFO: ", result)
