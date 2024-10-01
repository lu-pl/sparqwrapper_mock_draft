from collections.abc import Iterator


def _get_bindings_from_bindings_dict(bindings_dict: dict) -> Iterator[dict]:
    """Get a simple binding/unification mapping from a SPARQLWrapper bindings dict."""
    bindings = map(
        lambda binding: {k: v["value"] for k, v in binding.items()},
        bindings_dict["results"]["bindings"],
    )
    return bindings
