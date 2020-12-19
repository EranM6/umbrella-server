from objs.microService import MicroService


class Ms_ip2country(MicroService):
    replicaCount = None

    def __init__(self, service_name, namespace):
        super().__init__(service_name, namespace)

    def set_envs(self):
        self.env.update({"POOL_SIZE": "1000" if "prod" == self.namespace else "500"})
