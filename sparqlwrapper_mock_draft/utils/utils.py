"""Utils for SPARQLWrapper mocking experiments."""

import re
import urllib.parse

from rdflib.plugins.sparql.evaluate import ParseException
from rdflib.plugins.sparql.parser import parseQuery


def _unquote_query(quoted_query: str) -> str:
    """Unquote a quoted query extracted from a URL."""
    _unquoted_query = urllib.parse.unquote(quoted_query)
    query = _unquoted_query.replace("+", " ")
    return query


def _get_parameter_from_url[T](url, parameter: str, default: T = None) -> str | T:
    """Get a parameter from a URL."""
    try:
        value: str = re.findall(rf"{parameter}=(.+?)(&|$)", url)[0][0]
        return _unquote_query(value)
    except IndexError:
        return default


def get_query_from_url[T](url: str, default: T = None) -> str | T:
    return _get_parameter_from_url(url, parameter="query", default=default)


def get_format_from_url[T](url: str, default: T = None) -> str | T:
    return _get_parameter_from_url(url, parameter="format", default=default)


def is_update_query(query: str) -> bool:
    """Check if a query string is an update query.

    The function tries to parse a query, if a ParseException is raised
    because a SELECT, CONSTRUCT, DESCRIBE or ASK query was expected,
    the is_update_query predicate is considered True.

    If a ParseException for another reason (e.g. invalid query syntax) is raised,
    the ParseException is re-raised.
    """
    try:
        parseQuery(query)
    except ParseException as e:
        expected_query_msg = (
            "Expected {SelectQuery | ConstructQuery | DescribeQuery | AskQuery}"
        )

        if e.msg == expected_query_msg:
            return True
        else:
            raise e
    else:
        return False
