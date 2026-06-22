import sqlalchemy as db
import os

db_user = 'sa'
db_password = os.getenv('MY_DB_PASSWORD')
db_host = "localhost"
db_port = "1443"
db_name = 'master'

connection_url = f"mssql+pyodbc://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=no&TrustServerCertificate=yes"

engine = db.create_engine(connection_url)

