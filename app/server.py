# -*- coding: utf-8 -*-
import log as logpy
import const
import controller
import daoMigrate
import utils
import os
import flask_restful
import json
import glob
import re
import unittest
import sys
from flask_restful import Api, Resource
from datetime import datetime
from flask import Flask, request, render_template, send_from_directory, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

utils.setLogFileName()
log = logpy.logging.getLogger(__name__)
app = Flask(__name__)
api = Api(app)
controller.setup_route(api)

if __name__=="__main__":
    sched = BackgroundScheduler()
    sched.start()
    sched.add_job(utils.setLogFileName, CronTrigger.from_crontab('59 23 * * *'))
    dbData = daoMigrate.Database().getMigrate()
    log.info(dbData)

    #====== migrate db start =======
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
    #====== migrate db end =======

    #====== unittest start =======
    tests = unittest.TestLoader().discover("unitTest")
    log.info(tests)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.errors or result.failures:
        sys.exit(1)
    #====== unittest end =======

    app.run(host="0.0.0.0", port=const.PORT, debug=True, use_reloader=False)


