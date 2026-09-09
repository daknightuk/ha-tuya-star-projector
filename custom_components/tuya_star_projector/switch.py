"""Power switch for Tuya Star Projector."""

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, DP_POWER
from .entity import StarProjectorEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    async_add_entities([ProjectorPowerSwitch(hass.data[DOMAIN][entry.entry_id])])


class ProjectorPowerSwitch(StarProjectorEntity, SwitchEntity):
    """Main projector power."""

    _attr_name = "Power"
    _attr_icon = "mdi:projector"

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "power")

    @property
    def is_on(self) -> bool:
        return bool(self.coordinator.data.get(DP_POWER))

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.async_set(DP_POWER, True)

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_set(DP_POWER, False)
