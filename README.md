#### /deployments

**GET**

_List all deployed containers._

    # Example
    
    curl http://<host>/deployments
    {
        "job-manager": {
            "id": "b7166a134849b1198efefa62cb90c0a76652822c1e7ae89555ea3e9cbf76c363",
            "labels": {
                "lopco-type": "core"
            },
            "status": "running",
            "image": {
                "name": "platonam/lopco-job-manager:dev",
                "hash": "sha256:bd8ab66deeedd123fbe718780f92afd75f7beecb88a9fcdcde700fc99c03a9c4"
            },
            "ports": {
                "80/tcp": null
            },
            "created": "2020-11-20T08:35:45.978139375Z",
            "started": "2020-11-20T08:35:46.58210553Z",
            "restarts": 0,
            "environment": {
                "CONF_LOGGER_LEVEL": "debug",
                "CONF_JOBS_CHECK": "5",
                "CONF_JOBS_MAX_NUM": "10",
                "PATH": "/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                "LANG": "C.UTF-8",
                "GPG_KEY": "E3FF2839C048B25C084DEBE9B26995E310250568",
                "PYTHON_VERSION": "3.9.0",
                "PYTHON_PIP_VERSION": "20.2.4",
                "PYTHON_GET_PIP_URL": "https://github.com/pypa/get-pip/raw/fa7dc83944936bf09a0e4cb5d5ec852c0d256599/get-pip.py",
                "PYTHON_GET_PIP_SHA256": "6e0bb0a2c2533361d7f297ed547237caf1b7507f197835974c0dd7eba998c53c"
            }
        },
        "worker-registry": {
            "id": "1b7df68b5109191bbc3a0e3e2ec45b3f17c51b978c1fc091d86dd4f133805e52",
            "labels": {
                "lopco-type": "core"
            },
            "status": "running",
            "image": {
                "name": "platonam/lopco-worker-registry:latest",
                "hash": "sha256:894d25b7c1b0a5d08b7daa2b4abf828604097f629ff5743366daa9f0155c7ccc"
            },
            "ports": {
                "80/tcp": null
            },
            "created": "2020-11-06T13:42:21.410806221Z",
            "started": "2020-11-20T06:55:44.392396251Z",
            "restarts": 0,
            "environment": {
                "CRUDCONF_LOGGER_NAME": "worker-registry",
                "CRUDCONF_LOGGER_LEVEL": "debug",
                "CRUDCONF_ENDPOINT_NAME": "workers",
                "CRUDCONF_ENDPOINT_ALLOW_POST": "True",
                "CRUDCONF_ENDPOINT_FULL_COLLECTION": "True",
                "PATH": "/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                "LANG": "C.UTF-8",
                "GPG_KEY": "E3FF2839C048B25C084DEBE9B26995E310250568",
                "PYTHON_VERSION": "3.9.0",
                "PYTHON_PIP_VERSION": "20.2.4",
                "PYTHON_GET_PIP_URL": "https://github.com/pypa/get-pip/raw/8283828b8fd6f1783daf55a765384e6d8d2c5014/get-pip.py",
                "PYTHON_GET_PIP_SHA256": "2250ab0a7e70f6fd22b955493f7f5cf1ea53e70b584a84a32573644a045b4bfb"
            }
        },
        "89cc5a01-b43a-44ef-b169-6c855eebec07": {
            "id": "a5175320feab2531446bd64b4cb3a0929c72e7bfeff2fa315532e330ed0eedb1",
            "labels": {
                "lopco-id": "5e674298-49d5-4723-926c-cf062dd9c141",
                "lopco-type": "protocol-adapter"
            },
            "status": "running",
            "image": {
                "name": "platonam/lopco-http-protocol-adapter:dev",
                "hash": "sha256:468023a2f3483d1a1958a0715f4a5d1458f70bbb52857db77100a7aaa0f1a00b"
            },
            "ports": {
                "80/tcp": {
                    "host_interface": "0.0.0.0",
                    "host_ports": 7000
                }
            },
            "created": "2020-10-30T13:27:06.055525871Z",
            "started": "2020-11-20T06:55:43.224454185Z",
            "restarts": 0,
            "environment": {
                "DEP_INSTANCE": "89cc5a01-b43a-44ef-b169-6c855eebec07",
                "CONF_LOGGER_LEVEL": "debug",
                "PATH": "/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                "LANG": "C.UTF-8",
                "GPG_KEY": "E3FF2839C048B25C084DEBE9B26995E310250568",
                "PYTHON_VERSION": "3.9.0",
                "PYTHON_PIP_VERSION": "20.2.4",
                "PYTHON_GET_PIP_URL": "https://github.com/pypa/get-pip/raw/8283828b8fd6f1783daf55a765384e6d8d2c5014/get-pip.py",
                "PYTHON_GET_PIP_SHA256": "2250ab0a7e70f6fd22b955493f7f5cf1ea53e70b584a84a32573644a045b4bfb"
            }
        }
    }

_List only core services._

    # Example
    
    curl http://<host>/deployments?type=core
    {
        ...
    }
    
_List only workers._

    # Example
    
    curl http://<host>/deployments?type=worker
    {
        ...
    }

_List only protocol-adapters._

    # Example
    
    curl http://<host>/deployments?type=protocol-adapter
    {
        ...
    }

**POST**

_Deploy worker._

    # Example
    
    cat worker_data.json
    {
        "id": "004894dc-bb03-4649-92c4-6b184c30c594",
        "name": "Split CSV",
        "image": "platonam/lopco-split-csv-worker:dev",
        "data_cache_path": "/data_cache",
        "configs": {
            "column": "sensor",
            "delimiter": ";",
            "DS_PLATFORM_ID": "device:aeb83bf0-c50c-48e9-91b6-4db07c65c99c",
            "DS_PLATFORM_TYPE_ID": "device-type:c5940477-afe5-493c-9a9e-8043f8de7acd",
            "JOB_CALLBACK_URL": "http://job-manager/jobs/0d-bTcQEwCwG_zcdBDuIGA"
        },
        "inputs": {
            "source_table": "62087365f3694acf8ea1ab1c22441a01"
        },
        "type": "worker"
    }
    
    curl \
    -d @worker_data.json \
    -H 'Content-Type: application/json' \
    -X POST http://<host>/deployments
    9bef20b955ba4869a278b2f075c99260


_Deploy Protocol-Adapter._

    # Example

    cat pa_data.json
    {
        "id": "5e674298-49d5-4723-926c-cf062dd9c141",
        "image": "platonam/lopco-http-protocol-adapter:dev",
        "data_cache_path": "/data_cache",
        "configs": {
            "CONF_LOGGER_LEVEL": "info"
        },
        "ports": {
            "80/tcp": {
                "host_interface": null,
                "host_ports": 6000
            }
        },
        "type": "protocol-adapter"
    }
    
    curl \
    -d @pa_data.json \
    -H 'Content-Type: application/json' \
    -X POST http://<host>/deployments
    5e674298-49d5-4723-926c-cf062dd9c141

----

#### /deployments/{deployment}

**GET**

_Get container info._

    # Example
    
    curl http://<host>/deployments/gui
    {
        "id": "5253818179a856e280ea503ab5e8faeff7ab75bbd58ad17aa57e429c436d2e35",
        "labels": {
            "lopco-type": "core"
        },
        "status": "running",
        "image": {
            "name": "platonam/lopco-gui:dev",
            "hash": "sha256:3793a1ab3561761aee1c452c9bb842a45bd0911faf091cdde595c4588d20bc63"
        },
        "ports": {
            "80/tcp": {
                "host_interface": "0.0.0.0",
                "host_ports": 8080
            }
        },
        "created": "2020-11-10T05:50:56.882284941Z",
        "started": "2020-11-20T06:55:43.796005849Z",
        "restarts": 0,
        "environment": {
            "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
        }
    }

**PATCH**

_Start / Stop container._

    # Example

    cat dep_state.json
    {
        "status": "stopped"
    }

    curl \
    -d @dep_state.json \
    -H 'Content-Type: application/json' \
    -X PATCH http://<host>/deployments/5e674298-49d5-4723-926c-cf062dd9c141

**DELETE**

_Stop and remove container._

    # Example
    
    curl -X DELETE http://<host>/deployments/9bef20b955ba4869a278b2f075c99260

---

#### /deployments/{deployment}/log

**GET**

_Get complete log._

    # Example
    
    curl http://<host>/deployments/job-manager/log
    11.20.2020 09:55:20 AM - DEBUG: [job-manager.api] method='POST' path='/jobs' content_type='application/json'
    11.20.2020 09:55:20 AM - INFO: [job-manager.api] new job '0d-bTcQEwCwG_zcdBDuIGA'
    11.20.2020 09:55:20 AM - INFO: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: starting ...
    11.20.2020 09:55:21 AM - INFO: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: executing stage '0' of pipeline '677f99d4-2ec7-450c-add2-8b7c5f7f171c'
    11.20.2020 09:55:21 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: waiting for worker 'd23a8d1f-0b3f-4df8-b877-e70790b873ef'
    11.20.2020 09:55:24 AM - DEBUG: [job-manager.api] method='POST' path='/jobs/0d-bTcQEwCwG_zcdBDuIGA' content_type='application/json'
    11.20.2020 09:55:24 AM - INFO: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: executing stage '1' of pipeline '677f99d4-2ec7-450c-add2-8b7c5f7f171c'
    11.20.2020 09:55:25 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: waiting for worker '124bc2ff-558b-48e0-8463-68e9e25cf7a3'
    11.20.2020 09:55:25 AM - DEBUG: [job-manager.api] method='POST' path='/jobs/0d-bTcQEwCwG_zcdBDuIGA' content_type='application/json'
    11.20.2020 09:55:25 AM - INFO: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: executing stage '2' of pipeline '677f99d4-2ec7-450c-add2-8b7c5f7f171c'
    11.20.2020 09:55:25 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: waiting for worker '50a9a0e1-945b-49e7-ad0e-331d62dbcead'
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.api] method='POST' path='/jobs/0d-bTcQEwCwG_zcdBDuIGA' content_type='application/json'
    11.20.2020 09:55:26 AM - INFO: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: finished
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '8f124c499a314646a23addc397b3a93d' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '62087365f3694acf8ea1ab1c22441a01' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '0c61e7d655994a178e78d11fd814eb64' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '6745e87dfc0b4c9f98f7fa0752a48757' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '9cb2777ed3da42ef9f9d71569f434888' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file 'fb03083282dd42528a5fbda6fe6b58ea' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '85957dd8f4474f658a2a5a0e886569c2' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '7e2910a48ba94b83bc32923b28415092' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '8b30ba0c7f68414aaac304ce9e9a4d88' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file 'd618e2f2b2a345e59476429958db1cd1' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file 'e99cdd4c8a294a2dacc107928eeff6e3' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '847e8893d6c142b78a59c4cc52922c5e' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file 'bebe2beecc974e0c9b2d5d9d8990196b' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file 'abb2b039b884420d8f56e2965ba5340a' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '2b02f65a78b24f2da8fadf3b4853c9b9' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '7e59520dc6424a8baa2b25662131138d' from data-cache

_Get last x lines._

    # Example
    
    curl http://<host>/deployments/job-manager/log?lines=5
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '847e8893d6c142b78a59c4cc52922c5e' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file 'bebe2beecc974e0c9b2d5d9d8990196b' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file 'abb2b039b884420d8f56e2965ba5340a' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '2b02f65a78b24f2da8fadf3b4853c9b9' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '7e59520dc6424a8baa2b25662131138d' from data-cache

_Get all lines since a specified time._

    # Example
    
    curl http://<host>/deployments/job-manager/log?since=2020-11-20T9:55:26Z
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.api] method='POST' path='/jobs/0d-bTcQEwCwG_zcdBDuIGA' content_type='application/json'
    11.20.2020 09:55:26 AM - INFO: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: finished
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '8f124c499a314646a23addc397b3a93d' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '62087365f3694acf8ea1ab1c22441a01' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '0c61e7d655994a178e78d11fd814eb64' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '6745e87dfc0b4c9f98f7fa0752a48757' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '9cb2777ed3da42ef9f9d71569f434888' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file 'fb03083282dd42528a5fbda6fe6b58ea' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '85957dd8f4474f658a2a5a0e886569c2' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '7e2910a48ba94b83bc32923b28415092' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '8b30ba0c7f68414aaac304ce9e9a4d88' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file 'd618e2f2b2a345e59476429958db1cd1' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file 'e99cdd4c8a294a2dacc107928eeff6e3' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '847e8893d6c142b78a59c4cc52922c5e' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file 'bebe2beecc974e0c9b2d5d9d8990196b' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file 'abb2b039b884420d8f56e2965ba5340a' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '2b02f65a78b24f2da8fadf3b4853c9b9' from data-cache
    11.20.2020 09:55:26 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: removed file '7e59520dc6424a8baa2b25662131138d' from data-cache

_Get all lines up until a specified time._

    # Example
    
    curl http://<host>/deployments/job-manager/log?until=2020-11-20T9:55:26Z
    11.20.2020 09:55:20 AM - DEBUG: [job-manager.api] method='POST' path='/jobs' content_type='application/json'
    11.20.2020 09:55:20 AM - INFO: [job-manager.api] new job '0d-bTcQEwCwG_zcdBDuIGA'
    11.20.2020 09:55:20 AM - INFO: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: starting ...
    11.20.2020 09:55:21 AM - INFO: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: executing stage '0' of pipeline '677f99d4-2ec7-450c-add2-8b7c5f7f171c'
    11.20.2020 09:55:21 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: waiting for worker 'd23a8d1f-0b3f-4df8-b877-e70790b873ef'
    11.20.2020 09:55:24 AM - DEBUG: [job-manager.api] method='POST' path='/jobs/0d-bTcQEwCwG_zcdBDuIGA' content_type='application/json'
    11.20.2020 09:55:24 AM - INFO: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: executing stage '1' of pipeline '677f99d4-2ec7-450c-add2-8b7c5f7f171c'
    11.20.2020 09:55:25 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: waiting for worker '124bc2ff-558b-48e0-8463-68e9e25cf7a3'
    11.20.2020 09:55:25 AM - DEBUG: [job-manager.api] method='POST' path='/jobs/0d-bTcQEwCwG_zcdBDuIGA' content_type='application/json'
    11.20.2020 09:55:25 AM - INFO: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: executing stage '2' of pipeline '677f99d4-2ec7-450c-add2-8b7c5f7f171c'
    11.20.2020 09:55:25 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: waiting for worker '50a9a0e1-945b-49e7-ad0e-331d62dbcead'

_Get all lines since a specified time up until a specified time._

    # Example
    
    curl http://<host>/deployments/job-manager/log?since=2020-11-20T9:55:20Z&until=2020-11-20T9:55:24Z
    11.20.2020 09:55:20 AM - DEBUG: [job-manager.api] method='POST' path='/jobs' content_type='application/json'
    11.20.2020 09:55:20 AM - INFO: [job-manager.api] new job '0d-bTcQEwCwG_zcdBDuIGA'
    11.20.2020 09:55:20 AM - INFO: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: starting ...
    11.20.2020 09:55:21 AM - INFO: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: executing stage '0' of pipeline '677f99d4-2ec7-450c-add2-8b7c5f7f171c'
    11.20.2020 09:55:21 AM - DEBUG: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: waiting for worker 'd23a8d1f-0b3f-4df8-b877-e70790b873ef'
    11.20.2020 09:55:24 AM - DEBUG: [job-manager.api] method='POST' path='/jobs/0d-bTcQEwCwG_zcdBDuIGA' content_type='application/json'
    11.20.2020 09:55:24 AM - INFO: [job-manager.jobs] 0d-bTcQEwCwG_zcdBDuIGA: executing stage '1' of pipeline '677f99d4-2ec7-450c-add2-8b7c5f7f171c'

---

#### /images

**GET**

_List all images._

    # Example
    
    curl http://<host>/images
    {
        "platonam/lopco-job-manager:dev": {
            "hash": "sha256:bd8ab66deeedd123fbe718780f92afd75f7beecb88a9fcdcde700fc99c03a9c4",
            "created": "2020-11-20T08:24:37.922371263Z",
            "size": 74176809,
            "architecture": "amd64",
            "digests": [
                "platonam/lopco-job-manager@sha256:4a3df99c3d49cdcbe4313fa0d62d86d622049c66d01b567f244b21f216d6fbad"
            ]
        },
        "platonam/lopco-gui:dev": {
            "hash": "sha256:3793a1ab3561761aee1c452c9bb842a45bd0911faf091cdde595c4588d20bc63",
            "created": "2020-11-09T11:06:22.951522252Z",
            "size": 15503091,
            "architecture": "amd64",
            "digests": [
                "platonam/lopco-gui@sha256:7d145e02b69376242f33116e08de615e202d179d82495bc73a80cf04e45397b7"
            ]
        },
        "platonam/lopco-backup-manager:dev": {
            "hash": "sha256:54d3c41f761071086509244a736e96558837f934f0e366f31894a4a6f91487e8",
            "created": "2020-11-09T09:54:10.891845989Z",
            "size": 84639725,
            "architecture": "amd64",
            "digests": []
        },
        "platonam/lopco-update-manager:dev": {
            "hash": "sha256:d637912c6086e7e395fb5afb7528b42c4209f27d4f98e5faca4caf0d2b933831",
            "created": "2020-11-05T08:14:12.058982021Z",
            "size": 73340541,
            "architecture": "amd64",
            "digests": [
                "platonam/lopco-update-manager@sha256:1935815e550682ab1bfce12a4766b6923ada09d2870d50d4e3ae55ed18a499e7"
            ]
        },
        "platonam/lopco-protocol-adapter-registry:latest": {
            "hash": "sha256:65b23b4e5572aadb5b09a47face867dd461aecd401979e68962c367da1396254",
            "created": "2020-10-28T09:46:46.201170517Z",
            "size": 70240165,
            "architecture": "amd64",
            "digests": [
                "platonam/lopco-protocol-adapter-registry@sha256:8b9f35cba78923919d0d5340fc81dd5c4dae4618fb3b42771a7cbb8bba6dd4a1"
            ]
        },
        "platonam/lopco-worker-registry:latest": {
            "hash": "sha256:894d25b7c1b0a5d08b7daa2b4abf828604097f629ff5743366daa9f0155c7ccc",
            "created": "2020-10-28T09:43:47.886766227Z",
            "size": 70240164,
            "architecture": "amd64",
            "digests": [
                "platonam/lopco-worker-registry@sha256:0dfb7ac8a4cc0900990462ff90e1ac65c67a706d46d37f1f8061fec3f765c123"
            ]
        },
        "platonam/lopco-pipeline-registry:latest": {
            "hash": "sha256:e57b5ab1074f396f1fcb1475f90451c4519d8541b1b5096813682fd36cf9075d",
            "created": "2020-10-28T09:40:46.742116136Z",
            "size": 70240161,
            "architecture": "amd64",
            "digests": [
                "platonam/lopco-pipeline-registry@sha256:d76a63df01124a115f316d6b726ec424526ce611961880abef1eb253261b4ce9"
            ]
        },
        "platonam/lopco-machine-registry:latest": {
            "hash": "sha256:ee6c1ecdbd37a22f264c044e7506de7011e403f2c9344ab20d2ac5a391eb6043",
            "created": "2020-10-28T09:37:36.750397114Z",
            "size": 70240106,
            "architecture": "amd64",
            "digests": [
                "platonam/lopco-machine-registry@sha256:57f2e1087c7d2cfa5d5e9973968c3347328a73c89b23fd3daf85e79579dec2cb"
            ]
        },
        "platonam/lopco-reverse-proxy:latest": {
            "hash": "sha256:dca44a002ad317bb995e11e9d410c18c93bbe2c1bd86face5ce6e78f769b79e5",
            "created": "2020-10-28T08:24:43.423635312Z",
            "size": 7482155,
            "architecture": "amd64",
            "digests": [
                "platonam/lopco-reverse-proxy@sha256:b3d3dc87f8ba40f4d76fdf7400b7f7dee42990e656aa8e6841f1fb5c028983da"
            ]
        },
        "platonam/lopco-http-protocol-adapter:dev": {
            "hash": "sha256:468023a2f3483d1a1958a0715f4a5d1458f70bbb52857db77100a7aaa0f1a00b",
            "created": "2020-10-21T09:51:16.833172002Z",
            "size": 75383418,
            "architecture": "amd64",
            "digests": [
                "platonam/lopco-http-protocol-adapter@sha256:243116eabd10c50e9bfef17a4f1496f6a9b2752c27e61db6ded3c68828bbf89d"
            ]
        },
        "platonam/lopco-split-csv-worker:dev": {
            "hash": "sha256:b88fafe4eeda1a1e107f0372817aa682546cb6c8a160223593142ab081c73835",
            "created": "2020-10-21T07:54:47.769547248Z",
            "size": 73687885,
            "architecture": "amd64",
            "digests": [
                "platonam/lopco-split-csv-worker@sha256:87cbab350a3f13c4a5a0ac5fa5452311f38ab35cfb3510204012b18b2df98bf1"
            ]
        },
        "platonam/lopco-deployment-manager:dev": {
            "hash": "sha256:54e1fbc91facd92380e5e89303a1d8e3185ca020050d47834bf5bf38c6ca98dc",
            "created": "2020-10-20T08:58:08.547733405Z",
            "size": 77355661,
            "architecture": "amd64",
            "digests": [
                "platonam/lopco-deployment-manager@sha256:14abdac557d633bff1e923710a8cf29ed30491bdd725f725b3732e85ec9dbe7f"
            ]
        },
        "platonam/lopco-xlsx-to-csv-worker:dev": {
            "hash": "sha256:8d4fbf0663283e3fa5f022fc588e2c16d56e089c4430c8342051b10d40628a1c",
            "created": "2020-10-20T05:38:03.380242403Z",
            "size": 91262006,
            "architecture": "amd64",
            "digests": [
                "platonam/lopco-xlsx-to-csv-worker@sha256:8735a0b8e926f2bbe0c7d0cb3517fe698a0f9ac5bddf5edbc47484db9c6b835c"
            ]
        },
        "platonam/lopco-trim-csv-worker:dev": {
            "hash": "sha256:d8b116bff702e9b4f2974ce1c64cd5249d7ee9f4a1e84ffbf03619479c7ad0fb",
            "created": "2020-10-20T05:26:19.566278723Z",
            "size": 10325139,
            "architecture": "amd64",
            "digests": [
                "platonam/lopco-trim-csv-worker@sha256:326991d20e53653bdd6e9b92084013a6e0255c0ade2de9609a40597d08a0ee26"
            ]
        }
    }

**POST**

_Pull image._

    # Example
    
    cat img_info.json
    {
        "repository": "platonam/lopco-deployment-manager",
        "tag": "dev"
    }
    
    curl \
    -d @img_info.json \
    -H 'Content-Type: application/json' \
    -X PATCH http://<host>/images

---

#### /images/{image}

**GET**

    # Example
    
    curl http://<host>/images/platonam%252Flopco-trim-csv-worker%253Adev
    {
        "hash": "sha256:d8b116bff702e9b4f2974ce1c64cd5249d7ee9f4a1e84ffbf03619479c7ad0fb",
        "created": "2020-10-20T05:26:19.566278723Z",
        "size": 10325139,
        "architecture": "amd64",
        "digests": [
            "platonam/lopco-trim-csv-worker@sha256:326991d20e53653bdd6e9b92084013a6e0255c0ade2de9609a40597d08a0ee26"
        ]
    }

---

#### /remote-digests/{image}

**GET**

    # Example
    
    curl http://<host>/remote-digests/platonam%252Flopco-trim-csv-worker%253Adev
    {
        "digest": "sha256:326991d20e53653bdd6e9b92084013a6e0255c0ade2de9609a40597d08a0ee26"
    }
