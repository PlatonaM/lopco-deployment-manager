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

from manager.logger import initLogger
from manager.configuration import conf
from manager.docker import DockerAdapter
from manager import api
import falcon


initLogger(conf.Logger.level)

docker_adapter = DockerAdapter()

app = falcon.API()

app.req_options.strip_url_path_trailing_slash = True

routes = (
    ("/deployments", api.Deployments(docker_adapter)),
    ("/deployments/{deployment}", api.Deployment(docker_adapter)),
    ("/deployments/{deployment}/log", api.Log(docker_adapter)),
    ("/images", api.Images(docker_adapter)),
    ("/images/{image}", api.Image(docker_adapter)),
    ("/remote-digests/{image}", api.Digest(docker_adapter))
)

for route in routes:
    app.add_route(*route)

# gunicorn -b 0.0.0.0:8080 --workers 2 --threads 4 --worker-class gthread --log-level error app:app
