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

__all__ = ("Deployments", "Deployment")


from . import model
from .logger import getLogger
from .docker import DockerAdapter, NotFound
from .configuration import conf
import falcon
import json
import uuid


logger = getLogger(__name__.split(".", 1)[-1])


def reqDebugLog(req):
    logger.debug("method='{}' path='{}' content_type='{}'".format(req.method, req.path, req.content_type))

def reqErrorLog(req, ex):
    logger.error("method='{}' path='{}' - {}".format(req.method, req.path, ex))


class BadRequest(Exception):
    pass


class Deployments:
    def __init__(self, docker_adapter: DockerAdapter):
        self.__docker_adapter = docker_adapter

    def on_get(self, req: falcon.request.Request, resp: falcon.response.Response):
        reqDebugLog(req)
        try:
            if req.params:
                if model.Deployment.type in req.params and req.params[model.Deployment.type] in model.DepTypes.__dict__.values():
                    items = self.__docker_adapter.listContainers(req.params[model.Deployment.type])
                else:
                    raise BadRequest("unknown parameters or values - {}".format(req.params))
            else:
                items = self.__docker_adapter.listContainers()
            resp.content_type = falcon.MEDIA_JSON
            resp.body = json.dumps(items)
            resp.status = falcon.HTTP_200
        except BadRequest as ex:
            resp.status = falcon.HTTP_400
            reqErrorLog(req, ex)
        except NotFound as ex:
            resp.status = falcon.HTTP_404
            reqErrorLog(req, ex)
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)

    def on_post(self, req: falcon.request.Request, resp: falcon.response.Response):
        reqDebugLog(req)
        try:
            data = json.load(req.bounded_stream)
            if data[model.Deployment.type] == model.DepTypes.worker:
                resp.body = self.__docker_adapter.startContainer(
                    name=str(uuid.uuid4()),
                    dep_data=data,
                    restart=False,
                    remove=not conf.Docker.disable_rm
                )
            elif data[model.Deployment.type] == model.DepTypes.protocol_adapter:
                resp.body = self.__docker_adapter.startContainer(name=data[model.Deployment.id], dep_data=data)
            else:
                raise Exception("unknown deployment type '{}'".format(data[model.Deployment.type]))
            resp.status = falcon.HTTP_200
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)


class Deployment:
    def __init__(self, docker_adapter: DockerAdapter):
        self.__docker_adapter = docker_adapter

    def on_get(self, req: falcon.request.Request, resp: falcon.response.Response, deployment):
        reqDebugLog(req)
        try:
            resp.content_type = falcon.MEDIA_JSON
            resp.body = json.dumps(self.__docker_adapter.getContainer(deployment))
            resp.status = falcon.HTTP_200
        except NotFound as ex:
            resp.status = falcon.HTTP_404
            reqErrorLog(req, ex)
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)

    def on_delete(self, req: falcon.request.Request, resp: falcon.response.Response, deployment):
        reqDebugLog(req)
        try:
            self.__docker_adapter.stopContainer(deployment)
            self.__docker_adapter.removeContainer(deployment)
            resp.status = falcon.HTTP_200
        except NotFound as ex:
            resp.status = falcon.HTTP_404
            reqErrorLog(req, ex)
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)
