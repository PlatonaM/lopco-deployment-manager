"""
   Copyright 2020 InfAI (CC SES)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


__all__ = ("DockerAdapter", )


from . import model
from .logger import getLogger
from .configuration import conf
import docker
import docker.errors
import docker.types


logger = getLogger(__name__.split(".", 1)[-1])


class CEAdapterError(Exception):
    pass


class EngineAPIError(CEAdapterError):
    pass


class NotFound(CEAdapterError):
    pass


class ImageNotFound(CEAdapterError):
    pass


error_map = {
    docker.errors.APIError: EngineAPIError,
    docker.errors.NotFound: NotFound,
    docker.errors.ImageNotFound: ImageNotFound
}

container_state_map = {
    "created": "stopped",
    "restarting": "running",
    "running": "running",
    "removing": "running",
    "paused": "stopped",
    "exited": "stopped",
    "dead": "stopped"
}


class DockerAdapter:
    def __init__(self):
        self.__client = docker.DockerClient(base_url=conf.Docker.socket)

    def __purgeImages(self):
        try:
            self.__client.images.prune(filters={"dangling": True})
        except Exception as ex:
            logger.error("can't remove images - {]".format(ex))

    def __parsePortMappings(self, port_mappings: dict):
        mapping = dict()
        for c_port, h_ports in port_mappings.items():
            mapping[c_port] = {
                "host_interface": h_ports[-1]["HostIp"],
                "host_ports": [int(h_port["HostPort"]) for h_port in h_ports] if len(h_ports) > 1 else int(h_ports[-1]["HostPort"])
            } if h_ports else None
        return mapping

    def getContainer(self, c_name):
        try:
            container = self.__client.containers.get(c_name)
            return {
                "id": container.id,
                "labels": {key: value for key, value in container.labels.items() if "lopco" in key},
                "status": container_state_map[container.status],
                "image": {
                    "name": container.image.tags[-1] if container.image.tags else container.image.short_id.replace("sha256:", ""),
                    "hash": container.image.id
                },
                "ports": self.__parsePortMappings(container.ports) if container.ports else None
            }
        except Exception as ex:
            logger.error("can't get instance '{}' - {}".format(c_name, ex))
            raise error_map.setdefault(ex, CEAdapterError)(ex)

    def listContainers(self, type=None) -> dict:
        try:
            if not type:
                container_objs = self.__client.containers.list(all=True, filters={"label": "lopco-type"})
            else:
                container_objs = self.__client.containers.list(all=True, filters={"label": "lopco-type={}".format(type)})
            deployments = dict()
            for container in container_objs:
                deployments[container.name] = {
                    "id": container.id,
                    "labels": {key: value for key, value in container.labels.items() if "lopco" in key},
                    "status": container_state_map[container.status],
                    "image": {
                        "name": container.image.tags[-1] if container.image.tags else container.image.short_id.replace("sha256:", ""),
                        "hash": container.image.id
                    },
                    "ports": self.__parsePortMappings(container.ports) if container.ports else None
                }
            return deployments
        except Exception as ex:
            logger.error("can't list instances - {}".format(ex))
            raise error_map.setdefault(ex, CEAdapterError)(ex)

    def stopContainer(self, name: str) -> None:
        try:
            container_obj = self.__client.containers.get(name)
            container_obj.stop()
            container_obj.wait()
        except Exception as ex:
            logger.error("can't stop instance '{}' - {}".format(name, ex))
            raise error_map.setdefault(ex, CEAdapterError)(ex)

    def runContainer(self, name, dep_data: dict, restart: bool = True, remove: bool = False) -> str:
        try:
            try:
                self.__client.images.pull(repository=dep_data[model.Deployment.image])
            except Exception as ex:
                logger.warning("can't pull image for '{}' - {}".format(dep_data[model.Deployment.id], ex))
            params = dict()
            params["name"] = name
            params["labels"] = {
                "lopco-type": dep_data[model.Deployment.type],
                "lopco-id": dep_data[model.Deployment.id]
            }
            params["network"] = conf.Docker.network_name
            params["image"] = dep_data[model.Deployment.image]
            params["detach"] = True
            params["remove"] = remove
            params["volumes"] = {conf.DataCache.volume_name: {"bind": dep_data[model.Deployment.data_cache_path], "mode": "rw"}}
            params["environment"] = {"DEP_INSTANCE": params["name"]}
            if dep_data.get(model.Deployment.configs):
                params["environment"].update(dep_data[model.Deployment.configs])
            if dep_data.get(model.Worker.inputs):
                params["environment"].update(dep_data[model.Worker.inputs])
            if dep_data.get(model.ProtocolAdapter.ports):
                params["ports"] = {port: (val[model.Port.host_interface], val[model.Port.host_ports]) if val.get(model.Port.host_interface) else val[model.Port.host_ports] for port, val in dep_data[model.ProtocolAdapter.ports].items()}
            if restart:
                params["restart_policy"] = {"name": "always"}
            self.__client.containers.run(**params)
            return params["name"]
        except Exception as ex:
            logger.error("can't create instance for '{}' - {}".format(dep_data[model.Deployment.id], ex))
            raise error_map.setdefault(ex, CEAdapterError)(ex)

    def removeContainer(self, name: str) -> None:
        try:
            container_obj = self.__client.containers.get(name)
            container_obj.remove()
            self.__purgeImages()
        except Exception as ex:
            logger.error("can't remove instance '{}' - {}".format(name, ex))
            raise error_map.setdefault(ex, CEAdapterError)(ex)
