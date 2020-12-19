from objs.microService import MicroService


class Cookie_generator(MicroService):
    domains = ['haaretz.co.il']
    replicaCount = None

    def __init__(self, service_name, namespace):
        super().__init__(service_name, namespace)

    def set_envs(self):
        self.env.update({
            "SPRING_PROFILES_ACTIVE": "prod" if "prod" == self.namespace else "stage",
            "JVM_HEAP_MIN": "350M",
            "JVM_HEAP_MAX": "1300M" if "prod" == self.namespace else "700M",
            "GOOGLE_APPLICATION_CREDENTIALS": "/secrets/pubsub-creds.json",
            "MONGO_USER": {
                "secretKeyRef": {
                    "name": "user-info-reader-mongo" if self.namespace == "prod" else "legacy-oracle-mongo",
                    "key": "user"
                }
            },
            "MONGO_PASS": {
                "secretKeyRef": {
                    "name": "user-info-reader-mongo" if self.namespace == "prod" else "legacy-oracle-mongo",
                    "key": "password"
                }
            },
        })

    # Overriding the default method
    def populate_ingress(self, sub_domain):
        hosts = [f'{self.serviceName}{"-dev" if self.namespace != "prod" else ""}.{domain}' for domain in
                 self.domains]

        hosts.extend([f'{self.serviceName}.{sub_domain}.{domain}' for domain in self.domains])

        return {'hosts': hosts}
