# Customized document

## Initial enviroment
pip install -r ./gogolook/module/requirements.txt

## Git struct
```
.
├── README.md
├── docker
│   ├── Dockerfile
│   ├── build.sh
│   ├── dev.env
│   ├── docker-compose.yaml
│   └── run.sh
├── imgs
└── module
    ├── __pycache__
    ├── callApiUtils.py
    ├── const.py
    ├── controller.py
    ├── daoGogolook.py
    ├── daoMigrate.py
    ├── log.py
    ├── logs
    ├── migrate
    ├── migrate.sql
    ├── requirements.txt
    ├── server.py
    ├── unitTest
    └── utils.py

```


## Deploy with harbor image
### step1: init mysql db
```
cd ./gogolook/docker && ./run.sh 0
```
### step2: harbor login with account / password
```
docker login harbor.chlin.tk 
```
### step3: execute run.sh
```
./run.sh 3 -v
```

## Deploy with docker build and run 
### step1: init mysql db
```
cd ./gogolook/docker && ./run.sh 0
```
### step2: excute docker build and run
```
./run.sh 1
```


## Test API
```
 curl -XGET localhost/tasks | jq
 curl -XPOST  localhost/tasks -H 'content-type: application/json' -d '{"name": "買晚餐"}' | jq 
 curl -XPUT  localhost/tasks -H 'content-type: application/json' -d '{"id":3, "name": "買晚餐", "status":1}' | jq 
 curl -XDELETE  localhost/tasks/2
```
