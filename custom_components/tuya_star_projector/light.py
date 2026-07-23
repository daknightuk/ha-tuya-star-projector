"""Colour and laser lights for Tuya Star Projector."""

from __future__ import annotations

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_HS_COLOR,
    ColorMode,
    LightEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    DP_COLOR,
    DP_COLOR_STATE,
    DP_LASER_BRIGHTNESS,
    DP_LASER_STATE,
    DP_MODE,
)
from .entity import StarProjectorEntity


def _decode_color(value: str | None) -> tuple[float, float, int]:
    """Convert Tuya's 12-character HSV string to HA values."""
    value = value or "000003e803e8"
    try:
        hue = int(value[0:4], 16)
        saturation = int(value[4:8], 16) / 10
        brightness = round(int(value[8:12], 16) * 255 / 1000)
        return hue, saturation, brightness
    except (TypeError, ValueError):
        return 0, 100, 255


def _encode_color(hue: float, saturation: float, brightness: int) -> str:
    """Convert HA HS/brightness values to Tuya's HSV string."""
    return (
        f"{round(hue):04x}"
        f"{round(saturation * 10):04x}"
        f"{round(brightness * 1000 / 255):04x}"
    )


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ProjectorColorLight(coordinator), ProjectorLaserLight(coordinator)])


class ProjectorColorLight(StarProjectorEntity, LightEntity):
    """Nebula colour light."""

    _attr_name = "Nebula Colour"
    _attr_icon = "mdi:palette"
    _attr_color_mode = ColorMode.HS
    _attr_supported_color_modes = {ColorMode.HS}

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "nebula")

    @property
    def is_on(self) -> bool:
        return bool(self.coordinator.data.get(DP_COLOR_STATE))

    @property
    def hs_color(self) -> tuple[float, float]:
        hue, saturation, _ = _decode_color(self.coordinator.data.get(DP_COLOR))
        return hue, saturation

    @property
    def brightness(self) -> int:
        return _decode_color(self.coordinator.data.get(DP_COLOR))[2]

    async def async_turn_on(self, **kwargs) -> None:
        hue, saturation, brightness = _decode_color(
            self.coordinator.data.get(DP_COLOR)
        )
        if ATTR_HS_COLOR in kwargs:
            hue, saturation = kwargs[ATTR_HS_COLOR]
        if ATTR_BRIGHTNESS in kwargs:
            brightness = kwargs[ATTR_BRIGHTNESS]
        await self.coordinator.async_set_many(
            {
                DP_COLOR_STATE: True,
                DP_MODE: "colour",
                DP_COLOR: _encode_color(hue, saturation, brightness),
            }
        )

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_set(DP_COLOR_STATE, False)


class ProjectorLaserLight(StarProjectorEntity, LightEntity):
    """Green laser with brightness control."""

    _attr_name = "Laser"
    _attr_icon = "mdi:laser-pointer"
    _attr_color_mode = ColorMode.BRIGHTNESS
    _attr_supported_color_modes = {ColorMode.BRIGHTNESS}

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "laser")

    @property
    def is_on(self) -> bool:
        return bool(self.coordinator.data.get(DP_LASER_STATE))

    @property
    def brightness(self) -> int:
        raw = int(self.coordinator.data.get(DP_LASER_BRIGHTNESS, 1000))
        return round(max(10, min(1000, raw)) * 255 / 1000)

    async def async_turn_on(self, **kwargs) -> None:
        values = {DP_LASER_STATE: True}
        if ATTR_BRIGHTNESS in kwargs:
            values[DP_LASER_BRIGHTNESS] = max(
                10, round(kwargs[ATTR_BRIGHTNESS] * 1000 / 255)
            )
        await self.coordinator.async_set_many(values)

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_set(DP_LASER_STATE, False)
