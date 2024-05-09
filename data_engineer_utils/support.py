import os


def schema_formatter(schema_name: str, schema_prefix: str | None = None):
    default_schema_list = ["dbo", "public"]
    new_schema = ""

    if schema_prefix is None:
        new_schema = schema_name
    else:
        new_schema = schema_prefix if schema_name in default_schema_list else f"{schema_prefix}_{schema_name}"

    return new_schema


def concat_dict_to_delimated_list(col_Value):
    if isinstance(col_Value, dict):
        return ",".join([str(i) for i in col_Value.values()])
    else:
        return col_Value


# def load_json_file(json_file: str):
#     project_root = os.path.dirname(os.path.dirname(__file__))
#     filename = os.path.join(project_root, json_file)

#     with open(filename, "r") as myfile:
#         data = myfile.read()
#     # parse file
#     obj = json.loads(data)
#     return obj
