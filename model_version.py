from datetime import datetime
from dateutil import parser as date_parser


class ModelVersion():

    version = ""
    uri = ""
    xsd_url = ""
    xls_url = ""
    date_created = datetime(1900, 1, 1)
    layers = []

    def __init__(self, version_dict):
        self.version = version_dict.get("version", "")
        self.uri = version_dict.get("uri", "")
        self.xsd_url = version_dict.get("xsd_file_path", "")
        self.xls_url = version_dict.get("xls_file_path", "")
        self.date_created = date_parser(version_dict.get("date_created", self.date_created.isoformat()))
        self.layers = []

    def validate_file(self, csv_file):
        pass
