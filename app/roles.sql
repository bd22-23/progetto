DROP USER IF EXISTS Admin;
DROP USER IF EXISTS Researcher;
DROP USER IF EXISTS Evaluator;

CREATE USER Admin WITH PASSWORD 'password1';
CREATE USER Researcher WITH PASSWORD 'password2';
CREATE USER Evaluator WITH PASSWORD 'password3';

GRANT USAGE ON SCHEMA TO Admin;
GRANT USAGE ON SCHEMA TO Researcher;
GRANT USAGE ON SCHEMA TO Evaluator;

GRANT USAGE, ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO Admin;

GRANT USAGE, SELECT ON Researchers, Projects, Releases, Documents, Tag IN SCHEMA public TO Researcher;
GRANT USAGE, INSERT ON Researchers, Projects, Releases(number), Documents(path) IN SCHEMA public TO Researcher;
GRANT USAGE, UPDATE ON Researchers(name,surname,password,profile_picture,bio,pronouns,affiliation), Projects IN SCHEMA public TO Researcher;
GRANT USAGE, DELETE ON Researchers, Projects IN SCHEMA public TO Researcher;

GRANT USAGE, SELECT ON Evaluators, Projects, Releases, Documents, Tag IN SCHEMA public TO Evaluator;
GRANT USAGE, INSERT ON Releases(state), Documents IN SCHEMA public TO Evaluator;
GRANT USAGE, UPDATE ON Evaluators(name,surname,password,profile_picture,bio,pronouns), Releases(state) IN SCHEMA public TO Evaluator;