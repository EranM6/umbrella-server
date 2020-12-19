from objs.microService import MicroService


class Gcp_general_jobs(MicroService):
    def __init__(self, service_name, namespace):
        super().__init__(service_name, namespace)
        self.replicaCount = None if namespace == "prod" else 1

    def set_resources(self):
        self.namespace == "prod" or self.resources.update({
            "requests": {
                "cpu": "1000m",
                "memory": "1000Mi",
            },
            "limits": {
                "cpu": "1000m",
                "memory": "1000Mi",
            }
        })

    def set_envs(self):
        self.env.update({
            "SPRING_PROFILES_ACTIVE": "prod" if "prod" == self.namespace else "test",
            "JVM_HEAP_MIN": "350M" if "prod" == self.namespace else "150M",
            "JVM_HEAP_MAX": "700M" if "prod" == self.namespace else "300M",
        })

    # Overriding the default method
    def populate_ingress(self, sub_domain):
        hosts = [f'{self.serviceName}{"-dev" if self.namespace != "prod" else ""}.{domain}' for domain in self.domains]
        hosts.extend([f'{self.serviceName}.{sub_domain}.{domain}' for domain in self.domains])
        tls = [{'secreteName': self.tlsSecrets[self.extract_domain(host)], 'hosts': [host]} for host in
               list(filter(lambda host: "k8s" not in host, hosts))]

        return {'hosts': hosts, 'tls': tls}
