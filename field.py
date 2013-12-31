import datetime
import dateutil.parser as parser

class Field():

    field_name = ""
    field_type = ""
    field_description = ""
    field_optional = bool()

    def __init__(self, field):
        self.field_name = field.get("name", "")
        self.field_type = field.get("type", "")
        self.field_description = field.get("description", "")
        self.field_optional = field.get("optional", "")

    def validate_field(self, data):
        """Check that the data matches the required type: string, double or dateTime"""
        msg = None

        # String type
        if self.field_type == "string":
            try:
                data = str(data)
            except:
                if self.field_optional == False:
                    msg = "Error! Type should be string. Changing " + data + " to Missing"
                else:
                    msg = "Warning! " + self.field_name + " not recognized as a string. Deleting " + data
                    data = ""
            if data == "" and self.field_optional == False:
                data = "Missing"
                msg = "Warning! " + self.field_name + " can't be blank. Changing to Missing"

        # Double type
        elif self.field_type == "double":
            if data != "":
                try:
                    data = float(data)
                except:
                    if self.field_optional == False:
                        msg = "Warning! Type should be double. Changing " + str(data) + " to -9999"
                        data = -9999
                    else:
                        msg = "Warning! " + self.field_name + " not recognized as a double. Deleting " + str(data)
                        data = ""
            else:
                if self.field_optional == False:
                    data = -9999
                    msg = "Warning! " + self.field_name + " can't be blank. Changing to -9999"

        # DateTime type
        elif self.field_type == "dateTime":
            if data != "":
                try:
                    data = (parser.parse(data, default=datetime.datetime(1901, 01, 01, 00, 00, 00))).isoformat()
                except:
                    if self.field_optional == False:
                        msg = "Warning! Type should be dateTime. Changing " + str(data) + " to 1901-01-01T00:00:00"
                        data = datetime.datetime(1901, 01, 01, 00, 00, 00).isoformat()
                    else:
                        msg = "Warning! " + self.field_name + " not recognized as a date. Deleting " + str(data)
                        data = ""
            else:
                if self.field_optional == False:
                    data = datetime.datetime(1901, 01, 01, 00, 00, 00).isoformat()
                    msg = "Warning! " + self.field_name + " can't be blank. Changing to " + data

        return msg, data