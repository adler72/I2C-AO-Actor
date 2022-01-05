
# -*- coding: utf-8 -*-
import os
from aiohttp import web
import logging
from unittest.mock import MagicMock, patch
import asyncio
import random
from cbpi.api import *
from smbus import SMBus


logger = logging.getLogger(__name__)

def get_Address():
        bus = SMBus(1) # 1 indicates /dev/i2c-1
        addresses = []
        for address in range(128):
            try:
                bus.read_byte(address)
                addresses.append(address)
            except:
                pass
        return addresses


@parameters([Property.Select("Address AO", get_Address(), description="The I2C actor address."),Property.Select("Port AO", options=[0x00,0x01,0x02,0x03], description="Port of the Analog-Ouput-Modul to which the actor is connected")])
class CustomActor(CBPiActor):
     @action("Set Power", parameters=[Property.Number(label="Power", configurable=True,description="Power Setting [0-100]")])
    async def setpower(self,Power = 100 ,**kwargs):
        self.power=int(Power)
        if self.power < 0:
            self.power = 0
        if self.power > 100:
            self.power = 100           
        await self.set_power(self.power)      
     
    def init(self, props):
        self.state = False
        self.adress_AO = int(self.props.get("Adress AO",104))
        self.port_AO = int(self.props.get("Port AO",0))
        
        self.bus = SMBus(1) # 1 indicates /dev/i2c-1
        pass

    async def on(self, power=0):
        logger.info("ACTOR %s ON" % self.id)
        if power is not None:
            self.power = int(power)
        HBy = int(int(self.power)*10.23/256)
        LBy = int(int(self.power)*10.23-HBy*256)
        field=[LBy,HBy]
        try:
            self.bus.write_i2c_block_data(int(self.address_AO),int(self.port_AO,16),field)
        except: # exception if write_byte fails
            pass  
        self.state = True


    async def off(self):
        logger.info("ACTOR %s OFF " % self.id)
        HBy = 0
        LBy = 0
        field=[LBy,HBy]
        try:
            self.bus.write_i2c_block_data(int(self.address_AO),int(self.port_AO,16),field) 
        except: # exception if write_byte fails
            pass
        self.state = False
    
    async def set_power(self, power):
        self.power = power
        await self.cbpi.actor.actor_update(self.id,power)
        pass
   

    def get_state(self):
        return self.state
    
    async def run(self):
        pass


def setup(cbpi):
    cbpi.plugin.register("I2C-AO-Actor", CustomActor)
    pass
