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
### step1: harbor login with account / password
#### account / password => guest / HelloGuest@1
```
docker login harbor.chlin.tk 
```
### step2: execute run.sh
```
cd ./gogolook/docker && ./run.sh 0 3 -v
```

## Deploy with docker build and docker run 
```
cd ./gogolook/docker && ./run.sh 0 1
```

## Note if mysql db was init, excute below command 
```
cd ./gogolook/docker && ./run.sh 3 -v
```
```
cd ./gogolook/docker && ./run.sh 1
```


## Test API
```
 curl -XGET localhost/tasks | jq
 curl -XPOST  localhost/tasks -H 'content-type: application/json' -d '{"name": "買晚餐"}' | jq 
 curl -XPUT  localhost/tasks -H 'content-type: application/json' -d '{"id":3, "name": "買晚餐", "status":1}' | jq 
 curl -XDELETE  localhost/tasks/2
```
