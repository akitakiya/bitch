#!/usr/bin/env python
# -*- coding: gbk -*-
# -*- coding: utf_8 -*-
import sys, os
import urllib2
from threading import Thread 
import time 
import Queue
# working thread 
class Worker(Thread): 
    worker_count = 0 
    timeout = 1 
    def __init__( self, workQueue, resultQueue, **kwds): 
        Thread.__init__( self, **kwds ) 
        self.id = Worker.worker_count 
        Worker.worker_count += 1 
        self.setDaemon( True ) 
        self.workQueue = workQueue 
        self.resultQueue = resultQueue 
        self.start( ) 

    def run( self ): 
        ''''' the get-some-work, do-some-work main loop of worker threads ''' 
        while True: 
            try: 
                callable, args, kwds = self.workQueue.get(timeout=Worker.timeout) 
                res = callable(*args, **kwds) 
                self.resultQueue.put( res ) 
                #time.sleep(Worker.sleep) 
            except Queue.Empty: 
                break 
            except : 
                print 'worker[%2d]' % self.id, sys.exc_info()[:2] 
                raise 

class WorkerManager: 
    def __init__( self, num_of_workers=10, timeout = 2): 
        self.workQueue = Queue.Queue() 
        self.resultQueue = Queue.Queue() 
        self.workers = [] 
        self.timeout = timeout 
        self._recruitThreads( num_of_workers ) 

    def _recruitThreads( self, num_of_workers ): 
        for i in range( num_of_workers ): 
            worker = Worker( self.workQueue, self.resultQueue ) 
            self.workers.append(worker) 

    def wait_for_complete( self): 
        # ...then, wait for each of them to terminate: 
        while len(self.workers): 
            worker = self.workers.pop() 
            worker.join( ) 
            if worker.isAlive() and not self.workQueue.empty(): 
                self.workers.append( worker ) 
        print "All jobs are are completed." 

    def add_job( self, callable, *args, **kwds ): 
        self.workQueue.put( (callable, args, kwds) ) 

    def get_result( self, *args, **kwds ): 
        return self.resultQueue.get( *args, **kwds ) 
try:
    from lxml import html
except ImportError:
    raise SystemExit('\n[X] lxml模块导入错误,请执行pip install lxml安装!')


class SubMain():
    '''
    渗透测试域名收集
    '''

    def __init__(self, submain):
        self.submain = submain
        self.url_360 = 'http://webscan.360.cn/sub/index/?url=%s' % self.submain
        self.url_link = 'http://i.links.cn/subdomain/'
        self.link_post = 'domain=%s&b2=1&b3=1&b4=1' % self.submain
        self.sublist = []

    def get_360(self):
        scan_data = urllib2.urlopen(self.url_360).read()
        html_data = html.fromstring(scan_data)
        submains = html_data.xpath("//dd/strong/text()")
        return self.sublist.extend(submains)

    def get_links(self):
        link_data = urllib2.Request(self.url_link, data=self.link_post)
        link_res = urllib2.urlopen(link_data).read()
        html_data = html.fromstring(link_res)
        submains = html_data.xpath("//div[@class='domain']/a/text()")
        submains = [i.replace('http://', '') for i in submains]
        return self.sublist.extend(submains)

    def scan_domain(self):
        self.get_360()
        self.get_links()
        return list(set(self.sublist))

def exploit(domain):
    submain = SubMain(domain).scan_domain()
    with open('subdomain.txt', 'w+') as domain_file:
        for item in submain:
            domain_file.write(item + '\n')
if __name__ == '__main__':
    wm = WorkerManager(20)
    with open('wooyun.txt') as f:
        for line in f:
            line = line.strip('\n')
            wm.add_job(exploit, line) 
    wm.wait_for_complete()  