"""Utils for SPARQLWrapper mocking experiments."""

import re
import urllib.parse

from rdflib.plugins.sparql.processor import SPARQLResult


def _unquote_query(quoted_query: str) -> str:
    """Unquote a quoted query extracted from a URL."""
    _unquoted_query = urllib.parse.unquote(quoted_query)
    query = _unquoted_query.replace("+", " ")
    return query


def get_query_from_url(url: str) -> str:
    """Get a SPARQL query from a URL."""
    try:
        query: str = re.findall(r"query=(.+?)&", url)[0]
    except IndexError:
        raise Exception(f"Unable to extract query from URL: {url}")
    else:
        return _unquote_query(query)


# https://github.com/RDFLib/sparqlwrapper/blob/2a6e2d3ddbc3fe38ca47d6d05f23c9b61ff82366/SPARQLWrapper/Wrapper.py#L667
def update_query_p(query_string: str) -> bool:
    return False


def sparql_result_to_json_payload(sparql_result: SPARQLResult) -> str:
    return "fake json payload"
