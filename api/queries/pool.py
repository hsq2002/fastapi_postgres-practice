import os
# psycopg_pool is a library to create a pool
from psycopg_pool import ConnectionPool

# conninfo=os.environ['DATABASE_URL']--> create a pool base
# of the connection information in the docker-compose file
pool=ConnectionPool(conninfo=os.environ['DATABASE_URL'])
