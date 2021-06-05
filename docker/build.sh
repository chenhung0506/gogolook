#!/bin/bash
build() {
  DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
  BUILDROOT=$DIR/..
  cmd="DOCKER_BUILDKIT=1 docker build -t $REPO/$CONTAINER:$TAG -f $DIR/Dockerfile $BUILDROOT"
  # cmd="DOCKER_BUILDKIT=1 docker build -t $DOCKER_IMAGE -f $DIR/Dockerfile $BUILDROOT --no-cache=true"
  echo $cmd
  eval $cmd
  # sed -n 's/TAG=//1p'
}

imagePull() {
    cmd "git pull"
    echo 'execute:'$cmd
    eval $cmd
    echo "# Launching $DOCKER_IMAGE"
    # Check if docker image exists (locally or on the registry)
    local_img=$(docker images | grep $REPO | grep $CONTAINER | grep $TAG)
    if [ -z "$local_img" ] ; then
      echo "# Image not found locally, let's try to pull it from the registry."
      docker pull $DOCKER_IMAGE
      if [ "$?" -ne 0 ]; then
        echo "# Error: Image not found: $DOCKER_IMAGE"
        exit 1
      fi
    fi
    echo "# Great! Docker image found: $DOCKER_IMAGE"
}

dockerRun() {
  # global config:" \
  # - use local timezone \
  # - max memory = 5G \
  # "
  globalConf="
    -v ~/volumes/university:/usr/src/app/logs \
    -v ~/.ssh/known_hosts:/root/.ssh/known_hosts \
    -v ~/etc/timezone:/etc/localtime:ro \
    -m 5125m \
    --restart always \
    --net nginx \
    -e TZ=Asia/Taipei \
  "
  moduleConf="
    -p $PORT:$PORT \
    --env-file $ENV \
  "
  docker rm -f -v $CONTAINER
  cmd="docker run -d --name $CONTAINER \
    $globalConf \
    $moduleConf \
    $DOCKER_IMAGE \
  "
  echo $cmd
  eval $cmd
}

saveImage(){
  DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
  BUILDROOT=$DIR/..

  if [ ! -e $BUILDROOT/imgs ]; then
    echo 'imgs folder not found mkdir it'
    mkdir $BUILDROOT/imgs
  fi

  cmd="docker save $REPO/$CONTAINER:$TAG | gzip > $BUILDROOT/imgs/$CONTAINER-$TAG.tar.gz"
  echo $cmd
  eval $cmd
}

saveDeploy(){
  DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )"
  PROJECT_NAME="$(cd $DIR && basename "$PWD")"
  BUILD_DIR=$DIR/../..
  cmd="tar -C $DIR/.. -zcvf ${DIR}-${TAG}.tar.gz ${PROJECT_NAME}"
  # $(basename "$PWD")
  echo $cmd
  eval $cmd
  echo $cmd
}

init_db() {
  echo 'remove running container'
  docker rm -f mysql 
  
  echo 'remove mysql data'
  rm -rf ~/volumes/mysql

  echo 'execute mysql container'
  docker run --name mysql \
  -e MYSQL_USER=deployer -e MYSQL_PASSWORD=Password@1 \
  -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=migrate \
  -v ~/volumes/mysql:/var/lib/mysql \
  -p 3306:3306 -d mysql/mysql-server:8.0.23

  echo "sleeping 30 seconds for mysql init"
  sleep 30

  echo 'execute mysql container'
  docker exec -i mysql bash -c 'mysql -uroot -ppassword'  << EOF 
  GRANT ALL PRIVILEGES ON *.* TO 'deployer'@'%';
  DROP TABLE if exists migrate.migrate;
  CREATE TABLE migrate.migrate(
      id INT NOT NULL AUTO_INCREMENT,
      name VARCHAR(20) NOT NULL,
      init_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY ( id )
  )engine=InnoDB default charset=utf8mb4 collate utf8mb4_general_ci comment='migrate';
EOF

}

  CREATE DATABASE IF NOT EXISTS migrate DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

print_options(){
  echo "[ ------- 0.  init db             ------- ]"
  echo "[ ------- 1.  build and run       ------- ]"
  echo "[ ------- 2.  pull image and run  ------- ]"
  echo "[ ------- 3.  run module          ------- ]"
  echo "[ ------- 4.  stop module         ------- ]"
  echo "[ ------- 5.  push image          ------- ]"
  echo "[ ------- 6.  save image          ------- ]"
  echo "[ ------- 7.  save deploy         ------- ]"
  echo "[ ------- 8.  delete image        ------- ]"
}

print_help(){
  echo "=============================================="
  echo "First Options: "
  print_options
  echo "Other Options:"
  echo "-t : Input tag by user"
  echo "-v : Build with git data"
  echo "-l : Run with latest version"
  echo "-e : Specify .env file"
  echo "-p : Push image"
  echo "First Run Example:"
  echo "./run.sh 0 1"
  echo "Run Example:"
  echo "./run.sh 1"
  echo "./run.sh 1 -v -t input_tag_name"
  echo "./run.sh 1 -v -p"
  echo "./run.sh 1 -v -p -e dev.env -t test"
  echo "./run.sh 3 -v"
  echo "./run.sh 3 -l"
  echo "./run.sh 3 -t input_tag_name"
  echo "=============================================="
}

select_number(){
  # 如果帶入參數不等於數字 0~9 則詢問user
  if [[ "$1" =~ ^[0-9] ]]; then
    mode=$1
  else
    print_options
    read -t 90 -p $'請輸入操作序號，如 1,2,3,7 \n' mode 
    if [[ ! $? -eq 0 ]]
      then
        echo "input timeout"
        exit 1
    fi
  fi
  if [ "$mode" == "q" -o "$mode" == "quit" -o "$mode" == "exit" -o "$mode" == "bye" ]; then
      exit 0
  fi
  return $mode
}

execute_option(){
  mode=$1
  echo "excute mode: "$mode
  CMD=""
  if [ $mode == "0" ]; then
      echo "[ ------- 0.  init db             ------- ]"
      CMD=("init_db")
  elif [ $mode == "1" ]; then
      echo "[ -------- 1.   build and run        -------- ]"
      CMD=("build" "docker-compose up -d")
  elif [ $mode == "2" ]; then
      echo "[ -------- 2.   pull image and run   -------- ]"
      CMD=("imagePull" "docker-compose up -d")
  elif [ $mode == "3" ]; then
    echo "[ -------- 3.   run module           -------- ]"
      echo 'docker run with TAG:' $TAG
      CMD=("docker-compose up -d")
  elif [ $mode == "4" ]; then
    echo "[ -------- 4.   stop module          -------- ]"
      CMD=("docker-compose down")
  elif [ $mode == "5" ]; then
    echo "[ -------- 5.   push image           -------- ]"
      CMD=("docker push $REPO/$CONTAINER:$TAG")
  elif [ $mode == "6" ]; then
      echo "[ -------- 6.   save image           -------- ]"
      CMD=("saveImage")
  elif [ $mode == "7" ]; then
      echo "[ -------- 7.   save deploy          -------- ]"
      CMD=("saveDeploy")
  elif [ $mode == "8" ]; then
      echo "[ -------- 8.  delete image          -------- ]"
      docker rmi -f $(docker images | grep $CONTAINER | awk "{print$3}")
  fi

  if [[ ${#CMD} > 0 ]]; then
      for val in "${CMD[@]}"; do
        echo $val && eval $val
      done
  fi
}

getopts_help(){
  while getopts 'h' OPT; do
      case $OPT in
          h) print_help
             exit 1 ;;
      esac
  done
}

setting_getopts(){
  while getopts 't:vlphe:' OPT; do
      echo "$OPT = $OPTARG"
      case $OPT in
          t) export TAG="$OPTARG";;
          v) export TAG=$(git rev-parse --short=7 HEAD)-$(git log HEAD -n1 --pretty='format:%cd' --date=format:'%Y%m%d-%H%M');;
          l) export TAG=$(docker images | grep $CONTAINER | awk 'NR==1{print$2}');;
          e) export ENV="$OPTARG";;
          p) export PUSH_IMG=true;;
          h) print_help
             exit 1 ;;
      esac
  done

  DOCKER_IMAGE=$REPO/$CONTAINER:$TAG
  echo 'TAG:'$TAG
  echo 'ENV:'$ENV
  echo "DOCKER_IMAGE:" $DOCKER_IMAGE
  echo 'PUSH_IMG:'$PUSH_IMG

  set -o allexport
  source $ENV
  set +o allexport

  export ENV=$ENV
  export TAG=$TAG
  export PUSH_IMG=$PUSH_IMG
  export DOCKER_IMAGE=$REPO/$CONTAINER:$TAG
}