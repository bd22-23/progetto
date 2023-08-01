DROP USER IF EXISTS Admin;
DROP USER IF EXISTS Researcher;
DROP USER IF EXISTS Evaluator;
DROP USER IF EXISTS AppUser;

-- Utente senza account, può registrarsi e vedere i progetti pubblici
CREATE USER AppUser WITH PASSWORD 'password';
GRANT USAGE ON SCHEMA public TO AppUser;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO AppUser;
GRANT INSERT ON public.users, public.researchers TO AppUser;

CREATE USER Admin WITH PASSWORD 'password1';
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO Admin;

CREATE USER Researcher WITH PASSWORD 'password2';
GRANT AppUser TO Researcher;
GRANT INSERT ON TABLE public.projects, public.releases, public.documents, public.authors, public.project_tags TO Researcher;
GRANT DELETE ON TABLE public.researchers, public.projects TO Researcher;
GRANT UPDATE(title, abstract) ON TABLE public.projects TO Researcher;
GRANT UPDATE(name, surname, password, email) ON TABLE public.users TO Researcher;
GRANT UPDATE(pronouns, affiliation) ON TABLE public.researchers TO Researcher;
-- Update dei tag dei progetti? Per ora non si può fare

CREATE USER Evaluator WITH PASSWORD 'password3';
GRANT AppUser TO Evaluator;
GRANT UPDATE(status) ON TABLE public.releases TO Evaluator;
GRANT UPDATE(evaluator_id) ON TABLE public.projects TO Evaluator;
GRANT UPDATE(annotations) ON TABLE public.documents TO Evaluator;
GRANT UPDATE(name, surname, password, email) ON TABLE public.users TO Evaluator;
GRANT UPDATE(bio, pronouns) ON TABLE public.evaluators TO Evaluator;