"""Diagnostics support for KNX."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config as conf_util
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.system_info import async_get_system_info

from . import CONFIG_SCHEMA
from .const import DOMAIN


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""
    diag: dict[str, Any] = {}
    diag["home_assistant"] = await async_get_system_info(hass)

    knx_module = hass.data[DOMAIN]
    diag["xknx"] = {
        "version": knx_module.xknx.version,
        "current_address": str(knx_module.xknx.current_address),
    }

    diag["config_entry_data"] = dict(config_entry.data)

    raw_config = await conf_util.async_hass_config_yaml(hass)
    diag["configuration_yaml"] = raw_config.get(DOMAIN)
    try:
        CONFIG_SCHEMA(raw_config)
    except vol.Invalid as ex:
        diag["configuration_error"] = str(ex)
    else:
        diag["configuration_error"] = None

    return diag
