from objs.microService import MicroService


class Ms_otp(MicroService):
    domains = ['haaretz.co.il', 'themarker.com']

    def __init__(self, service_name, namespace):
        super().__init__(service_name, namespace)
        self.replicaCount = None if namespace == "prod" else 1

    def set_resources(self):
        self.namespace == "prod" or self.resources.update({
            "requests": {
                "cpu": "2000m",
                "memory": "2800Mi",
            },
            "limits": {
                "cpu": "2000m",
                "memory": "2800Mi",
            }
        })

    def set_envs(self):
        self.env.update({
            "SPRING_PROFILES_ACTIVE": "production" if "prod" == self.namespace else "test",
            "JVM_HEAP_MIN": "350M",
            "JVM_HEAP_MAX": "2800M",
            "GOOGLE_APPLICATION_CREDENTIALS": "/pubsub-secrets/pubsub-creds.json",
            "ACCESS_CIPHER": {
                "secretKeyRef": {
                    "name": "access-tokens", "key": "accessCipher"
                }
            },
            "APP_KEY": {
                "secretKeyRef": {
                    "name": "access-tokens", "key": "appKey"
                }
            },
            "MONGO_USER": {
                "secretKeyRef": {
                    "name": "mongo-creds-operations" if self.namespace == "prod" else "legacy-oracle-mongo",
                    "key": "user"
                }
            },
            "MONGO_PASS": {
                "secretKeyRef": {
                    "name": "mongo-creds-operations" if self.namespace == "prod" else "legacy-oracle-mongo",
                    "key": "password"
                }
            },
        })
