#!/usr/bin/env python
# -*- coding:utf8 -*-
__author__ = 'xiaozhang'

import redis



class CI_Redis(object):
    def __init__(self,**kwargs):
        self.redis_conf=kwargs['redis']
        self.app=kwargs['app']
        self.redis=None
        self.init()

    def init(self):
        conf=self.app.merge_conf(self.redis_conf,{'db':0,'password':None,'port':6379})
        self.redis=redis.Redis(**conf)

    def __getattr__(self, item):
        if hasattr(self.redis,item):
            return getattr(self.redis,item)


if __name__=='__main__':
    conf={
    'host':'172.16.3.92',
    'port':6379,
#    'db':0,
   'password':None,
    }
    redisconf={'redis':conf,'app':'app'}

    r=CI_Redis(**redisconf)

    (r.set)('asdf','asdfasdfasdf')








