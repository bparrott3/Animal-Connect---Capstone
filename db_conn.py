import mysql.connector
from urllib.parse import urlparse, unquote

# Database connection URL
DATABASE_URL = "mysql://root:E3aGe2efbfcfGCbCb2AhEfbBC1de1Hf4@viaduct.proxy.rlwy.net:53588/railway"

def get_db_connection():
    # Parse the database URL
    parsed_url = urlparse(DATABASE_URL)
    username = parsed_url.username
    password = unquote(parsed_url.password)  # URL decode the password
    host = parsed_url.hostname
    port = parsed_url.port
    database = parsed_url.path.lstrip('/')

    # Connect to the database
    try:
        connection = mysql.connector.connect(user=username, password=password,
                                             host=host, port=port, database=database)
        print("Database connection successful.")
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None
