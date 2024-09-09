from typing import TypedDict

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from genvexnabto import GenvexNabto # type: ignore

from custom_components.genvex_connect.const import DOMAIN # type: ignore

class GenvexConnectHassData(TypedDict):
    genvex_nabto: GenvexNabto    
    
def getHassData(hass: HomeAssistant, entry: ConfigEntry) -> GenvexConnectHassData:
    return hass.data[DOMAIN][entry.entry_id]

def getGenvexNabto(hass: HomeAssistant, entry: ConfigEntry) -> GenvexNabto:
    data:GenvexConnectHassData = hass.data[DOMAIN][entry.entry_id]
    return data["genvex_nabto"]
    
def removeHassData(hass: HomeAssistant, entry: ConfigEntry) -> GenvexConnectHassData:
    return hass.data[DOMAIN].pop(entry.entry_id)
    
def setHassData(hass: HomeAssistant, entry: ConfigEntry, data:GenvexConnectHassData) -> None:
    hass.data[DOMAIN][entry.entry_id] = data
