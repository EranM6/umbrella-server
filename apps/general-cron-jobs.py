from objs.microService import MicroService


class General_cron_jobs(MicroService):
    def __init__(self, service_name, namespace):
        super().__init__(service_name, namespace)
        self.replicaCount = None if namespace == "prod" else 1

    def set_resources(self):
        self.namespace == "prod" or self.resources.update({
            "requests": {
                "cpu": "750m",
                "memory": "2800Mi",
            },
            "limits": {
                "cpu": "1000m",
                "memory": "2800Mi",
            }
        })

    def set_envs(self):
        self.env.update({
            "SPRING_PROFILES_ACTIVE": "prod" if "prod" == self.namespace else "test",
            "JVM_HEAP_MIN": "350M",
            "JVM_HEAP_MAX": "2800M",
            "GOOGLE_APPLICATION_CREDENTIALS": "/pubsub-secrets/pubsub-creds.json",
            "ANDROID_CREDS": "/android-secrets/android_credentials.p12",
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
                    "name": "mongo-creds-ms-purchase" if self.namespace == "prod" else "legacy-oracle-mongo",
                    "key": "user"
                }
            },
            "MONGO_PASS": {
                "secretKeyRef": {
                    "name": "mongo-creds-ms-purchase" if self.namespace == "prod" else "legacy-oracle-mongo",
                    "key": "password"
                }
            },
        })
        "prod" == self.namespace and self.env.update({"FASTLY_ACCESS_TOKEN": "uDjL-gAn5SSO8h63u1CLgCN-glyTfAvP"})

    # Overriding the default method
    def populate_ingress(self, sub_domain):
        hosts = [f'{self.serviceName}{"-dev" if self.namespace != "prod" else ""}.{domain}' for domain in self.domains]
        hosts.extend([f'{self.serviceName}.{sub_domain}.{domain}' for domain in self.domains])
        tls = [{'secreteName': self.tlsSecrets[self.extract_domain(host)], 'hosts': [host]} for host in
               list(filter(lambda host: "k8s" not in host, hosts))]

        return {'hosts': hosts, 'tls': tls}
