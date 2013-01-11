#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import simplejson

render = web.template.render('/home/production/snipper/templates/')
urls = (
  '/', 'index',
  '/geturl/', 'geturl',
  '/geturl', 'geturl',
  '/([a-zA-Z0-9]+)/', 'redirect',
  '/([a-zA-Z0-9]+)', 'redirect',
  '/([a-zA-Z0-9]+)/stats/', 'stats',
  '/([a-zA-Z0-9]+)/stats', 'stats',
)

APP_URL = 'http://snipper.in/'

app = web.application(urls, locals())
db = web.database(dbn='postgres', user='production', pw='', db='snipper')

def baseN(num,b):
    return ((num == 0) and  "0" ) or ( baseN(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])

def processurl(url):
    if url.lower().startswith("http://") or url.lower().startswith("https://") or url.lower().startswith("ftp://"):
        return url
    return "http://"+url

class index:
    def GET(self):
        return render.index('0',"")
    def POST(self):
        params = web.input(url=None)
        if not params.url:
           web.ctx.status = '404 Not Found'
	   return render.notfound("")
        url = processurl(params.url)
        data = db.select('links',dict(link=url),where = 'link=$link')
        for d in data:
           stuff = d
        if len(data)!=0:
           return render.index('1',APP_URL+stuff.hash)
        in_id = db.insert('links',link=url)
        hash = baseN(int(in_id),36)
        db.update('links',where="id=%d" % (in_id,),hash=hash)
	return render.index('1',APP_URL+hash)

class geturl:
    def GET(self):
        params = web.input(url=None,type=None)
        if not params.url:
           web.ctx.status = '404 Not Found'
           return render.notfound("")
        if params.type=='json':
           web.header('Content-Type', 'application/json')
        url = processurl(params.url)
        data = db.select('links',dict(link=url),where = 'link=$link')
        for d in data:
           stuff=d
        if len(data)!=0:
           return APP_URL + stuff.hash
        in_id = db.insert('links',link=url)
        hash = baseN(int(in_id),36)
        db.update('links',where="id=%d" % (in_id,),hash=hash)
        if params.type=='json':
           return simplejson.dumps(APP_URL + hash)
        return APP_URL + hash

class redirect:
    def GET(self,hash):
        data = db.select('links',dict(hash=hash),where = 'hash=$hash')
        for d in data:
           stuff = d
	if len(data)==0:
           web.ctx.status = '404 Not Found'
           return render.notfound("")	   
        referer = web.ctx.env.get('HTTP_REFERER', '')
        ip = web.ctx.env.get('REMOTE_ADDR','')
        browser = web.ctx.env.get('HTTP_USER_AGENT','')
        db.insert('logs',link=d.id,ip=ip,browser=browser,redirect=referer)
        raise web.seeother(d.link)

class stats:
    def GET(self,hash):
        data = db.select('links',dict(hash=hash),where = 'hash=$hash')
        if len(data)==0:
           web.ctx.status = '404 Not Found'
           return render.notfound("")	   
        data = db.query("select count(*) as count from logs,links where logs.link=links.id and links.hash='%s'" % (hash,))
        for d in data:
           stuff = d
        last5 = db.query("select logs.ip as ip,logs.created_at as created_at from logs,links where logs.link=links.id and links.hash='%s' limit 5" % (hash,))
        return render.stats(d.count,last5)

if __name__ == "__main__":
    app.run()

application = web.application(urls, globals()).wsgifunc()
