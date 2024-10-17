from typing import TypedDict

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from nilan_proxy import NilanProxy # type: ignore

from custom_components.nilan_connect.const import DOMAIN # type: ignore

class NilanConnectHassData(TypedDict):
    proxy: NilanProxy    
    
def get_hass_data(hass: HomeAssistant, entry: ConfigEntry) -> NilanConnectHassData:
    return hass.data[DOMAIN][entry.entry_id]

def get_proxy(hass: HomeAssistant, entry: ConfigEntry) -> NilanProxy:
    data:NilanConnectHassData = hass.data[DOMAIN][entry.entry_id]
    return data["proxy"]
    
def remove_hass_data(hass: HomeAssistant, entry: ConfigEntry) -> NilanConnectHassData:
    return hass.data[DOMAIN].pop(entry.entry_id)
    
def set_hass_data(hass: HomeAssistant, entry: ConfigEntry, data:NilanConnectHassData) -> None:
    hass.data[DOMAIN][entry.entry_id] = data
