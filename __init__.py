import logging
from RHUI import UIField, UIFieldType, UIFieldSelectOption
import struct
from time import monotonic
from Database import ProgramMethod
from RHRace import RaceStatus
from flask.blueprints import Blueprint
from flask import Flask, templating
from eventmanager import Evt
import re

def __(str):
    return ""

logger = logging.getLogger(__name__)

#Version
VERSION_MAJOR = 1
VERSION_MINOR = 0

#Logging
DEBUG_LOGGING = False

#default values
PILOT_SECONDARY_COLOR_FIELD_NAME = "PilotSecondaryColor"
PILOT_URL_FIELD_NAME = "PilotDetailPhotoURL"

def log(message):
    if(DEBUG_LOGGING):
        logging.info(str(message))
    else:
        logging.debug(str(message))

def render_template(template_name_or_list, **context):
    try:
        return templating.render_template(template_name_or_list, **context)
    except Exception:
        logger.exception("Exception in render_template")
    return "Error rendering template"

def initialize(rhapi):
    RH = RUManager(rhapi)

    log("initializing pilot detail plugin")

    bp = Blueprint(
        'pilotphotos',
        __name__,
        template_folder='templates',
        static_folder='static',
        static_url_path='/pilotphotos/static'
    )



    #bp = Blueprint('pilotcard', __name__)
    @bp.route('/stream/pilotphoto/<int:node_id>')
    def bp_test_page(node_id):
        #return render_template('pilotcard.html', __=__,)
        return render_template('pilotphoto.html', serverInfo=None,
            getOption=rhapi.db.option, __=rhapi.__, node_id=node_id-1)
    rhapi.ui.blueprint_add(bp)
    
    #data attributes
    pilotSecondaryColor = UIField(name = PILOT_SECONDARY_COLOR_FIELD_NAME, label = "Secondary Color", field_type = UIFieldType.TEXT, desc = "hex color. E.G. #ff0000")
    pilotPhotoUrl = UIField(name = PILOT_URL_FIELD_NAME, label = "Pilot Photo URL", field_type = UIFieldType.TEXT)
    rhapi.fields.register_pilot_attribute(pilotPhotoUrl)
    rhapi.fields.register_pilot_attribute(pilotSecondaryColor)
    
    log("pilot detail plugin initialized")

class RUManager():
    def __init__(self, rhapi):
        self.rhapi = rhapi
        
        #websocket listeners
        self.rhapi.ui.socket_listen("get_pilot_photo", self.handleGetPilotPhoto)

        rhapi.events.on(Evt.HEAT_SET, self.handleGetPilotPhotos)

    def handleGetPilotPhotos(self, args):
        log("heat_set")
        log(args)
        heat = self.rhapi.db.heat_by_id(args["heat_id"])
        log("heat: "+str(heat))
        slots = self.rhapi.db.slots_by_heat(args["heat_id"])
        
        log("slots: "+str(slots))
        for slot in slots:
            log("slot: "+str(slot.node_index))
            pilotId = slot.pilot_id
            if(pilotId!=0 and pilotId!=None):
                self.sendPhotoURLByPilotId(pilotId, slot.node_index)

    def handleGetPilotPhoto(self, args):
        node = int(args["node"])
        pilotId = self.rhapi.race.pilots[node]
        if(pilotId!=0 and pilotId!=None):
            self.sendPhotoURLByPilotId(pilotId, node)

    def sendPhotoURLByPilotId(self, pilotId, node):
        pilotPhotoURL = self.rhapi.db.pilot_attribute_value(pilotId, PILOT_URL_FIELD_NAME)
        secondaryColor = self.rhapi.db.pilot_attribute_value(pilotId, PILOT_SECONDARY_COLOR_FIELD_NAME)
        
        #if the secondary color is invalid, use the primary color
        if(self.isValidHexColor(secondaryColor)==False):
            seatColor = self.rhapi.race.seat_colors[node]
            seatColor = self.colorToHex(seatColor)
            secondaryColor = seatColor
        
        log(pilotPhotoURL)
        pilot = self.rhapi.db.pilot_by_id(pilotId)
        if(pilot!=None):
            callsign = pilot.callsign
            body = {"callsign":callsign, "url": pilotPhotoURL, "node": node, "secondaryColor": secondaryColor}
            log("-> "+str(body))
            self.rhapi.ui.socket_broadcast("pilot_photo", body)

    def colorToHex(self, colorInt):
        return '#' + format(colorInt, '06x')
    
    def isValidHex(self, string):
        pattern = re.compile(r'^[a-fA-F0-9#]+$')
        return bool(pattern.match(string))
    
    def isValidHexColor(self, color):
        valid = True
        if(color==None):
            valid = False
        else:
            if(len(color)!=7) or (self.isValidHex(color)==False):
                valid = False
        return valid
