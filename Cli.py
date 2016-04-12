#!/usr/bin/env python
# -*- coding:utf8 -*-
__author__ = 'xiaozhang'


from codeigniter import ci
from codeigniter import CI_Cache
import os
import json

class Cli:


    def index(self):
        return "hello world"


    def help(self,param=''):
        return "hello world"

    def download(self,file=''):
        return open('files'+os.path.sep+ file,'rb').read()

    def shell(self,file='',param=''):
        return open('files'+os.path.sep+ file,'rb').read()


    def _params(self,param='{}',opts=''):
        params= json.loads(param)
        return params

    def listfile(self,param=''):
        return "\n".join(os.listdir('files'))


    def upload(self,**kwargs):
        print kwargs
        file=kwargs['file']
        filename='files/'+file.filename
        if not os.path.exists(filename):
            if isinstance(file,str):
                open(filename,'wb').write(file)
            else:
                open('files/'+file.filename,'wb').write(file.file.read())
            return 'success'
        else:
            return 'file exists'

    def delfile(self,param=''):
        params=self._params(param)
        filename=''
        key='Mz'
        k=''
        if  'f' in params:
            filename=params['f']
        else:
            return '-f(filename) require'
        if  'k' in params:
            k=params['k']
        else:
            return '-k(key) require'
        if not key==k:
            return 'key error'
        path='files/'+filename
        if os.path.exists(path):
            os.remove(path)
            return "sucess"
        else:
            return "Not Found"
