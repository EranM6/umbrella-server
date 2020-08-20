from objs.values import Values


class MicroService(Values):
    """This class is for Micro-services values file"""

    def __init__(self, service_name, namespace):
        super().__init__(service_name, namespace)
        self.tls = True
        self.ingress = self.populate_ingress(['haaretz.co.il', 'themarker.com'],
                                             'prod' if namespace == 'ms-app' else 'dev')

    def populate_envs(self):
        self.env.extend([{'name': 'aaaa', 'value': 'bbb'}, {'name': 'ppp', 'value': 'kkkk'}])
        return self.env