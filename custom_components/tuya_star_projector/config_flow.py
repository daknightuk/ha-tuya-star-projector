"""Config flow for Tuya Star Projector."""

from __future__ import annotations

from typing import Any

import tinytuya
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_DEVICE_ID,
    CONF_LOCAL_KEY,
    DEFAULT_NAME,
    DOMAIN,
    PROTOCOL_VERSION,
)


async def _test_connection(hass: HomeAssistant, data: dict[str, Any]) -> None:
    """Raise if the projector cannot be queried."""

    def query() -> None:
        device = tinytuya.Device(
            data[CONF_DEVICE_ID],
            data[CONF_HOST],
            data[CONF_LOCAL_KEY],
            version=PROTOCOL_VERSION,
        )
        device.set_socketTimeout(5)
        result = device.status()
        if not isinstance(result, dict) or "dps" not in result:
            message = (
                result.get("Error") or result.get("Err") or "No DPS returned"
                if isinstance(result, dict)
                else str(result)
            )
            raise ConnectionError(message)

    await hass.async_add_executor_job(query)


class TuyaStarProjectorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Collect and validate local Tuya credentials."""
        errors: dict[str, str] = {}
        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_DEVICE_ID])
            self._abort_if_unique_id_configured()
            try:
                await _test_connection(self.hass, user_input)
            except Exception:  # noqa: BLE001 - converted to a friendly flow error
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_DEVICE_ID): str,
                vol.Required(CONF_LOCAL_KEY): str,
            }
        )
        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )
