from sqlalchemy import text


def create_roles(app, db):
    with app.app_context():
        with db.engine.connect() as connection:
            query = text("""
                DROP USER IF EXISTS Admin;
                DROP USER IF EXISTS Researcher;
                DROP USER IF EXISTS Evaluator;
                
                CREATE USER Admin WITH PASSWORD 'password1';
                CREATE USER Researcher WITH PASSWORD 'password2';
                CREATE USER Evaluator WITH PASSWORD 'password3';
                
                GRANT USAGE ON SCHEMA public TO Admin;
                GRANT USAGE ON SCHEMA public TO Researcher;
                GRANT USAGE ON SCHEMA public TO Evaluator;
                
                GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO Admin;
                
                GRANT SELECT ON TABLE Researchers, Projects, Releases, Documents, Tag TO Researcher;
                GRANT INSERT ON TABLE Researchers, Projects, Releases(number), Documents(path) TO Researcher;
                GRANT UPDATE ON TABLE Researchers, Projects TO Researcher;
                GRANT DELETE ON TABLE Researchers, Projects TO Researcher;
                
                GRANT SELECT ON TABLE Evaluators, Projects, Releases, Documents, Tag TO Evaluator;
                GRANT INSERT ON TABLE Releases(state), Documents TO Evaluator;
                GRANT SELECT, UPDATE ON TABLE Evaluators, Releases TO Evaluator;
            """)

            connection.execute(query)
            connection.commit()
