from app import create_app
from os import path

app = create_app()

if __name__ == '__main__':
    if not path.exists("app/db.sqlite"):
         with app.app_context():
            from app import db
            db.create_all()
    app.run(debug=True)
