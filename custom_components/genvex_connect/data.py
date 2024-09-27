from typing import TypedDict

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from genvexnabto import GenvexNabto # type: ignore

from custom_components.genvex_connect.const import DOMAIN # type: ignore

class GenvexConnectHassData(TypedDict):
    genvexnabto: GenvexNabto    
    
def get_hass_data(hass: HomeAssistant, entry: ConfigEntry) -> GenvexConnectHassData:
    return hass.data[DOMAIN][entry.entry_id]

def get_genvexnabto(hass: HomeAssistant, entry: ConfigEntry) -> GenvexNabto:
    data:GenvexConnectHassData = hass.data[DOMAIN][entry.entry_id]
    return data["genvexnabto"]
    
def remove_hass_data(hass: HomeAssistant, entry: ConfigEntry) -> GenvexConnectHassData:
    return hass.data[DOMAIN].pop(entry.entry_id)
    
def set_hass_data(hass: HomeAssistant, entry: ConfigEntry, data:GenvexConnectHassData) -> None:
    hass.data[DOMAIN][entry.entry_id] = data
