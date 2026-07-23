# Tuya Star Projector Integration for Home Assistant

A Home Assistant custom integration for direct, local control of Tuya and
Smart Life SK20-style star projectors.

It communicates directly with the projector over your local network, so Homebridge, Apple HomeKit, custom ESP firmware, the official Tuya Home Assistant integration, LocalTuya, and Tuya Local are not required.

## Features

- Main projector power
- Nebula light on/off
- Nebula colour wheel
- Nebula brightness
- Laser on/off
- Laser brightness
- Rotation on/off
- Rotation speed control
- Operating modes: `white`, `colour`, and `scene`
- Configuration through the Home Assistant interface
- Local polling with no Tuya cloud dependency during normal operation

## Supported device

This integration was developed for the Tuya/Smart Life **SK20 Star
Projector** using the following datapoints:

| Function | DP | Value |
| --- | ---: | --- |
| Main power | 20 | Boolean |
| Operating mode | 21 | `white`, `colour`, or `scene` |
| Laser brightness | 22 | 10–1000 |
| Nebula colour | 24 | Tuya HSV string |
| Scene data | 25 | Encoded scene data |
| Rotation speed | 101 | 10–1000 |
| Laser state | 102 | Boolean |
| Nebula state | 103 | Boolean |

Other projectors using the same datapoints may also work, but have not been
tested.

## Installation with HACS

Until this integration is included in the default HACS repository list, add it
as a custom repository:

1. Open **HACS** in Home Assistant.
2. Open the three-dot menu in the upper-right corner.
3. Select **Custom repositories**.
4. Enter:

   ```text
   https://github.com/daknightuk/ha-tuya-star-projector
   ```

5. Select **Integration** as the repository type.
6. Select **Add**.
7. Find **Tuya Star Projector** in HACS and download it.
8. Restart Home Assistant.

## Manual installation

1. Download the latest release.
2. Copy this directory:

   ```text
   custom_components/tuya_star_projector
   ```

   into your Home Assistant configuration directory:

   ```text
   /config/custom_components/tuya_star_projector
   ```

3. Restart Home Assistant.

The final path must contain `manifest.json`:

```text
/config/custom_components/tuya_star_projector/manifest.json
```

## Configuration

After installation:

1. Open **Settings → Devices & services**.
2. Select **Add integration**.
3. Search for **Tuya Star Projector**.
4. Enter:

   - A friendly name for the projector
   - The projector's local IP address
   - Its Tuya device ID (`tuyaId`)
   - Its Tuya local key (`tuyaKey`/`local_key`)

The integration tests the local connection before saving the configuration.

## Entities

The integration creates the following controls:

| Entity type | Name | Purpose |
| --- | --- | --- |
| Switch | Power | Main projector power |
| Light | Nebula Colour | Nebula on/off, colour, and brightness |
| Light | Laser | Laser on/off and brightness |
| Fan | Rotation | Rotation on/off and percentage speed |
| Number | Rotation Speed | Dedicated 1–100% rotation-speed slider |
| Select | Mode | Selects `white`, `colour`, or `scene` mode |

The **Mode** selector does not choose a colour. Open the separate **Nebula
Colour** light entity to access its colour wheel.

## Before adding the integration

Complete all three preparation steps below before trying to configure the
projector in Home Assistant.

### 1. Obtain the Device ID and local key

The old Homebridge configuration calls these values `tuyaId` and `tuyaKey`.
Tuya's current platform calls them `id` (or **Device ID**) and `local_key`.
They are the same values:

| Homebridge name | Tuya platform name | Home Assistant field |
| --- | --- | --- |
| `tuyaId` | `id` / Device ID | Device ID |
| `tuyaKey` | `local_key` | Local key |

To obtain them:

1. Sign in to the
   [Tuya Developer Platform](https://platform.tuya.com/).
2. Open **Cloud → Development**.
3. Create a cloud project if you do not already have one:

   - Choose **Smart Home** as the development method.
   - Choose the data centre that matches the region of your Smart Life
     account.
   - Authorize **Industry Basic Service**, **Smart Home Basic Service**, and
     **Device Status Notification** when prompted.

4. Open the project and select **Devices**.
5. Select **Link Tuya App Account → Add App Account**.
6. A QR code appears. In Smart Life, use its scanner to scan the code and
   confirm the login/link request.
7. Return to the project and open **Devices → All Devices**. Locate the star
   projector and copy its **Device ID**. This is the value to enter as the
   integration's Device ID.
8. If the device details page displays **Local Key**, copy it. If it does not:

   - Open **Cloud → API Explorer**.
   - Select the same cloud project.
   - Find **IoT Core → Device Management → Query Device Details**.
   - Enter the projector's Device ID and submit the request.
   - In the returned `result`, copy `local_key`.

The current Tuya device-details endpoint is:

```text
GET /v2.0/cloud/thing/{device_id}
```

Its result contains both `id` and `local_key`.

> **Keep the local key secret.** Never place a real Device ID or local key in
> GitHub, screenshots, logs, configuration examples, or support requests.
> Removing and re-pairing a device in Smart Life can change its local key.

### 2. Find the projector's MAC address

In the Smart Life app:

1. Open the star projector.
2. Tap the **pencil/edit icon** in the top-right corner.
3. Tap **Device Information**.
4. Copy or write down the projector's **MAC address**.

### 3. Assign a static IP address and power-cycle

The integration connects directly to the projector's local IP address. That
address must not change.

1. Sign in to your router.
2. Find **DHCP reservation**, **Address reservation**, **Static lease**, or a
   similarly named page.
3. Create a reservation for the projector using the MAC address obtained from
   Smart Life.
4. Assign the IP address that you intend to enter into Home Assistant.
5. Save/apply the router configuration.
6. **Power-cycle the projector**: disconnect its power, wait several seconds,
   and reconnect it.
7. Confirm that the projector reconnects using the reserved IP address.

Only after completing the reservation and power cycle should you install the
repository through HACS and add **Tuya Star Projector** under
**Settings → Devices & services**.

Home Assistant must be able to reach the projector on the local network. Avoid
controlling it simultaneously from multiple local Tuya integrations. Internet
access is not required for normal local control after configuration.

## Troubleshooting

### The integration is not listed

- Confirm the integration folder is named `tuya_star_projector`.
- Confirm `manifest.json` is directly inside that folder.
- Restart Home Assistant.
- Clear or refresh the browser cache.
- Check **Settings → System → Logs** for errors mentioning
  `tuya_star_projector`.

### Cannot connect during setup

- Confirm the projector is powered and connected to Wi-Fi.
- Confirm its IP address has not changed.
- Check the device ID and local key.
- Confirm that the router's static DHCP reservation matches the MAC address
  shown in Smart Life.
- Power-cycle the projector after creating or changing the reservation.
- Ensure Home Assistant and the projector can communicate across any VLAN or
  firewall rules.

### Power works but another control does not

Confirm that the projector uses the datapoints listed in the supported-device
table. Similar-looking Tuya projectors can use different datapoint numbers or
value ranges.

### Colour control

Use the **Nebula Colour** light entity rather than the Mode selector. Selecting
a colour automatically places the projector into `colour` mode.

### Rotation control

Use either the **Rotation** fan entity or the dedicated **Rotation Speed**
number slider. The number slider maps Home Assistant's 1–100% range to the
SK20's DP 101 range of 10–1000.

## Diagnostics and bug reports

When reporting a problem, include:

- Home Assistant version
- Integration version
- Projector make and model
- Relevant Home Assistant log messages
- Which controls work and which fail

Remove device IDs, local keys, external IP addresses, tokens, and other secrets
before posting.

## Credits

The datapoint mapping and Tuya colour encoding were derived from the
MIT-licensed
[SeydX/homebridge-star-projector](https://github.com/SeydX/homebridge-star-projector)
project.

Local Tuya communication is provided by
[TinyTuya](https://github.com/jasonacox/tinytuya).

## Disclaimer

This is an independent community project. It is not affiliated with or
endorsed by Tuya, Smart Life, Home Assistant, or the projector manufacturer.

Use custom integrations at your own risk.
