import yaml
import importlib


def generate_file(app_name, namespace, file_name):
    try:
        module = importlib.import_module("apps.{}".format(app_name))
        class_ = getattr(module, app_name.replace("-", "_").capitalize())
        instance = class_(app_name, namespace)

        content = instance.generate_file()
        f = open(file_name, 'w+')
        yaml.dump(content, f, allow_unicode=True)
    except ModuleNotFoundError as e:
        return str(e)
