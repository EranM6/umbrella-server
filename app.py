import yaml
from flask import Flask, request, send_from_directory, abort
from utils import generate_file

app = Flask(__name__)


@app.route('/config', methods=['GET'])
def main():
    if not all([request.args.get(key) for key in ['name', 'namespace']]):
        abort(400, "Error: Please provide all of the required arguments ('name', 'namespace')")

    app_name = request.args.get('name')
    namespace = request.args.get('namespace')
    file_name = 'values-temp.yaml'

    error = generate_file(app_name, namespace, file_name)

    if error:
        abort(400, error)

    return send_from_directory("./", file_name, as_attachment=True)


if __name__ == '__main__':
    app.run()
