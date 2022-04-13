from jsonschema import validate, ValidationError, SchemaError


def validate_payload_schema(request_schema: object, request_data):
    """
        Validate request parameters
        """
    try:
        validate(request_data, request_schema)

    except ValidationError as e:
        return e.message
    except SchemaError as error:
        return error.message
