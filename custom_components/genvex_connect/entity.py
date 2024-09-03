"""GenvexConnect base entity class"""

import logging

from genvexnabto import GenvexNabto, GenvexNabtoDatapointKey, GenvexNabtoSetpointKey, GenvexNabtoUnits
from homeassistant.helpers.entity import Entity
from homeassistant.const import UnitOfTime,UnitOfTemperature,PERCENTAGE,CONCENTRATION_PARTS_PER_MILLION,REVOLUTIONS_PER_MINUTE



from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class GenvexConnectEntityBase(Entity):
    """Base for all GenvexConnect entities"""

    _attr_has_entity_name = True

    def __init__(
        self,
        genvex_nabto: GenvexNabto,
        name: str,
        value_key: GenvexNabtoDatapointKey|GenvexNabtoSetpointKey|None,
        use_default_update_handler: bool = True,
    ) -> None:
        self.genvex_nabto = genvex_nabto
        self._translation_key = name
        self._value_key = value_key
        self._unit_of_measurement = GenvexNabtoUnits.UNDEFINED
        if value_key is not None:
            self._unit_of_measurement = genvex_nabto.get_unit_of_measure(value_key)
            if use_default_update_handler:
                genvex_nabto.register_update_handler(value_key, self._on_change)
        if self._unit_of_measurement is not None:
            self.set_unit_of_measurement(self._unit_of_measurement)

    def set_unit_of_measurement(self, uom:str):
        # self._attr_unit_of_measurement = self.parseUnitOfMeasure(uom)
        return
        
    def parse_unit_of_measure(self, uom:str, default:str|None=None) -> str|None:
        match uom:
            case GenvexNabtoUnits.SECONDS:     return UnitOfTime.SECONDS
            case GenvexNabtoUnits.MINUTES:     return UnitOfTime.MINUTES
            case GenvexNabtoUnits.HOURS:     return UnitOfTime.HOURS
            case GenvexNabtoUnits.DAYS:     return UnitOfTime.DAYS
            case GenvexNabtoUnits.MONTHS:   return UnitOfTime.MONTHS
            case GenvexNabtoUnits.YEARS:    return UnitOfTime.YEARS
            case GenvexNabtoUnits.CELSIUS:  return UnitOfTemperature.CELSIUS
            case GenvexNabtoUnits.PCT:      return PERCENTAGE
            case GenvexNabtoUnits.PPM:      return CONCENTRATION_PARTS_PER_MILLION
            case GenvexNabtoUnits.RPM:      return REVOLUTIONS_PER_MINUTE
            case _:
                return default
    
    @property
    def translation_key(self) -> str|None:
        """Return the translation key to translate the entity's name and states."""
        return self._translation_key

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return f"{self.genvex_nabto.get_device_id()}_{self._translation_key.split("__")[0]}"

    @property
    def should_poll(self) -> bool:
        """Return false, we push changes to HA"""
        return False

    def _on_change(self, _old_value:int|float|None, _new_value:int|float|None):
        """Notify HA of changes"""
        if self.hass is not None:
            self.schedule_update_ha_state(force_refresh=True)

    @property
    def device_info(self):
        info = {
            "identifiers": {(DOMAIN, self.genvex_nabto.get_device_id())},
            "name": self.genvex_nabto.get_device_id(),
            "manufacturer": self.genvex_nabto.get_device_manufacturer(),
            "model": self.genvex_nabto.get_loaded_model_name(),
            "hw_version": f"M: {self.genvex_nabto.get_device_model()}, SD: {self.genvex_nabto.get_slave_device_number()}, SDM: {self.genvex_nabto.get_slave_device_model()}",
        }
        return info
