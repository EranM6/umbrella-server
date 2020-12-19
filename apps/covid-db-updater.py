from objs.microService import MicroService


class Covid_db_updater(MicroService):
    replicaCount = None
    istio = False
    domains = ["haaretz.co.il"]

    def __init__(self, service_name, namespace):
        super().__init__(service_name, namespace)
        self.replicaCount = None if namespace == "prod" else 1

    def set_resources(self):
        self.namespace == "prod" or self.resources.update({
            "requests": {
                "cpu": 2,
                "memory": "1500Mi",
            },
            "limits": {
                "cpu": 4,
                "memory": "2000Mi",
            }
        })

    def set_envs(self):
        self.env.update({
            "PORT": "3000",
            "NODE_ENV": "prod" if self.namespace == "prod" else "dev",
            "INTERVAL": "20" if self.namespace == "prod" else "10",
            "LOGIN": "covid-19",
            "PASSWORD": "OrenHazan",
            "MONGO_USER": {
                "secretKeyRef": {
                    "name": "covid-db" if self.namespace == "prod" else "legacy-oracle-mongo",
                    "key": "user"
                }
            },
            "MONGO_PASS": {
                "secretKeyRef": {
                    "name": "covid-db" if self.namespace == "prod" else "legacy-oracle-mongo",
                    "key": "password"
                }
            },
            "FASTLY_KEY": {
                "secretKeyRef": {
                    "name": "fastly-tokens",
                    "key": "key"
                }
            },
            "FASTLY_SERVICE_ID": {
                "secretKeyRef": {
                    "name": "fastly-tokens",
                    "key": "subDomain"
                }
            },
            "API_KEY": {
                "secretKeyRef": {
                    "name": "coronavirus-app-token",
                    "key": "api-key"
                }
            },
        })

    # Overriding the default method
    def populate_ingress(self, sub_domain):
        hosts = [f'{self.serviceName}{"-dev" if self.namespace != "prod" else ""}.{domain}' for domain in self.domains]

        if self.namespace == "prod":
            tls = [{'secreteName': self.tlsSecrets[self.extract_domain(host)], 'hosts': [host]} for host in hosts]

        ingress = {'hosts': hosts}
        if 'tls' in locals():
            ingress['tls'] = tls

        return ingress
