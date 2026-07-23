"""Constants for the Tuya Star Projector integration."""

DOMAIN = "tuya_star_projector"
PLATFORMS = ["light", "fan", "switch", "select", "number"]

CONF_DEVICE_ID = "device_id"
CONF_LOCAL_KEY = "local_key"

DEFAULT_NAME = "Star Projector"
PROTOCOL_VERSION = 3.5

DP_POWER = "20"
DP_MODE = "21"
DP_LASER_BRIGHTNESS = "22"
DP_COLOR = "24"
DP_SCENE = "25"
DP_ROTATION = "101"
DP_LASER_STATE = "102"
DP_COLOR_STATE = "103"

MODES = ["white", "colour", "scene"]
