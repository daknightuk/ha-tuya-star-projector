"""Base entity for Tuya Star Projector."""

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_DEVICE_ID, DOMAIN
from .coordinator import StarProjectorCoordinator


class StarProjectorEntity(CoordinatorEntity[StarProjectorCoordinator]):
    """Common entity attributes."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: StarProjectorCoordinator, suffix: str) -> None:
        super().__init__(coordinator)
        device_id = coordinator.entry.data[CONF_DEVICE_ID]
        self._attr_unique_id = f"{device_id}_{suffix}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=coordinator.entry.title,
            manufacturer="Tuya",
            model="SK20 Star Projector",
        )
