"""Polling and command coordinator for a Tuya star projector."""

from __future__ import annotations

import asyncio
from datetime import timedelta
import logging
from typing import Any

import tinytuya

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    CONF_DEVICE_ID,
    CONF_LOCAL_KEY,
    DOMAIN,
    PROTOCOL_VERSION,
)

_LOGGER = logging.getLogger(__name__)


class StarProjectorCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Serialize local Tuya calls and publish projector DPS."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(
            hass,
            logger=_LOGGER,
            name=entry.title,
            update_interval=timedelta(seconds=10),
            config_entry=entry,
        )
        self.entry = entry
        self._lock = asyncio.Lock()
        self.device = tinytuya.Device(
            entry.data[CONF_DEVICE_ID],
            entry.data[CONF_HOST],
            entry.data[CONF_LOCAL_KEY],
            version=PROTOCOL_VERSION,
        )
        self.device.set_socketTimeout(5)
        self.device.set_socketPersistent(False)

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            async with self._lock:
                response = await self.hass.async_add_executor_job(self.device.status)
            if not isinstance(response, dict) or "dps" not in response:
                raise UpdateFailed(f"Invalid response from projector: {response}")
            return {str(key): value for key, value in response["dps"].items()}
        except UpdateFailed:
            raise
        except Exception as err:
            raise UpdateFailed(f"Unable to query projector: {err}") from err

    async def async_set(self, dp: str, value: Any) -> None:
        """Set one DPS and refresh state."""
        await self._async_call(self.device.set_value, int(dp), value)

    async def async_set_many(self, values: dict[str, Any]) -> None:
        """Set several DPS in one Tuya command and refresh state."""
        payload = {str(dp): value for dp, value in values.items()}
        await self._async_call(self.device.set_multiple_values, payload)

    async def _async_call(self, method: Any, *args: Any) -> None:
        try:
            async with self._lock:
                result = await self.hass.async_add_executor_job(method, *args)
            if isinstance(result, dict) and (result.get("Error") or result.get("Err")):
                raise HomeAssistantError(str(result.get("Error") or result.get("Err")))
        except HomeAssistantError:
            raise
        except Exception as err:
            raise HomeAssistantError(f"Projector command failed: {err}") from err
        await self.async_request_refresh()
