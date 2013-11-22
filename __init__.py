"""
Here we get to define a public API people can use when they `import usginmodels`
"""
import re

from exceptions import *
from model_cache import ModelCache
cache = ModelCache()
cache.refresh()


def get_models():
    """Return a List of ContentModel objects"""
    return cache.models


def get_uri(uri):
    """Return a single model or version given a URI"""

    # Check the URI to determine whether or not we're looking for a version or a model. If there are numbers in the
    # last portion of the URI then that is a version URI
    find_version = False
    uri_components = uri.split('/')
    last = uri_components.pop()
    if not re.match("\d", last):
        uri_components.append(last)
        find_version = True

    # Find Models that match the URI given
    uri = "/".join(uri_components)
    model_matches = [m for m in cache.models if m.uri == uri]

    # If there are no matches, raise an exception
    if len(model_matches) == 0:
        raise InvalidUri(uri)

    # If there are more than one model, we'll just take the first one
    model = model_matches[0]

    # If the original URI was not for a version, just return the model
    if not find_version:
        return model

    # If we can get a version from the model that we already have, return it
    if model.is_version_valid(last):
        return model.get_version(last)
    else:
        raise InvalidUri("/".join([uri, last]))


def validate_file(uri, csv_file):
    """Return boolean and validation errors"""
    model_or_version = get_uri(uri)
    return model_or_version.validate_file(csv_file)


def refresh():
    cache.refresh()