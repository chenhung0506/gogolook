# -*- coding: utf-8 -*-
from flask import Flask
# from flask_cors import CORS
import log as logpy
import re
import os
import const
import controller
import daoMigrate
import flask_restful
import utils
import json
import glob
import re
from flask_restful import Api
from flask_restful import Resource
from datetime import datetime
from flask import Flask, request, render_template, send_from_directory, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

utils.setLogFileName()
log = logpy.logging.getLogger(__name__)
template_dir = os.path.abspath('./resource/university/') # setting for render_template
app = Flask(__name__, template_folder=template_dir)
# app.config['UPLOAD_FOLDER'] = './univer/upload'
app.config['MAX_CONTENT_LENGTH'] = 128 * 1024 * 1024  # 16MB
api = Api(app)
controller.setup_route(api)

if __name__=="__main__":
    sched = BackgroundScheduler()
    sched.start()
    sched.add_job(utils.setLogFileName, CronTrigger.from_crontab('59 23 * * *'))

    dbData = daoMigrate.Database().getMigrate()
    log.info(dbData)

    # migrate db
    fileNameList=[]
    for file in glob.glob("./migrate/*.sql"):
        log.debug(file)
        regex = re.compile(r'^./migrate/{1}(.*).sql{1}$')
        match = regex.search(file)
        fileNameList.append(match.group(1))
    log.debug(fileNameList)
    sortedFileNameList=sorted(fileNameList)
    log.info(sortedFileNameList)
    for record in sortedFileNameList:
        if record not in dbData:
            file = "./migrate/{name}.sql".format(name=record)
            log.info(file)
            try:
                utils.excuteSqlFile(file)
            except Exception as e:
                utils.except_raise(e)
            try:
                result = daoMigrate.Database().addMigrate(record)
                log.info("migrate ./migrate/{name}.sql result: {result}".format(name=record, result=result))
            except Exception as e:
                utils.except_raise(e)

    app.run(host="0.0.0.0", port=const.PORT, debug=True, use_reloader=False)