from objs.microService import MicroService


class Ms_ds(MicroService):
    domains = ['haaretz.co.il', 'themarker.com']

    def __init__(self, service_name, namespace):
        super().__init__(service_name, namespace)

    def set_envs(self):
        self.env.update({
            "SPRING_PROFILES_ACTIVE": "prod" if "prod" == self.namespace else "stage",
            "JVM_HEAP_MIN": "350M",
            "JVM_HEAP_MAX": "800M",
            "GOOGLE_APPLICATION_CREDENTIALS": "/pubsub-secrets/pubsub-creds.json",
        })

    def set_autoscale(self):
        self.namespace == "prod" and self.autoscale.update({
            "minReplicas": 3,
            "maxReplicas": 20,
        })
