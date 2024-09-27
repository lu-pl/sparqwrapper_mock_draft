"""Playground for mocking urllib instead of SPARQLWrapper."""

from contextlib import contextmanager
from typing import cast
from unittest.mock import MagicMock, patch

from SPARQLWrapper import Wrapper
from rdflib import Graph
from rdflib.plugins.sparql.processor import SPARQLResult
from sparqlwrapper_mock_draft.utils.utils import (
    get_format_from_url,
    get_query_from_url,
    is_update_query,
)


@contextmanager
def sparqlwrapper_graph_target(graph: Graph):
    """Context for mocking SPARQLWrapper by routing queries to a local rdflib.Graph."""

    with patch.object(Wrapper, "urlopener") as mock_open:
        mock_response = MagicMock()

        def mock_side_effect():
            """Side effect encapsulation for mocking HTTPResponse.read.

            Extract a query from a URL, run it against a local rdflib.Graph instance
            and return the applicable payload.
            """
            _url: str = mock_open.call_args[0][0].full_url
            query: str = cast(str, get_query_from_url(_url))
            _format: str = cast(str, get_format_from_url(_url))

            graph_query_method: str = "update" if is_update_query(query) else "query"
            sparql_result: SPARQLResult = getattr(graph, graph_query_method)(query)

            payload = sparql_result.serialize(format=_format)
            return payload

        mock_response.read.side_effect = mock_side_effect
        mock_open.return_value = mock_response

        yield graph
