import sqlalchemy as db
import os
import pandas as pd

db_user = 'sa'
db_password = os.getenv('MY_DB_PASSWORD')
db_host = "localhost"
db_port = "1443"
db_name = 'master'

connection_url = f"mssql+pyodbc://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=no&TrustServerCertificate=yes"

engine = db.create_engine(connection_url)

log_query = """
INSERT INTO PipelineLog (ExecutionStart, ExecutionEnd, RowsInserted, PipelineStatus)
VALUES (:start, :end, :rows, :status);
"""

with engine.connect() as connection:
    connection.execute(
        db.text(log_query),
        {
            "start": start_time,
            "end": end_time,
            "rows": len(cleaned_df),
            "status": "SUCCESS"
        }
    )
    connection.commit()