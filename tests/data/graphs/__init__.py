from importlib.resources import files
from pathlib import Path
import sys
from typing import cast

from rdflib import Graph


graph_data: Path = cast(Path, files("tests.data.graphs"))


def generate_graph_objects() -> None:
    """Iterates over the data/graphs dir, parses files into Graph objects and exposes them in the module."""
    for rdf_file in graph_data.rglob("*.ttl"):
        setattr(sys.modules[__name__], rdf_file.stem, Graph().parse(rdf_file))


generate_graph_objects()
