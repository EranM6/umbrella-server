from objs.microService import MicroService


class Ms_personal_newsletter(MicroService):
    domains = ['haaretz.co.il', 'themarker.com']

    def __init__(self, service_name, namespace):
        super().__init__(service_name, namespace)

    def set_envs(self):
        self.env.update({
            "SPRING_PROFILES_ACTIVE": "prod" if "prod" == self.namespace else "stage",
            "JVM_HEAP_MIN": "350M",
            "JVM_HEAP_MAX": "800M",
            "GOOGLE_APPLICATION_CREDENTIALS": "/secrets/bigQuery-creds.json",
            "MONGO_USER": {
                "secretKeyRef": {
                    "name": "mongo-personal-newsletter" if self.namespace == "prod" else "legacy-oracle-mongo",
                    "key": "username" if self.namespace == "prod" else "user",
                }
            },
            "MONGO_PASS": {
                "secretKeyRef": {
                    "name": "mongo-personal-newsletter" if self.namespace == "prod" else "legacy-oracle-mongo",
                    "key": "password",
                }
            },
        })

