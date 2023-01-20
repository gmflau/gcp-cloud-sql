from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql

# initialize Connector object
connector = Connector()


# DATABASE_CONNECTION_URI = f"mysql+mysqldb://{USER}:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"


# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "central-beach-194106:us-west1:caching-demo-81ba0c0b03db4c99-mysql",
        "pymysql",
        user="demo",
        password="caching",
        db="main"
    )
    return conn

# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)


# drop table
drop_table = sqlalchemy.text('DROP TABLE IF EXISTS my_table')

# create table
create_sql = sqlalchemy.text(
    "CREATE TABLE my_table (id varchar(255) PRIMARY KEY, title varchar(255))")

# insert statement
insert_stmt = sqlalchemy.text(
    "INSERT INTO my_table (id, title) VALUES (:id, :title)",
)

with pool.connect() as db_conn:
    # drop table if exist
    db_conn.execute(drop_table)

    # create table
    db_conn.execute(create_sql)

    # insert into database
    db_conn.execute(insert_stmt, id="book1", title="Book One")

    # query database
    result = db_conn.execute("SELECT * from my_table").fetchall()

    # Do something with the results
    for row in result:
        print(row)

connector.close()


