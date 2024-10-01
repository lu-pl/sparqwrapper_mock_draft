# SPARQLWrapper mock draft

A draft for mocking `SPARQLWrapper` for testing purposes.


The general idea is to come up with a context where `SPARQLWrapper` query/update operations are routed to a local `rdflib.Graph` object instead of actually targeting a remote SPARQL endpoint.


The `SPARQLWrapperLocalTarget` context manager aims to implement this behavior.

In the following example, the `SPARQLWrapper` operations in`code_under_test` will be routed to the local `rdflib.Graph` instance `graph`.
The `SPARQLWrapper.QueryResult` object will have a mock `HTTPResponse` with the SPARQL result as response payload.


```python
from SPARQLWrapper import SPARQLWrapper
from rdflib import Graph
from sparqlwrapper_mock_draft.draft_urllib_mock import sparqlwrapper_graph_target

graph = Graph().parse("some_actual_rdf.ttl") 

def code_under_test():
    s = SPARQLWrapper("https://some.inexistent.endpoint")
    s.setQuery("select * where {?s ?p ?o .}")

    result = s.query()
    return result


with SPARQLWrapperLocalTarget(graph) as graph:
    result = code_under_test() 
```

Also see a [basic_example](https://github.com/lu-pl/sparqwrapper_mock_draft/blob/main/sparqlwrapper_mock_draft/example/basic_example.py) for ad hoc runable example code.


Theoretically, this should run across query types and also for update requests and for all response formats.

> Note: This is an untested draft. Do not use this code.

## Todo
Write tests.
