"""Latest attempt to come up with a generic mocking facility for SPARQLWrapper."""

from contextlib import contextmanager
from functools import partial
from http.client import HTTPResponse
from unittest.mock import MagicMock, patch

from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper.Wrapper import QueryResult
from rdflib import Graph
from rdflib.plugins.sparql.processor import SPARQLResult


class SPARQLWrapperLocalMock(SPARQLWrapper):
    def __init__(self, *args, graph, **kwargs):
        self.graph = graph
        super().__init__(*args, **kwargs)

    def query(self):
        mock_response: MagicMock = MagicMock(spec=HTTPResponse)

        result: SPARQLResult = self.graph.query(self.queryString)
        mock_response.read.return_value = result.serialize(format=self.returnFormat)

        return QueryResult(mock_response)


@contextmanager
def SPARQLWrapperLocalTarget(graph: Graph):
    with patch("__main__.SPARQLWrapper", partial(SPARQLWrapperLocalMock, graph=graph)):
        yield graph
