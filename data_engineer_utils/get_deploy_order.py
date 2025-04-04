from typing import (
    Dict,
    List,
    Optional,
    Union,
)

import networkx as nx
from sqlalchemy import inspect
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session


def construct_key(schema: Optional[str], table: str) -> str:
    """
    Constructs a case-sensitive schema.table key.
    """
    return f"{schema}.{table}" if schema else table


def get_execution_order(
    db_resource: Union[Session, Connection],
    table_mappings: List[Dict[str, Union[str, List[str]]]],
    reverse: bool = False,
) -> Union[List[str], str]:
    """
    Retrieves the execution order for inserts based on foreign key dependencies.
    Only includes tables defined in the config (table_mappings).

    Args:
        db_resource: SQLAlchemy session or connection.
        table_mappings: List of target schema/table mappings from config.
        reverse: If True, reverses the order (e.g. for deletes).

    Returns:
        Ordered list of schema.table names or error message.
    """
    inspector = inspect(db_resource)
    graph = nx.DiGraph()

    # Build a set of fully qualified target tables from config
    target_tables = {construct_key(mapping['targetSchema'], mapping['targetTable']) for mapping in table_mappings}

    for schema in inspector.get_schema_names():
        for table in inspector.get_table_names(schema=schema):
            full_table = construct_key(schema, table)
            if full_table not in target_tables:
                continue

            graph.add_node(full_table)

            for fk in inspector.get_foreign_keys(table, schema=schema):
                ref_schema = fk.get('referred_schema') or schema
                ref_table = fk.get('referred_table')
                ref_full = construct_key(ref_schema, ref_table)

                if ref_full in target_tables:
                    graph.add_edge(ref_full, full_table)

    try:
        execution_order = list(nx.topological_sort(graph))
        return list(reversed(execution_order)) if reverse else execution_order
    except nx.NetworkXUnfeasible:
        return "The graph has cycles, indicating a circular dependency in your schema."


def sort_table_mappings(
    table_mappings: List[Dict[str, Union[str, List[str]]]],
    execution_order: List[str],
) -> List[Dict[str, Union[str, List[str]]]]:
    """
    Sorts a list of table mappings based on the provided execution order.
    """
    mapping_dict = {
        construct_key(mapping['targetSchema'], mapping['targetTable']): mapping for mapping in table_mappings
    }

    sorted_mappings = [mapping_dict[table] for table in execution_order if table in mapping_dict]

    return sorted_mappings
