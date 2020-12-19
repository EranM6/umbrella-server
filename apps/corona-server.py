from objs.microService import MicroService


class Corona_server(MicroService):
    replicaCount = None

    def __init__(self, service_name, namespace):
        super().__init__(service_name, namespace)
        self.replicaCount = None if namespace == "prod" else 1
        self.istio = False if namespace == "prod" else None
        self.set_liveness(9000, "/ready")
        self.set_readiness(9000, "/ready")

    def set_envs(self):
        self.env.update({
            "PORT": "3000",
            "NODE_ENV": "prod" if self.namespace == "prod" else "stage",
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
        })

    # Overriding the default method
    def populate_ingress(self, sub_domain):
        hosts = [f'covid{"-dev" if self.namespace != "prod" else ""}.{domain}' for domain in self.domains]

        tls = [{'secreteName': self.tlsSecrets[self.extract_domain(host)], 'hosts': [host]} for host in hosts]

        return {'hosts': hosts, 'tls': tls}
