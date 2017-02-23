#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""
Intentionally Vulnerable Web Application
"""
import os
import mimetypes
import sqlite3 as lite
import tornado.web
import tornado.httpserver
import rasp
rasp.rasp_init()


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/static/(.*)", StaticHandler),
            (r"/", MainHandler),
            (r"/index.html", MainHandler),
            (r"/search", SearchHandler),
            (r"/login.html", UsersHandler),
            (r"/server.html", ServerHandler),
        ]
        settings = {
            "template_path": os.path.join(os.path.dirname(__file__), 'templates'),
            "debug": True
        }
        tornado.web.Application.__init__(self, handlers, **settings)


class StaticHandler(tornado.web.RequestHandler):

    def get(self, path):
        print "GET ", self.request.uri
        path = 'static/' + path
        base = os.path.join(os.path.dirname(__file__))
        static_file = os.path.join(base, path)
        mime_type, _ = mimetypes.guess_type(static_file)
        if mime_type:
            self.set_header("Content-Type", mime_type)
        with open(static_file, "r") as fpl:
            self.write(fpl.read())


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        print "GET ", self.request.uri
        self.render("index.html")


class SearchHandler(tornado.web.RequestHandler):

    def get(self):
        print "GET ", self.request.uri
        query = self.get_argument("q", default="Query")
        self.render("search.html", query=query, link=query)


class UsersHandler(tornado.web.RequestHandler):

    def get(self):
        print "GET ", self.request.uri
        self.render("login.html", msg="")

    def post(self):
        print "POST ", self.request.uri, "\nBODY ", self.request.body
        con = lite.connect('test.db')
        dat = ""
        uname = self.get_argument('username')
        pwd = self.get_argument('password')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Users WHERE User ='" +
                        uname + "' AND Password ='" + pwd + "'")
            cur_resp = cur.fetchone()
        if not cur_resp:
            dat = "Login Failed"
        else:
            dat = "Login Success, Hello " + str(cur_resp[1])
        self.render("login.html", msg=dat)


class ServerHandler(tornado.web.RequestHandler):

    def get(self):
        print "GET ", self.request.uri
        self.render("server.html", msg="", cmd="127.0.0.1")

    def post(self):
        print "POST ", self.request.uri, "\nBODY ", self.request.body
        server = self.get_argument('server')
        process = os.popen('ping -c 3 ' + server)
        preprocessed = process.read()
        process.close()
        self.render("server.html", msg=preprocessed, cmd=server)


def create_db():
    con = lite.connect('test.db')
    with con:
        cur = con.cursor()
        cur.execute(
            "SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name = 'Users'")
        exc = cur.fetchone()[0]
        if exc == 0:
            cur.execute("CREATE TABLE Users(Id INT, User TEXT, Password TEXT)")
            cur.execute("INSERT INTO Users VALUES(1,'admin','admin')")
            cur.execute("INSERT INTO Users VALUES(2,'test-user','test@123')")
            cur.execute("INSERT INTO Users VALUES(3,'sagar','lall0l')")
            cur.execute("INSERT INTO Users VALUES(4,'alias','ohrealli')")
            cur.execute("INSERT INTO Users VALUES(5,'jacky','st40ngp@55')")
            cur.execute("INSERT INTO Users VALUES(6,'sam','tomTOM123')")
            cur.execute("INSERT INTO Users VALUES(7,'maxi','D@ni3lDizaark')")
            cur.execute("INSERT INTO Users VALUES(8,'lelol','Leeee@Looo@!$')")
            cur.fetchone()


def main():
    # create_db()
    applicaton = Application()
    http_server = tornado.httpserver.HTTPServer(applicaton)
    http_server.bind(7777, address='127.0.0.1')
    http_server.start()
    print "Server Started: http://127.0.0.1:7777"
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
