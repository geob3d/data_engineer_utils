# from icecream import ic

# import networkx as nx
from typing import (
    Dict,
    List,
    Union,
)

import networkx as nx
from sqlalchemy import (
    create_engine,
    inspect,
)
from sqlalchemy.engine import Connection
from sqlalchemy.orm import (
    Session,
    sessionmaker,
)


def get_execution_order(db_resource: Union[Session, Connection]) -> Union[List[str], str]:
    """
    Retrieves the execution order for SQL inserts based on foreign key dependencies.

    Args:
        db_resource (Union[Session, Connection]): An active SQLAlchemy session or connection.

    Returns:
        Union[List[str], str]: A list of table names in the order they should be inserted,
                               or an error message if there is a circular dependency.
    """
    inspector = inspect(db_resource)
    graph = nx.DiGraph()

    # Get all schemas
    schemas = inspector.get_schema_names()

    # Add nodes and edges based on foreign key relationships
    for schema in schemas:
        tables = inspector.get_table_names(schema=schema)
        for table in tables:
            full_table_name = f"{schema}.{table}" if schema else table
            graph.add_node(full_table_name)
            fks = inspector.get_foreign_keys(table, schema=schema)
            for fk in fks:
                referred_table = (
                    f"{fk['referred_schema']}.{fk['referred_table']}" if fk['referred_schema'] else fk['referred_table']
                )
                graph.add_edge(referred_table, full_table_name)

    # Perform topological sort to get execution order
    try:
        execution_order = list(nx.topological_sort(graph))
        return execution_order
    except nx.NetworkXUnfeasible:
        return "The graph has cycles, indicating a circular dependency in your schema."


def construct_key(schema: Union[str, None], table: str) -> str:
    """
    Constructs a key for the mapping dictionary based on schema and table name.

    Args:
        schema (Union[str, None]): The schema name.
        table (str): The table name.

    Returns:
        str: The constructed key.
    """
    return f"{schema}.{table}" if schema else table


def sort_table_mappings(
    table_mappings: List[Dict[str, Union[str, List[str]]]], execution_order: List[str]
) -> List[Dict[str, Union[str, List[str]]]]:
    """
    Sorts a list of table mappings based on the provided execution order.

    Args:
        table_mappings (List[Dict[str, Union[str, List[str]]]]): A list of table mappings.
        execution_order (List[str]): A list of table names in the desired execution order.

    Returns:
        List[Dict[str, Union[str, List[str]]]]: A sorted list of table mappings.
    """
    # Create a dictionary to map full table names to their corresponding mappings
    mapping_dict = {
        construct_key(mapping['targetSchema'], mapping['targetTable']): mapping for mapping in table_mappings
    }

    # Debug: Print the mapping dictionary and execution order
    print("Mapping Dictionary:", mapping_dict)
    print("Execution Order:", execution_order)

    # Sort the mappings based on the execution order
    sorted_mappings = [mapping_dict[table] for table in execution_order if table in mapping_dict]

    return sorted_mappings


# # # Example usage For testing scripts
# # if __name__ == "__main__":
# #     # Define your SQLAlchemy database URL
# #     db_url = 'sqlite:////Users/themobilescientist/Documents/projects/archive/keepitsql/test.db'  # Replace with your database URL

# #     # Create an engine and session
# #     engine = create_engine(db_url)
# #     Session = sessionmaker(bind=engine)
# #     session = Session()

# #     # Get the execution order from the database
# #     execution_order = get_execution_order(session.bind)
# #     print("Execution Order:", execution_order)

# #     # Example list of table mappings
# #     table_mappings = [
# #         {
# #             "sourceSchema": "main",
# #             "sourceTable": "users",
# #             "targetSchema": "main",
# #             "targetTable": "users",
# #             "updateKeys": [""],
# #             "loadType": "MERGE"
# #         },
# #         {
# #             "sourceSchema": "main",
# #             "sourceTable": "user_address",
# #             "targetSchema": "main",
# #             "targetTable": "user_address",
# #             "updateKeys": [""],
# #             "loadType": "MERGE"
# #         },
# #         {
# #             "sourceSchema": "main",
# #             "sourceTable": "user_phones",
# #             "targetSchema": None,
# #             "targetTable": "user_phones",
# #             "updateKeys": [""],
# #             "loadType": "MERGE"
# #         },
# #         {
# #             "sourceSchema": None,
# #             "sourceTable": "address_info",
# #             "targetSchema": 'main',
# #             "targetTable": "address_info",
# #             "updateKeys": [""],
# #             "loadType": "MERGE"
# #         }
# #     ]

# #     if isinstance(execution_order, list):
# #         sorted_table_mappings = sort_table_mappings(table_mappings, execution_order)
# #         ic("Sorted Table Mappings:", sorted_table_mappings)
# #     else:
# #         print("Error in getting execution order:", execution_order)

# #     session.close()
