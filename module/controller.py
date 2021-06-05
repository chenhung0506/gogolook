# coding=UTF-8
import requests
import json
import ast
import logging
import os
import threading
import daoGogolook
import log as logpy
import utils
import const
from datetime import datetime
from flask import Flask, Response, render_template, request, redirect, jsonify, send_from_directory, url_for, make_response
from threading import Timer,Thread,Event
from flask_restful import Resource
from datetime import datetime

log = logpy.logging.getLogger(__name__)

def setup_route(api):
    api.add_resource(HealthCheck, '/healthCheck')
    # api.add_resource(Default, '/')
    api.add_resource(Tasks, '/tasks')
    api.add_resource(DelTasks, '/tasks/<path:id>')

class HealthCheck(Resource):
    log.debug('check health')
    def get(self):
        return {"status": "200","message": "success"}, 200
# curl -XGET localhost/tasks | jq
class Tasks(Resource):
    def get(self):
        try:
            data = daoGogolook.Database().getTasks(None)
            log.info(data)
            return {"result":data}, 200
        except Exception as e:
            log.error("GetTasks error: "+utils.except_raise(e))
            return {"status":400, "message":"get data error: {}".format(e)}, 200

    # curl -XPOST  localhost/tasks -H 'content-type: application/json' -d '{"name": "買晚餐"}' | jq 
    def post(self):
        try:
            input_data = json.loads(request.data)
            log.info(input_data)
            result = daoGogolook.Database().addTasks(input_data)
            if result:
                data = daoGogolook.Database().getTasks("add")
                return {"result":data}, 201
            return {"status":400, "message":"insert fail"}, 200
        except Exception as e:
            log.error("AddTasks error: "+utils.except_raise(e))
            return {"status":400, "message":"insert error: {}".format(e)}, 200
    # curl -XPUT  localhost/tasks -H 'content-type: application/json' -d '{"id":3, "name": "買晚餐", "status":1}' | jq 
    def put(self):
        try:
            input_data = json.loads(request.data)
            log.info(input_data)
            tasks = daoGogolook.Database().getTasks(input_data)
            if len(tasks) < 1:
                return {"status":400, "message":"更新失敗，任務 [ "+input_data.get('u_name')+" ] 不存在"},200
            result = daoGogolook.Database().editTasks(input_data)
            log.info('edit result:' + str(result))
            if result:
                data = daoGogolook.Database().getTasks(input_data)
                log.info(data)
                return data, 200
        except Exception as e:
            log.error("EditTasks error: "+utils.except_raise(e))
            return {"status":400, "message":"edit error: {}".format(e)}, 200

# curl -XDELETE  localhost/tasks/2
class DelTasks(Resource):
    def delete(self,id):
        try:
            log.info(id)
            result = daoGogolook.Database().delTasks(id)
            if result:
                return 200
            else:
                return {"status": 401, "message":"delete fail"}, 401
        except Exception as e:
            log.error("DelTasks error: "+utils.except_raise(e))
            return {"status":400, "message":"delete error: {}".format(e)}, 200