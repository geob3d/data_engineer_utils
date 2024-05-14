sqlalchemy_drivers_merge_systems = {
    "oracle": {"drivers": ["oracle+cx_oracle", "oracle+oracledb", "oracle+pyodbc"], "upsert_type": "MERGE"},
    "mssql": {"drivers": ["mssql+pyodbc", "mssql+pymssql", "mssql+adodbapi", "mssql+pytds"], "upsert_type": "MERGE"},
    "db2": {"drivers": ["ibm_db_sa", "db2+ibm_db", "db2+pyodbc"], "upsert_type": "MERGE"},
    "postgresql": {
        "drivers": [
            "postgresql+psycopg2",
            "postgresql+pg8000",
            "postgresql+asyncpg",
            "postgresql+pygresql",
            "postgresql+psycopg",
        ],
        "upsert_type": "ON CONFLICT",  # For versions before 15 # For versions 15 and abov
    },
    "mysql": {
        "drivers": [
            "mysql+mysqlconnector",
            "mysql+pymysql",
            "mysql+mysqldb",
            "mysql+pyodbc",
            "mysql+cymysql",
            "mysql+aiomysql",
        ],
        "upsert_type": "ON DUPLICATE KEY UPDATE",
    },
    "sqlite": {"drivers": ["sqlite+pysqlite"], "upsert_type": "ON CONFLICT"},
    "teradata": {"drivers": ["teradata+teradata"], "upsert_type": "MERGE"},
    "hana": {"drivers": ["hana+pyhdb", "hana+hdbcli"], "upsert_type": "MERGE"},
    "snowflake": {"drivers": ["snowflake+snowflake"], "upsert_type": "MERGE"},
    "redshift": {"drivers": ["redshift+psycopg2", "redshift+redshift_connector"], "upsert_type": "MERGE"},
    "bigquery": {"drivers": ["bigquery+bigquery"], "upsert_type": "MERGE"},
}


# Additional mssql_local entry for local temporary table in MSSQL
# sqlalchemy_drivers_merge_systems["mssql_global"] = {
#     "drivers": ["mssql+pyodbc", "mssql+pymssql", "mssql+adodbapi", "mssql+pytds"],
#     "create_temp_table_header": "CREATE TABLE ##{table_name} ",
#     "upsert_type": "MERGE"
# }

dbms_list = list(sqlalchemy_drivers_merge_systems.keys())


def get_dbms_by_py_driver(driver_name) -> str:
    """
    Finds the DBMS key based on the given SQLAlchemy driver.

    Args:
        target_value (str): The SQLAlchemy driver string to search for.

    Returns:
        Optional[str]: The DBMS key if found, otherwise None.

    Raises:
        ValueError: If the target_value is not found in any DBMS drivers.
    """
    dbms_key = next(
        (key for key, value in sqlalchemy_drivers_merge_systems.items() if driver_name in value["drivers"]), None
    )

    if dbms_key is None:
        raise ValueError(f"The target value {driver_name} is not found in any DBMS drivers.")

    return dbms_key


def get_upsert_type_by_dbms(dbms_name: str) -> str:
    dbms_config = sqlalchemy_drivers_merge_systems.get(dbms_name)

    if dbms_config is None:
        raise ValueError(f"DBMS '{dbms_name}' is not found in the configuration.")

    upsert_type = dbms_config.get('upsert_type')

    if upsert_type is None:
        raise ValueError(f"Upsert type for DBMS '{dbms_name}' is not defined.")

    return upsert_type


print(get_upsert_type_by_dbms('postgresql'))
