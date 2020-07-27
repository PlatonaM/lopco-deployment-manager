#### /deployments

**POST**

_Create worker instance._

    # Example
    
    cat worker_data.json
    {
        "type": "worker",
        "id": "1567e155-51c6-4f0b-a898-842c737f1b34",
        "image": "xlsx-to-csv-worker",
        "data_cache_path": "/data_cache",
        "configs": {
            "delimiter": ";",
            "JOB_CALLBACK_URL": "http://job-manager/jobs/UVpxMTeqgMijLlbmNI8A_A"
        },
        "inputs": {
            "xlsx_file": "3f8b39c0a3ef42c0ae18e34af8fdce96"
        }
    }
    
    curl \
    -d @worker_data.json \
    -H 'Content-Type: application/json' \
    -X POST http://host:8000/deployment-manager/deployments
    9bef20b955ba4869a278b2f075c99260


_Create Protocol-Adapter instance._

    cat pa_data.json
    {
        "type": "protocol-adapter",
        "id": "5e674298-49d5-4723-926c-cf062dd9c141",
        "image": "http-adapter",
        "data_cache_path": "/data_cache",
        "configs": {
            "CONF_LOGGER_LEVEL": "debug"
        },
        "ports": {
            "80": {
                "protocol": "tcp",
                "host_interface": null,
                "host_ports": 7000
            }
        }
    }
    
    curl \
    -d @pa_data.json \
    -H 'Content-Type: application/json' \
    -X POST http://host:8000/deployment-manager/deployments
    5e674298-49d5-4723-926c-cf062dd9c141

----

#### /deployments/{deployment}

**DELETE**

_Stop and remove instance._

    # Example
    
    curl -X DELETE http://host:8000/deployment-manager/deployments/9bef20b955ba4869a278b2f075c99260
