from objs.values import Values


class MicroService(Values):
    """This class is for Micro-services values file"""

    tls = True
    domains = ['haaretz.co.il', 'themarker.com', 'haaretz.com']

    def __init__(self, service_name, namespace):
        super().__init__(service_name, namespace)
        self.ingress = self.populate_ingress(
            "k8s-{}".format('prod' if namespace == 'prod' else 'stage')
        )

        # Initialize dictionaries
        self.env = {}
        self.autoscale = {}
        self.resources = {}

    def set_envs(self):
        return

    def set_resources(self):
        return

    def set_autoscale(self):
        return
