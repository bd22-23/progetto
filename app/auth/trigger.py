# from app import db


def create_refresh_users_function(db):
    query = f"""
        CREATE OR REPLACE FUNCTION refresh_users()
        RETURNS TRIGGER AS $$
        BEGIN
            REFRESH MATERIALIZED VIEW users;
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql
    """
    with db.engine.connect() as connection:
        connection.execute(query)
        connection.commit()


def create_refresh_users_trigger(db, table_name):
    create_refresh_users_function(db)
    query = f"""
        CREATE OR REPLACE TRIGGER refresh_users_trigger
        AFTER INSERT OR UPDATE OR DELETE
        ON {table_name}
        EXECUTE PROCEDURE refresh_users();
    """.format(table_name=table_name)
    with db.engine.connect() as connection:
        connection.execute(query)
        connection.commit()
