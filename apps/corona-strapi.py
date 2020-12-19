from objs.microService import MicroService


class Corona_strapi(MicroService):
    replicaCount = None

    def __init__(self, service_name, namespace):
        super().__init__(service_name, namespace)
        self.replicaCount = None if namespace == "prod" else 1
        self.set_liveness(1337, "/")
        self.set_readiness(1337, "/")
        self.ingress = None

    def set_envs(self):
        self.env.update({
            "NODE_ENV": "production",
            "STRAPI_LOG_LEVEL": "info",
            "DB_UPDATE_USER": "covid-19",
            "DB_UPDATE_PASS": "OrenHazan",
            "DATABASE_CLIENT": "mongo",
            "DATABASE_URI": {
                "secretKeyRef": {
                    "name": "strapi-mongo-secret",
                    "key": "DATABASE_URI"
                }
            },
            "STRAPI_ADMIN_JWT_SECRET": {
                "secretKeyRef": {
                    "name": "strapi-jwt-key",
                    "key": "api_key"
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
        })
