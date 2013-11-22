# contentmodels

A library defining an API for working with [USGIN Content Models](http://schemas.usgin.org/models) in Python.

## Usage

Start by importing the module

```python
import usginmodels
```

This exposes four important functions:

### usginmodels.refresh

Checks http://schemas.usgin.org/contentmodels.json for the most up-to-date description of available content models

Example Usage:

```python
usginmodels.refresh()
```

### usginmodels.get_models

Returns a list of [ContentModel](#contentmodels) objects that represent the models available from USGIN. See below
for a description of the capabilities of [ContentModel](#contentmodels) objects.

Example Usage:

```python
models = usginmodels.get_models
```

### usginmodels.get_uri

You pass in a URI as a string, you get back a [ContentModel](#contentmodel) or [ModelVersion](#modelversion) object.
If your URI is invalid, an [InvalidUri](#invaliduri) exception will be thrown.

Example Usage:

```python
active_faults = usginmodels.get_uri(
    "http://schemas.usgin.org/uri-gin/ngds/dataschema/activefault/"
)
active_fault_1_1 = usginmodels.get_uri(
    "http://schemas.usgin.org/uri-gin/ngds/dataschema/activefault/1.1"
)
```

### usginmodels.validate_file

You pass in a URI as a string, and a **file-like object** that represents a CSV file.

Example Usage:

```python
my_csv = open("/path/to/csv/file", "r")
valid, errors = usginmodels.validate_file(
    "http://schemas.usgin.org/uri-gin/ngds/dataschema/activefault/",
    my_csv
)

if valid:
    print "Hurrah!"
else:
    print errors
```