from objs.microService import MicroService


class Ms_gstat_campaign(MicroService):
    domains = ['haaretz.co.il']
    replicaCount = None

    def __init__(self, service_name, namespace):
        super().__init__(service_name, namespace)

    def set_envs(self):
        self.env.update({
            "SPRING_PROFILES_ACTIVE": "production" if "prod" == self.namespace else "stage",
            "JVM_HEAP_MIN": "350M",
            "JVM_HEAP_MAX": "750M",
            "GOOGLE_APPLICATION_CREDENTIALS": "/secrets/bigQuery-creds.json",
        })

    # Overriding the default method
    def populate_ingress(self, sub_domain):
        hosts = [f'{self.serviceName}{"-dev" if self.namespace != "prod" else ""}.{domain}' for domain in
                 self.domains]

        hosts.extend([f'{self.serviceName}.{sub_domain}.{domain}' for domain in self.domains])

        return {'hosts': hosts}
