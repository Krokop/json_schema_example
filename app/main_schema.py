import flaskext.couchdb
from flask import Flask, g, request, send_from_directory


main_app = Flask(__name__)


@main_app.route('/schemas/<path:path>')
def get_schema(path):
    return send_from_directory('../schemas', path)


"""
Flask main
"""
if __name__ == "__main__":
    main_app.config.update(DEBUG=True)
    main_app.run()
