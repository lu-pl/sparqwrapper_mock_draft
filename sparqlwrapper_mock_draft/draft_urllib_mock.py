"""Playground for mocking urllib instead of SPARQLWrapper."""

from contextlib import contextmanager
from unittest.mock import MagicMock, patch

from SPARQLWrapper import Wrapper
from SPARQLWrapper import SPARQLWrapper
from rdflib import Graph
from rdflib.plugins.sparql.processor import SPARQLResult

from sparqlwrapper_mock_draft.utils.utils import (
    get_query_from_url,
    sparql_result_to_json_payload,
    update_query_p,
)


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


@contextmanager
def sparqlwrapper_graph_target(graph: Graph):
    with patch.object(Wrapper, "urlopener") as mock_open:
        mock_response = MagicMock()

        def mock_side_effect():
            """Extract a query from a URL, run it against a local rdflib.Graph instance and return a response JSON payload."""
            _url: str = mock_open.call_args[0][0].full_url
            query: str = get_query_from_url(_url)

            graph_query_method: str = "update" if update_query_p(query) else "query"
            sparql_result: SPARQLResult = getattr(graph, graph_query_method)(query)

            json_payload = sparql_result_to_json_payload(sparql_result=sparql_result)
            return json_payload

        mock_response.read.side_effect = mock_side_effect
        mock_open.return_value = mock_response

        yield graph


with sparqlwrapper_graph_target(graph):
    result = code_under_test()
    print("INFO: ", result)
    print("INFO: ", result.convert())
