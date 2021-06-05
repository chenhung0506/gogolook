# Customized document

## Initial enviroment
pip install -r ./customized/module/requirements.txt

## Git struct
```
.
├── README.md
├── docker
│   ├── Dockerfile
│   ├── build.sh
│   ├── dev.env
│   ├── docker-compose.yaml
│   ├── run.sh
│   └── test.env
├── imgs
│   └── customized-b24bfb9-20201030190120.tar.gz
├── logs
└── module
    ├── const.py
    ├── controller.py
    ├── dao.py
    ├── data_for_KG
    ├── log.py
    ├── logs
    ├── requirements.txt
    ├── resource
    ├── server.py
    ├── service.py
    └── utils.py
```

## Deploy with run.sh
### step1:  customized*.tar.gz file
```gherkin=
tar zxvf customized-kgi-b785119-20201026.tar.gz
```
### step2: load image, and get image $tag
```gherkin=
docker load -i customized/imgs/customized-b785119-20201026193411.tar.gz
```
### step3: execute run.sh
```gherkin=
./customized/docker/run.sh 3
```
### step4: enter $tag
```gherkin=
Enter TAG: b785119
```

## Deploy with docker-compose.yaml

```gherkin=
export ENV=dev.env TAG=529d578 PORT=8330 && \
docker-compose up   
```

## Deploy with docker run
```gherkin=
export ENV=dev.env TAG=529d578 PORT=8330 && \
docker run -d --name customized -v ~/volumes/customized:/usr/src/app/logs -v ~/.ssh/known_hosts:/root/.ssh/known_hosts -v ~/etc/timezone:/etc/localtime:ro -m 5125m --restart always --net docker-compose-base_default -e TZ=Asia/Taipei -p ${PORT}:${PORT} --env-file ${ENV} chenhung0506/customized:${TAG}
```

# Coding Exercise

Implement a Restful task list API as well as run this application in container.

- Spec
  - Fields of task:
      - name
          - Type: String
      - status
          - Type: Bool
          - Value
              - 0=Incomplete
              - 1=Complete
  - Reponse headers
      - Content-Type=application/json
  - Unit Test
  - DB migration strategy
  - Manage code base on Github

- Runtime Environment Requirement
    - Python 3.7
    - Flask 1.1
    - uWSGI LTS
    - MySQL 8.0.23 (Docker Image: mysql/mysql-server:8.0.23)
    - nginx 1.19.5
    - Ubuntu 18.04
    - Docker


### 1.  GET /tasks (list tasks)
```
{
    "result": [
        {"id": 1, "name": "name", "status": 0}
    ]
}
```

### 2.  POST /task  (create task)
```
request
{
  "name": "買晚餐"
}

response status code 201
{
    "result": {"name": "買晚餐", "status": 0, "id": 1}
}
```

### 3. PUT /task/<id> (update task)
```
request
{
  "name": "買早餐",
  "status": 1
  "id": 1
}

response status code 200
{
  "name": "買早餐",
  "status": 1,
  "id": 1
}
```

### 4. DELETE /task/<id> (delete task)
response status code 200
