"""Utils for SPARQLWrapper mocking experiments."""

import re
from typing import NamedTuple
import urllib.parse
from urllib.request import Request

from rdflib.plugins.sparql.evaluate import ParseException
from rdflib.plugins.sparql.parser import parseQuery


class QueryData(NamedTuple):
    query: str
    format: str
    is_update: bool


def _unquote_query(quoted_query: str) -> str:
    """Unquote a quoted query extracted from a URL."""
    _unquoted_query = urllib.parse.unquote(quoted_query)
    query = _unquoted_query.replace("+", " ")
    return query


def _get_parameter_from_str(url, parameter: str) -> str:
    """Get a parameter from a URL."""
    value: str = re.findall(rf"{parameter}=(.+?)(&|$)", url)[0][0]
    return _unquote_query(value)


def _get_query_from_url(url: str) -> str:
    return _get_parameter_from_url(url, parameter="query")


def _get_format_from_url(url: str) -> str:
    return _get_parameter_from_str(url, parameter="format")


def _get_query_from_request_data(request: Request) -> str:
    _data: str = request.data.decode("utf-8")
    query: str = _get_parameter_from_str(_data, "update")
    return query


def _get_format_from_request_data(request: Request) -> str:
    return "json"


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


def _get_query_data_from_url(url: str) -> QueryData:
    query = _get_query_from_url(url)
    format = _get_format_from_url(url)

    return QueryData(query=query, format=format, is_update=False)


def _get_query_data_from_request(request: Request) -> QueryData:
    query = _get_query_from_request_data(request)
    format = _get_format_from_request_data(request)

    return QueryData(query=query, format=format, is_update=True)


def get_query_data(obj: str | Request) -> QueryData:
    match obj:
        case str():
            query_data = _get_query_data_from_url(obj)
        case Request():
            query_data = _get_query_data_from_request(obj)
        case _:
            raise Exception(
                "Argument obj must be either a string or a urllib.request.Request object."
            )

    return query_data
