from sqlalchemy import DDL


def create_triggers(app, db):

    triggers = [
        project_authors(),
        check_status_flow(),
        delete_old_releases()
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
            researcher_id uuid;
            num_authors INTEGER;
        BEGIN
            researcher_id := OLD.id;
            SELECT COUNT(*) INTO num_authors
            FROM authors
            WHERE researcher_id IN (SELECT researcher_id AS id FROM authors WHERE project IN
                (SELECT project FROM authors WHERE researcher_id = id) );
        
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
            IF OLD.status = 'rejected' OR OLD.status = 'accepted' THEN
                RAISE EXCEPTION 'Non è possibile modificare lo stato di una release di un progetto concluso';
            END IF;
            IF OLD.status = NEW.status THEN
                RAISE EXCEPTION 'Non è possibile modificare lo stato in sè stesso';
            END IF;
            IF OLD.status = 'returned' AND NOT EXISTS(
                SELECT * FROM releases WHERE created_at = (
                    SELECT MAX(created_at) FROM releases
                ) AND project = OLD.project
            ) THEN
                RAISE EXCEPTION 'Non è possibile modificare lo stato di una release in questo modo';
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
                DELETE FROM releases WHERE project = OLD.project AND id != OLD.id;
            END IF;
            
            RETURN OLD;
        END;
        $$ LANGUAGE plpgsql;

        CREATE OR REPLACE TRIGGER check_old_releases_trigger
        BEFORE UPDATE ON releases
        FOR EACH ROW
        EXECUTE FUNCTION check_status();
    ''')


def delete_project_rejected():
    pass
    return DDL('''\
        CREATE OR REPLACE FUNCTION check_project_rejected()
        RETURNS TRIGGER AS $$
        BEGIN
            
        END;
        $$ LANGUAGE plpgsql;

        CREATE OR REPLACE TRIGGER check_project_rejected_trigger
        BEFORE DELETE ON projects
        FOR EACH ROW
        EXECUTE FUNCTION check_project_rejected();
    ''')

