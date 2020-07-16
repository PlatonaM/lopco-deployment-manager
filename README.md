#### /workers

**POST**

_Create worker instance._

    # Example
    
    cat instance_data.json
    {
        "id": "1567e155-51c6-4f0b-a898-842c737f1b34",
        "name": "Convert xlsx to csv",
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
    -d @instance_data.json \
    -H 'Content-Type: application/json' \
    -X POST http://host:8000/worker-manager/workers
    9bef20b955ba4869a278b2f075c99260

----

#### /workers/{worker}

**DELETE**

_Stop and remove worker instance._

    # Example
    
    curl -X DELETE http://host:8000/worker-manager/workers/9bef20b955ba4869a278b2f075c99260
