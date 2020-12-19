import abc
import re


class Values:
    """This is the main class for values file"""

    __metaclass__ = abc.ABCMeta

    # default values
    resources = {}
    autoscale = {}
    readiness = {}
    liveness = {}
    env = {}
    replicaCount = 1
    ingress = {}
    tls = False
    istio = None
    domains = []
    tlsSecrets = {
        'haaretz.co.il': 'haaretz.co.il-star-tls',
        'themarker.com': 'themarker.com-star-tls',
        'haaretz.com': 'haaretz.com-star-tls',
    }

    def __init__(self, service_name, namespace):
        self.serviceName = service_name
        self.namespace = namespace

    def populate_ingress(self, sub_domain):
        hosts = [f'{self.serviceName}.{sub_domain}.{domain}' for domain in self.domains]
        ingress = {'hosts': hosts}
        if self.tls:
            ingress['tls'] = [{'secreteName': self.tlsSecrets[self.extract_domain(host)], 'hosts': [host]} for host in
                              hosts]
        return ingress

    def generate_file(self):
        output = {
            self.serviceName: {},
        }

        self.set_resources()
        self.set_autoscale()
        self.set_envs()

        if self.resources:
            output[self.serviceName]['resources'] = self.resources

        if self.ingress:
            output[self.serviceName]['ingress'] = self.ingress

        if self.autoscale:
            output[self.serviceName]['autoscale'] = self.autoscale

        if self.replicaCount:
            output[self.serviceName]['replicaCount'] = self.replicaCount

        if self.env:
            output[self.serviceName]['env'] = self.__populate_envs()

        if self.readiness:
            output[self.serviceName]['readinessProbe'] = self.readiness

        if self.liveness:
            output[self.serviceName]['livenessProbe'] = self.liveness

        if self.istio is not None:
            output[self.serviceName]['istio'] = {"enabled": self.istio}

        return output

    def set_readiness(self, port, path):
        self.readiness = {
            "httpGet": {
                "path": path,
                "port": port
            }
        }

    def set_liveness(self, port, path):
        self.liveness = {
            "httpGet": {
                "path": path,
                "port": port
            }
        }

    @staticmethod
    def get_default_resources():
        return {
            'requests': {
                'cpu': '750m',
                'memory': '1000Mi'
            },
            'limits': {
                'cpu': '1000m',
                'memory': '1000Mi'
            }
        }

    @staticmethod
    def extract_domain(host):
        m = re.search('^.+\\.([haaretz|themarker].*)$', host)
        if m:
            return m.group(1)
        return ''

    def __populate_envs(self):
        return list(
            {"name": key, "value" if type(self.env[key]) is str else "valueFrom": self.env[key]} for key in self.env)

    @abc.abstractmethod
    def set_resources(self):
        """Populate `resources` obj"""
        return

    @abc.abstractmethod
    def set_autoscale(self):
        """Populate `resources` obj"""
        return

    @abc.abstractmethod
    def set_envs(self):
        """Populate the `envs` list"""
        return
