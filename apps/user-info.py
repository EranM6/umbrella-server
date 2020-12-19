from objs.microService import MicroService


class User_info(MicroService):
    domains = ['haaretz.co.il']
    replicaCount = None

    def __init__(self, service_name, namespace):
        super().__init__(service_name, namespace)

    def set_envs(self):
        self.env.update({
            "PROFILE": "prod" if "prod" == self.namespace else "stage",
            "GOOGLE_APPLICATION_CREDENTIALS": "/secrets/pubsub-creds.json",
            "GOOGLE_APPLICATION_CREDENTIALS2": "/secrets2/bigQuery-creds.json",
            "MONGO_USER": {
                "secretKeyRef": {
                    "name": "user-info-mongo" if self.namespace == "prod" else "legacy-oracle-mongo",
                    "key": "user"
                }
            },
            "MONGO_PASS": {
                "secretKeyRef": {
                    "name": "user-info-mongo" if self.namespace == "prod" else "legacy-oracle-mongo",
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
