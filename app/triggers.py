from sqlalchemy import DDL


def create_triggers(app, db):

    triggers = [
        project_authors(),
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


def delete_project_rejected():
    pass
    # return DDL('''\
    #     CREATE OR REPLACE FUNCTION check_project_status()
    #     RETURNS TRIGGER AS $$
    #     DECLARE
    #         researcher_id uuid;
    #         num_authors INTEGER;
    #     BEGIN
    #         researcher_id := OLD.id;
    #         SELECT COUNT(*) INTO num_authors
    #         FROM authors
    #         WHERE researcher_id IN (SELECT researcher_id AS id FROM authors WHERE project IN
    #             (SELECT project FROM authors WHERE researcher_id = id) );
    #
    #         IF num_authors <= 1 THEN
    #             RAISE EXCEPTION 'Non è possibile eliminare il ricercatore perché è l''unico autore collegato ad un progetto.';
    #         END IF;
    #
    #         RETURN OLD;
    #     END;
    #     $$ LANGUAGE plpgsql;
    #
    #     CREATE OR REPLACE TRIGGER check_project_status_trigger
    #     BEFORE DELETE ON release
    #     FOR EACH ROW
    #     EXECUTE FUNCTION check_project_status();
    # ''')

