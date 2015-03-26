#!/usr/bin/python3
# -*-coding:utf-8 -*

from abc import ABCMeta, abstractmethod
import utils

class Browser(object):
    __metaclass__ = ABCMeta

    #METHODS
    def __init__(self):
        self.dataPath = utils.relativeToAbsoluteHomePath("/home/blink/profile/data.json")
    
    @abstractmethod
    def importData(self):
        raise NotImplementedError("importData function not implemented")

    @abstractmethod
    def exportData(self):
        raise NotImplementedError("exportData function not implemented")
    
    @abstractmethod
    def runBrowser(self):
        raise NotImplementedError("runBrowser function not implemented")
    

