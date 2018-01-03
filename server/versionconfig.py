import logging
import os
import sys
import socket
import ConfigParser
import enumerate_interfaces
import string
import inspect
import json 
from  baseconfig import baseconfig

class versionconfig(baseconfig):
    def __init__(self): 
        logger = logging.getLogger("basic")    
        logger.debug("version config init")
        baseconfig.__init__(self)
        self.filename=os.path.join(os.path.dirname(os.path.abspath(__file__)),'versionRCM.cfg')
        self.parse()
    
    def get_checksum(self,buildPlatformString=''): 
        logger = logging.getLogger("basic")    
        logger.debug("get_checksum")
        checksum = self.confdict.get(('checksum',buildPlatformString),'')
        downloadurl = self.confdict.get(('url', buildPlatformString),'')
        return(checksum,downloadurl)
