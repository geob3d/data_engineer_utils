def execute_sql_statment(db_connection, query, params=None) -> None:
    """
    Execute a SQL query dynamically using either a Session or an Engine.

    Parameters:
        db_connection (Session or Engine): A SQLAlchemy Session or Engine.
        query (str): SQL query to execute.
        params (dict, optional): Parameters to safely inject into the SQL query. Defaults to None.

    Returns:
        list: A list of result tuples from the executed query.
    """
    # Initialize params if None is provided
    if params is None:
        params = {}

    # Determine if the provided 'db_connection' is a Session or an Engine
    if isinstance(db_connection, SQLAlchemySession):
        # Execute query using a session
        db_connection.execute(text(query), params)
    elif isinstance(db_connection, Engine):
        # Create a session for the engine and execute the query
        Session = sessionmaker(bind=db_connection)
        with Session() as session:
            session.execute(text(query), params)
    else:
        raise TypeError("Provided db_connection object must be a Session or an Engine.")


# def execute_queries(db_connection, queries):
#     """
#     Execute multiple SQL queries dynamically using either a Session or an Engine.

#     Parameters:
#         db_connection (Session or Engine): A SQLAlchemy Session or Engine.
#         queries (list of tuple): Each tuple contains the SQL query as a string and an optional dictionary of parameters.

#     Returns:
#         list: A list of lists, where each sublist contains the result tuples from one executed query.
#     """
#     results = []

#     # Determine if the provided 'db_connection' is a Session or an Engine
#     if isinstance(db_connection, SQLAlchemySession):
#         for query, params in queries:
#             result = db_connection.execute(text(query), params or {})
#             results.append([row for row in result.fetchall()])
#         db_connection.commit()
#     elif isinstance(db_connection, Engine):
#         # Create a session for the engine and execute the queries
#         Session = sessionmaker(bind=db_connection)
#         with Session() as session:
#             for query, params in queries:
#                 result = session.execute(text(query), params or {})
#                 results.append([row for row in result.fetchall()])
#             session.commit()
#     else:
#         raise TypeError("Provided db_connection object must be a Session or an Engine.")

#     return results
