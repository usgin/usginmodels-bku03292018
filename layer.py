from field import Field

class Layer():

    layer_name = ""
    fields = []

    def __init__(self, layer, fields_dict):
        self.layer_name = layer
        self.fields = [Field(f) for f in fields_dict]


    def validate_file(self, csv_file):
        errors = []
        valid = True

        # Create the object for the corrected data and don't include the first field (OBJECTID) or last field (Shape)
        dataCorrected = []
        dataCorrected.append([f.field_name for f in self.fields[1:][:-1]])

        # Check if the number of fields in the csv in the same as the number of fields in the schema
        # (minus 2 for the OBJECTID and Shape fields which those are not in the csv)
        if self.fields.__len__()-2 != len(csv_file.fieldnames):
            errors.append("Error! The imported CSV does not have the correct number of fields. Check the schema.")

        primary_uri_field = get_primary_uri_field(self.fields[1:][:-1])
        print "Primary URI field: " + primary_uri_field.field_name

        for i, row in enumerate(csv_file):
            rowCorrected = []
            for f in self.fields[1:][:-1]:

                # Check required fields. Immediately return when a required field is not found.
                try:
                    data = row[f.field_name]
                except:
                    if f.field_optional == False:
                        errors.append("Error! " + f.field_name + " is a required field but was not found in the imported csv file.")
                    return False, errors, dataCorrected

                # Check encoding of data
                encoding_error = check_encoding(data)
                errors = addError(i, encoding_error, errors)

                if not encoding_error:
                    # Check data types
                    type_error, data = f.validate_field(data)
                    # type_error, data = check_field_type(data, f)
                    errors = addError(i, type_error, errors)

                rowCorrected.append(data)
            dataCorrected.append(rowCorrected)

        return valid, errors, dataCorrected

def get_primary_uri_field(fields):
    """Find the first field name containing URI"""

    for f in fields:
        if "URI" in f.field_name:
            return f

    return None

def check_encoding(data):
    """Check that conversion to utf-8 and Win-1252 encoding (used by the server) is possible"""
    msg = None

    try:
        data = data.encode("utf-8")
        data = data.encode("windows-1252")
    except:
        msg = "Encoding Error! Found an unrecognized character in " + data + "."

    return msg

def addError(i, error, errors):
    """ Add error message to the list of errors and set the validity"""

    if error:
        if "Error" in error:
            valid = False
        errors.append("Row " + str(i+1) + " " + error)
    return errors