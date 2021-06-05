import unittest
from flask import url_for, Flask, request, render_template, send_from_directory, redirect, url_for
from flask_testing import TestCase
import json
import os, sys
import pymysql
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.append(parentdir)
from module import callApiUtils
from module import daoGogolook
from module import log as logpy
from module import const

log = logpy.logging.getLogger(__name__)

class SettingBase(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setUp(self):
        conn = pymysql.Connect(host=const.DB_HOST, port=int(const.DB_PORT), user=const.DB_ACCOUNT, passwd=const.DB_PASSWORD, db='gogolook',charset='utf8')
        pass

    def tearDown(self):
        pass

    def addTasks(self):
        return daoGogolook.Database().addTasks({"name":"unitest"})

    def getTasks(self):
        return daoGogolook.Database().addTasks({"name":"unitest"})

class CheckUserAndLogin(SettingBase):
    def test_addTasks(self):
        response = self.addTasks()
        log.info(response)
        self.assertEqual(response, True)

    def test_getTasks(self):
        response = self.getTasks()
        log.info(response)
        self.assertIsNotNone(response)

if __name__ == '__main__':
    unittest.main()