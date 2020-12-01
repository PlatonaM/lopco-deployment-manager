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
from .docker import DockerAdapter, NotFound, ImageNotFound, CEAdapterError
from .configuration import conf
import falcon
import json
import uuid
import datetime


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
                resp.body = self.__docker_adapter.runContainer(name=str(uuid.uuid4()), dep_data=data, restart=False)
            elif data[model.Deployment.type] == model.DepTypes.protocol_adapter:
                resp.body = self.__docker_adapter.runContainer(name=str(uuid.uuid4()), dep_data=data)
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

    def on_patch(self, req: falcon.request.Request, resp: falcon.response.Response, deployment):
        reqDebugLog(req)
        if not req.content_type == falcon.MEDIA_JSON:
            resp.status = falcon.HTTP_415
        else:
            try:
                data = json.load(req.bounded_stream)
                if data["status"] == "running":
                    self.__docker_adapter.startContainer(deployment)
                elif data["status"] == "stopped":
                    self.__docker_adapter.stopContainer(deployment)
                else:
                    raise ValueError("unknown status '{}'".format(data["status"]))
                resp.status = falcon.HTTP_200
            except KeyError as ex:
                resp.status = falcon.HTTP_400
                reqErrorLog(req, ex)
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
            try:
                self.__docker_adapter.removeContainer(deployment)
            except CEAdapterError:
                pass
            resp.status = falcon.HTTP_200
        except NotFound as ex:
            resp.status = falcon.HTTP_404
            reqErrorLog(req, ex)
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)


class Images:
    def __init__(self, docker_adapter: DockerAdapter):
        self.__docker_adapter = docker_adapter

    def on_get(self, req: falcon.request.Request, resp: falcon.response.Response):
        reqDebugLog(req)
        try:
            resp.content_type = falcon.MEDIA_JSON
            resp.body = json.dumps(self.__docker_adapter.listImages())
            resp.status = falcon.HTTP_200
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)

    def on_post(self, req: falcon.request.Request, resp: falcon.response.Response):
        reqDebugLog(req)
        try:
            data = json.load(req.bounded_stream)
            self.__docker_adapter.pullImage(data[model.Image.repository], data[model.Image.tag])
            resp.status = falcon.HTTP_200
        except KeyError as ex:
            resp.status = falcon.HTTP_400
            reqErrorLog(req, ex)
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)

    def on_patch(self, req: falcon.request.Request, resp: falcon.response.Response):
        reqDebugLog(req)
        try:
            self.__docker_adapter.pruneImages()
            resp.status = falcon.HTTP_200
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)


class Image:
    def __init__(self, docker_adapter: DockerAdapter):
        self.__docker_adapter = docker_adapter

    def on_get(self, req: falcon.request.Request, resp: falcon.response.Response, image):
        reqDebugLog(req)
        try:
            resp.content_type = falcon.MEDIA_JSON
            resp.body = json.dumps(self.__docker_adapter.getImage(falcon.uri.decode(image)))
            resp.status = falcon.HTTP_200
        except ImageNotFound as ex:
            resp.status = falcon.HTTP_404
            reqErrorLog(req, ex)
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)


class Digest:
    def __init__(self, docker_adapter: DockerAdapter):
        self.__docker_adapter = docker_adapter

    def on_get(self, req: falcon.request.Request, resp: falcon.response.Response, image):
        reqDebugLog(req)
        try:
            resp.content_type = falcon.MEDIA_JSON
            resp.body = json.dumps(self.__docker_adapter.getRegImageDigest(falcon.uri.decode(image)))
            resp.status = falcon.HTTP_200
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)


class Log:
    __abs_parameters = ("lines", )
    __rel_parameters = ("since", "until")

    def __init__(self, docker_adapter: DockerAdapter):
        self.__docker_adapter = docker_adapter

    def on_get(self, req: falcon.request.Request, resp: falcon.response.Response, deployment):
        reqDebugLog(req)
        try:
            if req.params:
                params = req.params.copy()
                if set(params).issubset(self.__rel_parameters):
                    utc_tstp_format = "%Y-%m-%dT%H:%M:%SZ"
                    for key in params:
                        params[key] = int(datetime.datetime.strptime(params[key], utc_tstp_format).replace(tzinfo=datetime.timezone.utc).timestamp())
                    resp.body = self.__docker_adapter.getRelative(deployment, **params)
                elif set(params).issubset(self.__abs_parameters):
                    for key in params:
                        params[key] = int(params[key])
                    resp.body = self.__docker_adapter.getAbsolut(deployment, **params)
                else:
                    raise TypeError("unknown arguments")
            else:
                resp.body = self.__docker_adapter.getRelative(deployment)
            resp.content_type = falcon.MEDIA_TEXT
            resp.status = falcon.HTTP_200
        except TypeError as ex:
            resp.status = falcon.HTTP_400
            reqErrorLog(req, ex)
        except ValueError as ex:
            resp.status = falcon.HTTP_400
            reqErrorLog(req, ex)
        except NotFound as ex:
            resp.status = falcon.HTTP_404
            reqErrorLog(req, ex)
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)
