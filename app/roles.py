import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname='bd23',
    user='your_username',
    password='gallina96!',
    host='localhost',
    port='5000'
)

# Create a cursor to execute SQL commands
cursor = conn.cursor()

# SQL command to create a new role
Admin = 'admin'
create_role_query_admin = f"CREATE ROLE {Admin} LOGIN PASSWORD 'your_role_password';"

# SQL command to grant permissions to a role
grant_permissions_query_admin = f"GRANT ALL PRIVILEGES ON your_tabl TO {Admin};"

# Execute the SQL command
cursor.execute(create_role_query_admin)

# Execute the SQL command
cursor.execute(grant_permissions_query_admin)

User = 'user'
create_role_query_user = f"CREATE ROLE {User} LOGIN PASSWORD 'your_role_password';"

# SQL command to grant permissions to a role
grant_permissions_query_user = f"GRANT your_permission1, your_permission2, ... ON your_table TO {User};"

# Execute the SQL command
cursor.execute(create_role_query_user)

# Execute the SQL command
cursor.execute(grant_permissions_query_user)

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
