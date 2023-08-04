from sqlalchemy import DDL


def create_triggers(app, db):

    triggers = [
        project_authors(),
        check_status_flow(),
        delete_old_releases(),
        increase_evaluator_grade(),
        delete_project_rejected()
    ]

    with app.app_context():
        with db.engine.connect() as connection:
            for trigger in triggers:
                connection.execute(trigger)
                connection.commit()


def project_authors():
    return DDL('''\
        CREATE OR REPLACE FUNCTION check_authors()
        RETURNS TRIGGER AS $$
        DECLARE
            r_id uuid;
            num_authors INTEGER;
        BEGIN
            r_id := OLD.id;
            SELECT COUNT(*) INTO num_authors
            FROM authors
            WHERE researcher_id IN (SELECT researcher_id AS id FROM authors WHERE project_id IN
                (SELECT project_id FROM authors WHERE researcher_id = r_id) );
        
            IF num_authors <= 1 THEN
                RAISE EXCEPTION 'Non è possibile eliminare il ricercatore perché è l''unico autore collegato ad un progetto.';
            END IF;
            
            RETURN OLD;
        END;
        $$ LANGUAGE plpgsql;
        
        CREATE OR REPLACE TRIGGER check_authors_trigger
        BEFORE DELETE ON researchers
        FOR EACH ROW
        EXECUTE FUNCTION check_authors();
    ''')


def check_status_flow():
    return DDL('''\
        CREATE OR REPLACE FUNCTION check_status()
        RETURNS TRIGGER AS $$
        BEGIN
            IF OLD.status = 'rejected' OR OLD.status = 'accepted' OR old.status = 'returned' THEN
                RAISE EXCEPTION 'Non è possibile modificare lo stato di una release di un progetto concluso';
            END IF;
            IF OLD.status = NEW.status THEN
                RAISE EXCEPTION 'Non è possibile modificare lo stato in sè stesso';
            END IF;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE OR REPLACE TRIGGER check_status_trigger
        BEFORE UPDATE ON releases
        FOR EACH ROW
        EXECUTE FUNCTION check_status();
    ''')


def delete_old_releases():
    return DDL('''\
        CREATE OR REPLACE FUNCTION check_old_releases()
        RETURNS TRIGGER AS $$
        BEGIN
            IF OLD.status = 'rejected' OR OLD.status = 'accepted' THEN
                DELETE FROM releases WHERE project_id = OLD.project_id AND id != OLD.id;
            END IF;
            
            RETURN OLD;
        END;
        $$ LANGUAGE plpgsql;

        CREATE OR REPLACE TRIGGER check_old_releases_trigger
        BEFORE UPDATE ON releases
        FOR EACH ROW
        EXECUTE FUNCTION check_old_releases();
    ''')


def increase_evaluator_grade():
    return DDL('''\
        CREATE OR REPLACE FUNCTION increase_evaluator_grade()
        RETURNS TRIGGER AS $$
        DECLARE
            e_id uuid;
            num_releases INTEGER;
        BEGIN
            SELECT evaluator_id INTO e_id
            FROM projects
            WHERE id = NEW.project
            LIMIT 1;
        
            SELECT COUNT(*) INTO num_releases
            FROM projects
            WHERE evaluator_id = e_id;
            
            IF (num_releases = 15) THEN
                UPDATE evaluators
                SET grade = 'intermediate'
                WHERE id = e_id;
            ELSIF (num_releases = 50) THEN
                UPDATE evaluators
                SET grade = 'expert'
                WHERE id = e_id;
            END IF;
        END;
        $$ LANGUAGE plpgsql;

        CREATE OR REPLACE TRIGGER increase_evaluator_grade_trigger
        AFTER UPDATE ON releases
        FOR EACH ROW
        EXECUTE FUNCTION increase_evaluator_grade();
    ''')


def delete_project_rejected():
    return DDL('''\
        CREATE OR REPLACE FUNCTION check_project_rejected()
        RETURNS TRIGGER AS $$
        DECLARE
            stat varchar;
        BEGIN
            SELECT status INTO stat
            FROM releases
            WHERE created_at = (
                SELECT MAX(created_at)
                FROM releases
                WHERE project_id = id
            );
            IF(stat != 'rejected') THEN
                RAISE EXCEPTION 'Non puoi eliminare un progetto che non è stato rifiutato';
            END IF;
            
            RETURN OLD;
        END;
        $$ LANGUAGE plpgsql;

        CREATE OR REPLACE TRIGGER check_project_rejected_trigger
        BEFORE DELETE ON projects
        FOR EACH ROW
        EXECUTE FUNCTION check_project_rejected();
    ''')
