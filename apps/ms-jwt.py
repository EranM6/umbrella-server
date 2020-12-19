from objs.microService import MicroService


class Ms_jwt(MicroService):
    replicaCount = None

    def __init__(self, service_name, namespace):
        super().__init__(service_name, namespace)
        self.replicaCount = None if namespace == "prod" else 1

    def set_resources(self):
        self.namespace != "prod" and self.resources.update({
            "requests": {
                "cpu": "750m",
                "memory": "1000Mi",
            },
            "limits": {
                "cpu": "1500m",
                "memory": "2000Mi",
            }
        })

    def set_envs(self):
        self.env.update({
            "SPRING_PROFILES_ACTIVE": "prod" if "prod" == self.namespace else "dev",
            "JVM_HEAP_MIN": "350M",
            "JVM_HEAP_MAX": "1700M" if "prod" == self.namespace else "700M",
        })

    # Overriding the default method
    def populate_ingress(self, sub_domain):
        hosts = [f'service.{domain}' for domain in
                 self.domains]
        tls = [{'secreteName': self.tlsSecrets[self.extract_domain(host)], 'hosts': [host]} for host in hosts]

        return {'hosts': hosts, 'tls': tls}
