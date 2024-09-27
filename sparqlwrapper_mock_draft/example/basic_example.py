"""Basic example for sparqlwrapper_graph_target."""

from SPARQLWrapper import SPARQLWrapper
from rdflib import Graph
from sparqlwrapper_mock_draft.draft_urllib_mock import sparqlwrapper_graph_target

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
    s = SPARQLWrapper("https://some.inexistent.endpoint")
    s.setQuery("select * where {?s ?p ?o .}")

    result = s.query()
    return result


with sparqlwrapper_graph_target(graph):
    result = code_under_test()
    print("INFO: ", result)
    print()
    print("INFO: ", result.convert())
