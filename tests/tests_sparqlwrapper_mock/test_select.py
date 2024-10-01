"""Tests for SPARQLWrapper SELECT queries."""

from sparqlwrapper_mock_draft.draft_urllib_mock import SPARQLWrapperLocalTarget
from tests.data.graphs import spiderman
from tests.utils.wrapper import sparql_wrapper


def test_base_select():
    with SPARQLWrapperLocalTarget(spiderman) as graph:
        sparql_wrapper.setQuery("select * where {?s ?p ?o .}")
        assert sparql_wrapper.query()
