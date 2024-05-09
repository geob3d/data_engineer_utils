class CreateConnectionString:
    def __init__(self, server_name, database_name):
        self.server_name = server_name
        self.database_name = database_name

    def mssql_integrated_security(self):
        return f"mssql+pyodbc://{self.server_name}/{self.database_name}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
        # conn_str = "?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
        # engine = "mssql+pyodbc://"
        # + self.server_name
        # + "/"
        # + self.database_name
        # + "?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server",
        # fast_executemany=True,
