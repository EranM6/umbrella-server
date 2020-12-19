from objs.microService import MicroService


class Personalization(MicroService):
    domains = ['haaretz.co.il', 'themarker.com']

    def __init__(self, service_name, namespace):
        super().__init__(service_name, namespace)
        self.replicaCount = None if namespace == "prod" else 1

    def set_resources(self):
        self.namespace == "prod" or self.resources.update(self.get_default_resources())

    def set_autoscale(self):
        self.namespace == "prod" and self.autoscale.update({
            "minReplicas": 1,
            "maxReplicas": 5,
            "metrics": [
                {
                    "type": "Resource",
                    "resource": {
                        "name": "cpu",
                        "targetAverageUtilization": 50
                    }
                }
            ]
        })

    def set_envs(self):
        self.env.update({
            "SPRING_PROFILES_ACTIVE": "production" if "prod" == self.namespace else "test",
            "MONGO_USER": {
                "secretKeyRef": {
                    "name": "mongo-creds-personal" if self.namespace == "prod" else "legacy-oracle-mongo",
                    "key": "username" if self.namespace == "prod" else "user"
                }
            },
            "MONGO_PASS": {
                "secretKeyRef": {
                    "name": "mongo-creds-personal" if self.namespace == "prod" else "legacy-oracle-mongo",
                    "key": "password"
                }
            },
        })

    # Overriding the default method
    def populate_ingress(self, sub_domain):
        hosts = [f'data-api{"-dev" if self.namespace != "prod" else ""}.{domain}' for domain in self.domains]

        if self.namespace != "prod":
            hosts.extend(
                [f'data-api{"-dev" if self.namespace != "prod" else ""}.{sub_domain}.{domain}' for domain in
                 self.domains]
            )
            tls = [{'secreteName': self.tlsSecrets[self.extract_domain(host)], 'hosts': [host]} for host in
                  list(filter(lambda host: "k8s" not in host, hosts))]

        ingress = {'hosts': hosts}
        if 'tls' in locals():
            ingress['tls'] = tls

        return ingress
