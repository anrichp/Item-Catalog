import os
from app import create_app, db
from app.models import Item, Category

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Item=Item, Category=Category)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
