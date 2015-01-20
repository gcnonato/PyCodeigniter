#!/usr/bin/env python
# -*- coding:utf8 -*-
__author__ = 'xiaozhang'



import os
import sys
import logging
import inspect
import re


class CI_Loader(object):
    def __init__(self,**kwargs):
        self.application_path= kwargs['application_path']
        self.app=kwargs['app']
        self.kwargs=kwargs
        self.app_modules_list=['controllers','models','helpers','library']
        self.modules={}
        self.classes={}
        self.sys_path=sys.path
        for m in self.app_modules_list:
            self.modules[m]={}
        map(self._load_application,self.app_modules_list)

    def cls(self,name):
        return self.classes[name]
    def model(self,name):
        return self._load('models',name)
    def ctrl(self,name):
        return self._load('controllers',name)
    def helper(self,name):
        return self._load('helpers',name)
    def library(self,name):
        return self._load('library',name)
    def _load(self,categroy,name):
        try:
            return self.modules[categroy][name]['instance']
        except KeyError,e:
            self.app.logger.log(name+" not found")




    def regcls(self,name,aclass):
        self.classes[name]=aclass


    def _load_application(self,module_name,path=None):
        if path==None:
            path=self.application_path
        module_path=path+os.path.sep+module_name
        if not os.path.isdir(module_path):
            self.app.logger.log(module_path+' not exists')
            return
        if module_path not in sys.path:
            sys.path=self.sys_path
            sys.path.insert(0,module_path)
        files=os.listdir(path+os.path.sep+module_name)

        for file in files:
            file_path=path+os.path.sep+module_name+os.path.sep+ file
            if os.path.isfile(file_path) and file.endswith('.py') and file!='__init__.py':
                try:
                    module=file.split('.')[0]
                    # __import__(module)
                    exec("from "+module+" import "+module )
                    cmodule=__import__(module)

                    aclass= getattr(cmodule,module)

                    has_init=hasattr(aclass,'__init__')
                    if has_init:
                        init_member=getattr(aclass,'__init__')
                        arginfo= inspect.getargspec(init_member)
                    else:
                        arginfo=''
                    if module not in self.modules[module_name].keys():
                        _instance=None
                        try:

                            if str(arginfo).find('kwargs')>0:
                                _instance= eval(module+'(**self.kwargs)')
                            else:
                                _instance= eval(module+'()')

                            if not hasattr(_instance,'app'):
                                setattr(_instance,'app',self.app)

                        except Exception,e:
                            self.app.logger.log('create '+ module+ ' failed ,please check parameters',logging.ERROR)
                            # print(file_path, e)

                        self.modules[module_name][module]={'aclass':getattr( cmodule ,module),'instance':_instance}
                        self.classes[module]=getattr(cmodule ,module)

                except Exception,e:
                    self.app.logger.error(e)

            elif os.path.isdir(file_path):
                self._load(module_name,file_path)










if __name__=='__main__':

    #loader=CI_Loader(r'E:\python\study\Codeigniter\system',r'E:\python\study\Codeigniter\application')
    loader=CI_Loader(application_path=r'E:\python\study\Codeigniter\application',app=None)

    print loader.model('SearchModel')


