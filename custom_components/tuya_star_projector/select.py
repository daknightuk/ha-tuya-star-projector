"""Mode selector for Tuya Star Projector."""

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, DP_MODE, MODES
from .entity import StarProjectorEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    async_add_entities([ProjectorModeSelect(hass.data[DOMAIN][entry.entry_id])])


class ProjectorModeSelect(StarProjectorEntity, SelectEntity):
    """Projector operating mode."""

    _attr_name = "Mode"
    _attr_options = MODES
    _attr_icon = "mdi:theme-light-dark"

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "mode")

    @property
    def current_option(self) -> str | None:
        value = self.coordinator.data.get(DP_MODE)
        return value if value in MODES else None

    async def async_select_option(self, option: str) -> None:
        await self.coordinator.async_set(DP_MODE, option)
