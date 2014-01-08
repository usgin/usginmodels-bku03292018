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

        # Check the fields in the csv against those in the schema, not including the first field (OBJECTID) or last field (Shape)
        errors = check_fields(csv_file.fieldnames, self.fields[1:][:-1])
        if errors:
            return False, errors, [], {}, ""

        used_uris = []
        primary_uri_field = get_primary_uri_field(self.fields[1:][:-1])

        temp_units = ""
        srs = ""
        long_fields = {}

        for i, row in enumerate(csv_file):
            rowCorrected = []
            for f in self.fields[1:][:-1]:

                # Check required fields. Immediately return when a required field is not found.
                try:
                    data = row[f.field_name]
                except:
                    if f.field_optional == False:
                        errors.append("Error! " + f.field_name + " is a required field but was not found in the imported file.")
                    return False, errors, [], {}, ""

                # Remove leading and trailing whitespace
                data = data.strip()

                # Check encoding of data
                encoding_error = check_encoding(data)
                valid, errors = addError(i, valid, encoding_error, errors)

                if not encoding_error:
                    # Check data types
                    type_error, data = f.validate_field(data)
                    valid, errors = addError(i,valid, type_error, errors)

                    # Check URIs
                    uri_error, data, used_uris = f.check_uri(data, primary_uri_field, used_uris)
                    valid, errors = addError(i, valid, uri_error, errors)

                    # Check temperature units
                    temp_units_error, data, temp_units = f.check_temp_units(data, temp_units)
                    valid, errors = addError(i, valid, temp_units_error, errors)

                    # Check SRS
                    srs_error, data, srs = f.check_srs(data, srs)
                    valid, errors = addError(i, valid, srs_error, errors)

                    # Check Domain
                    domain_error, data = f.check_domain(data)
                    valid, errors = addError(i, valid, domain_error, errors)

                    # Check length of data
                    long_fields = f.check_field_length(data, long_fields)

                rowCorrected.append(data)
            dataCorrected.append(rowCorrected)

        return valid, errors, dataCorrected, long_fields, srs

def check_fields(csvFields, xsdFields):
    """Check that fields in the csv match those in the schema"""

    msg = []
    # Check if the number of fields in the csv in the same as the number of fields in the schema
    if len(xsdFields) != len(csvFields):
        msg.append("Error! The imported file does not have the correct number of fields. Check the schema.")
        msg.append(str(len(csvFields)) + " fields in the imported file (fields on the left below).")
        msg.append(str(len(xsdFields)) + " fields in the schema (fields on the right below).")
        for csvF, xsdF in map(None, csvFields, xsdFields):
            if xsdF != None:
                if csvF != xsdF.field_name:
                    msg.append(str(csvF) + " != " + xsdF.field_name)
                else:
                    msg.append(str(csvF) + " == " + xsdF.field_name)
            else:
                msg.append(str(csvF) + " != None")

    return msg


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

def addError(i, valid, error, errors):
    """ Add error message to the list of errors and set the validity"""

    if error:
        if "Error" in error:
            valid = False
        errors.append("Row " + str(i+1) + " " + error)
    return valid, errors