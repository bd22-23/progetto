from sqlalchemy import text

from app import create_app
from app import db


app = create_app()
with app.app_context():
    # Questa estensione contiene diverse funzioni che permettono la creazione di
    # UUID a livello di DBMS piuttosto che Flask.
    with db.engine.connect() as conn:
        result = conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8080, debug=True)
