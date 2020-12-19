from objs.microService import MicroService


class Ms_customer_service(MicroService):
    domains = ['haaretz.co.il', 'themarker.com']

    def __init__(self, service_name, namespace):
        super().__init__(service_name, namespace)

    def set_resources(self):
        self.resources.update({
            "requests": {
                "cpu": "800m",
                "memory": "800Mi",
            },
            "limits": {
                "cpu": "2000m",
                "memory": "2800Mi",
            }
        })

    def set_envs(self):
        self.env.update({
            "SPRING_PROFILES_ACTIVE": "prod" if "prod" == self.namespace else "stage",
            "JVM_HEAP_MIN": "350M",
            "JVM_HEAP_MAX": "800M",
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
        self.namespace == "prod" and self.env.update({
            "OPERATIONS_MONGO_USER": {
                "secretKeyRef": {
                    "name": "mongo-creds-operations",
                    "key": "user"
                }
            },
            "OPERATIONS_MONGO_PASS": {
                "secretKeyRef": {
                    "name": "mongo-creds-operations",
                    "key": "password"
                }
            },
        })
