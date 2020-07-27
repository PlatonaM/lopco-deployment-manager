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


class DockerAdapter:
    def __init__(self):
        self.__client = docker.DockerClient(base_url=conf.Docker.socket)

    def __purgeImages(self):
        try:
            self.__client.images.prune(filters={"dangling": True})
        except Exception as ex:
            logger.error("can't remove images - {]".format(ex))

    def getContainer(self, c_name):
        try:
            container = self.__client.containers.get(c_name)
            return {
                "id": container.id,
                "labels": {key: value for key, value in container.labels.items() if "lopco" in key},
                "status": container.status,
                "image": {
                    "name": container.image.tags[-1] if container.image.tags else container.image.short_id.replace("sha256:", ""),
                    "hash": container.image.id
                }
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
                    "status": container.status,
                    "image": {
                        "name": container.image.tags[-1] if container.image.tags else container.image.short_id.replace("sha256:", ""),
                        "hash": container.image.id
                    }
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

    def startContainer(self, wrk_data: dict) -> str:
        try:
            try:
                self.__client.images.pull(repository=dep_data[model.Deployment.image])
            except Exception as ex:
                logger.warning("can't pull image for '{}' - {}".format(dep_data[model.Deployment.id], ex))
            params = dict()
            params["name"] = uuid.uuid4().hex
            params["labels"] = {
                "worker-id": wrk_data[model.Worker.id],
                "worker-name": wrk_data[model.Worker.name]
            }
            params["network"] = conf.Docker.network_name
            params["image"] = wrk_data[model.Worker.image]
            params["detach"] = True
            params["remove"] = conf.Docker.rm_container
            params["volumes"] = {conf.DataCache.volume_name: {"bind": wrk_data[model.Worker.data_cache_path], "mode": "rw"}}
            params["environment"] = {"WORKER_INSTANCE": params["name"]}
            if wrk_data.get(model.Worker.configs):
                params["environment"].update(wrk_data[model.Worker.configs])
            if wrk_data.get(model.Worker.inputs):
                params["environment"].update(wrk_data[model.Worker.inputs])
            params["environment"] = {"DEP_INSTANCE": params["name"]}
            self.__client.containers.run(**params)
            return params["name"]
        except Exception as ex:
            logger.error("can't create instance for '{}' - {}".format(wrk_data[model.Worker.id], ex))
            raise error_map.setdefault(ex, CEAdapterError)(ex)

    def removeContainer(self, name: str) -> None:
        try:
            container_obj = self.__client.containers.get(name)
            container_obj.remove()
            self.__purgeImages()
        except Exception as ex:
            logger.error("can't remove instance '{}' - {}".format(name, ex))
            raise error_map.setdefault(ex, CEAdapterError)(ex)
