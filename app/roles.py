'''
import psycopg2

conn = psycopg2.connect(
    dbname='bd23',
    # user='your_username',
    password='gallina96!',
    host='localhost',
    port='5000'
)
cursor = conn.cursor()

Admin = 'admin'
create_role_query_admin = f"CREATE ROLE {Admin};"
cursor.execute(create_role_query_admin)
grant_permissions_query_admin = f"GRANT ALL PRIVILEGES ON ALL TABLES TO {Admin};"
cursor.execute(grant_permissions_query_admin)

Evaluators = 'evaluators'
create_role_query_evaluators = f"CREATE ROLE {Evaluators};"
cursor.execute(create_role_query_evaluators)
cursor.execute(f"GRANT SELECT ON Evaluators, Projects, Releases, Documents, Tag TO {Evaluators};")
cursor.execute(f"GRANT INSERT ON Releases(state), Documents TO {Evaluators};")
cursor.execute(f"GRANT UPDATE ON Evaluators(name,surname,password,profile_picture,bio,pronouns), Releases(state) TO {Evaluators};")

Researcher = 'researcher'
create_role_query_researcher = f"CREATE ROLE {Researcher} LOGIN PASSWORD '...';"
cursor.execute(create_role_query_researcher)
cursor.execute(f"GRANT SELECT ON Researchers, Projects, Releases, Documents, Tag TO {Researcher};")
cursor.execute(f"GRANT INSERT ON Researchers, Projects, Releases(number), Documents(path) TO {Researcher};")
cursor.execute(f"GRANT UPDATE ON Researchers(name,surname,password,profile_picture,bio,pronouns,affiliation), Projects TO {Researcher};")
cursor.execute(f"GRANT DELETE ON Researchers, Projects TO {Researcher};")

conn.commit()
cursor.close()
conn.close()
'''




