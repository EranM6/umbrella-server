import yaml
from flask import Flask, request

from objs.microService import MicroService
from objs.react import React

app = Flask(__name__)


@app.route('/config/service', methods=['GET'])
def generate_config():
    if all([request.args.get(key) for key in ['type', 'name', 'namespace']]):
        app_type = request.args.get('type')
        app_name = request.args.get('name')
        namespace = request.args.get('namespace')

        Model = React if app_type == 'react' else MicroService

        q = Model(app_name, namespace)
        f = open('values.yaml', 'w+')
        yaml.dump(q.generate_file(), f, allow_unicode=True)
        return yaml.dump(q.generate_file())
    else:
        return "Error: Please provide all of the required arguments ('type', 'name', 'namespace')"


if __name__ == '__main__':
    app.run()
