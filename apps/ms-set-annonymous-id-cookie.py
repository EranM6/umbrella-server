from objs.microService import MicroService


class Ms_set_annonymous_id_cookie(MicroService):
    domains = ['haaretz.co.il']
    replicaCount = None

    def __init__(self, service_name, namespace):
        super().__init__(service_name, namespace)

    def set_envs(self):
        self.env.update({
            "APP_PROFILE": "prod" if "prod" == self.namespace else "dev",
        })

    # Overriding the default method
    def populate_ingress(self, sub_domain):
        hosts = [f'{self.serviceName}{"-dev" if self.namespace != "prod" else ""}.{domain}' for domain in
                 self.domains]

        hosts.extend([f'{self.serviceName}.{sub_domain}.{domain}' for domain in self.domains])

        return {'hosts': hosts}
