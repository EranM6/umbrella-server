import abc
import re


class Values:
    """This is the main class for values file"""

    __metaclass__ = abc.ABCMeta

    tlsSecrets = {
        'haaretz.co.il': 'haaretz.co.il-star-tls',
        'themarker.com': 'themarker.com-star-tls',
        'haaretz.com': 'haaretz.com-star-tls',
    }

    def __init__(self, service_name, namespace):
        self.serviceName = service_name
        self.namespace = namespace
        self.tls = False

        # default values
        self.env = []
        self.replicaCount = 1
        self.resources = {
            'requests': {
                'cpu': '750m',
                'memory': '1000Mi'
            },
            'limits': {
                'cpu': '1000m',
                'memory': '1000Mi'
            }
        }
        self.ingress = {}

    def populate_ingress(self, domains, env):
        hosts = [f'{self.serviceName}{env == "dev" and "-dev"}.{domain}' for domain in domains]
        ingress = {'hosts': hosts}
        if self.tls:
            ingress['tls'] = [{'secreteName': self.tlsSecrets[self.extract_domain(host)], 'hosts': [host]} for host in hosts]
        return ingress

    def generate_file(self):
        return {
            self.serviceName: {
                'env': self.populate_envs(),
                'replicaCount': self.replicaCount,
                'resources': self.resources,
                'ingress': self.ingress
            },
        }

    @staticmethod
    def extract_domain(host):
        m = re.search('^.+\\.([haaretz|themarker].*)$', host)
        if m:
            return m.group(1)
        return ''

    @abc.abstractmethod
    def populate_envs(self):
        """Populate the `envs` list"""
        return
