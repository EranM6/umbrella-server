from objs.microService import MicroService


class Ms_user_alerts(MicroService):
    domains = ['haaretz.co.il']
    replicaCount = None

    def __init__(self, service_name, namespace):
        super().__init__(service_name, namespace)
        self.replicaCount = None if namespace == "prod" else 1

    def set_resources(self):
        self.resources.update({
            "requests": {
                "cpu": "800m",
                "memory": "800Mi",
            },
            "limits": {
                "cpu": "2000m" if self.namespace == "prod" else "1000m",
                "memory": "2800Mi" if self.namespace == "prod" else "1000Mi",
            }
        })

    def set_envs(self):
        self.env.update({
            "SPRING_PROFILES_ACTIVE": "prod" if "prod" == self.namespace else "test",
            "JVM_HEAP_MIN": "350M",
            "JVM_HEAP_MAX": "2700M" if "prod" == self.namespace else "700M",
            "GOOGLE_APPLICATION_CREDENTIALS": "/bigquery-secrets/bigQuery-writer-creds.json",
            "MONGO_USER": {
                "secretKeyRef": {
                    "name": "legacy-oracle-mongo",
                    "key": "user"
                }
            },
            "MONGO_PASS": {
                "secretKeyRef": {
                    "name": "legacy-oracle-mongo",
                    "key": "password"
                }
            },
        })

    # Overriding the default method
    def populate_ingress(self, sub_domain):
        hosts = [f'{self.serviceName}{"-dev" if self.namespace != "prod" else ""}.{domain}' for domain in
                 self.domains]

        return {'hosts': hosts}
