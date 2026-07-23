"""Rotation speed slider for Tuya Star Projector."""

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, DP_ROTATION
from .entity import StarProjectorEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the rotation speed slider."""
    async_add_entities([ProjectorRotationSpeed(hass.data[DOMAIN][entry.entry_id])])


class ProjectorRotationSpeed(StarProjectorEntity, NumberEntity):
    """Control DP 101 using the projector's native 1-100 scale."""

    _attr_name = "Rotation Speed"
    _attr_icon = "mdi:speedometer"
    _attr_native_min_value = 1
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_mode = NumberMode.SLIDER

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "rotation_speed")

    @property
    def native_value(self) -> float:
        """Return Tuya's 10-1000 value as a 1-100 percentage."""
        raw = int(self.coordinator.data.get(DP_ROTATION, 10))
        return max(1, min(100, raw / 10))

    async def async_set_native_value(self, value: float) -> None:
        """Set rotation speed; the SK20 stores percentage multiplied by ten."""
        await self.coordinator.async_set(DP_ROTATION, round(value * 10))
