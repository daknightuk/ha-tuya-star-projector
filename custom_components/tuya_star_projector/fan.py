"""Rotation control for Tuya Star Projector."""

from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.percentage import ranged_value_to_percentage

from .const import DOMAIN, DP_ROTATION
from .entity import StarProjectorEntity

SPEED_RANGE = (10, 1000)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    async_add_entities([ProjectorRotationFan(hass.data[DOMAIN][entry.entry_id])])


class ProjectorRotationFan(StarProjectorEntity, FanEntity):
    """Star-field rotation speed."""

    _attr_name = "Rotation"
    _attr_icon = "mdi:rotate-360"
    _attr_supported_features = (
        FanEntityFeature.SET_SPEED
        | FanEntityFeature.TURN_ON
        | FanEntityFeature.TURN_OFF
    )

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "rotation")

    @property
    def is_on(self) -> bool:
        return int(self.coordinator.data.get(DP_ROTATION, 10)) > 10

    @property
    def percentage(self) -> int:
        raw = int(self.coordinator.data.get(DP_ROTATION, 10))
        return 0 if raw <= 10 else ranged_value_to_percentage(SPEED_RANGE, raw)

    async def async_turn_on(self, percentage=None, **kwargs) -> None:
        await self.async_set_percentage(percentage or 100)

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_set(DP_ROTATION, 10)

    async def async_set_percentage(self, percentage: int) -> None:
        if percentage <= 0:
            await self.async_turn_off()
            return
        raw = round(10 + (percentage / 100) * 990)
        await self.coordinator.async_set(DP_ROTATION, raw)
