# Location Plugin

The **Location Plugin** allows Cipher v2 to determine the device's approximate location using an IP-based geolocation service.

---

## Features

- Detect current public IP address
- Get city, region, country
- Get postal code
- Get latitude and longitude
- Get timezone
- Get ISP / organization information
- Open the current location in Google Maps

---

## Supported Commands

### Current Location

Examples:

- where am I
- my location
- current location
- where are we
- detect my location

---

### Open Map

Examples:

- open my location in maps
- show my location on map
- open Google Maps
- current location on map

---

## Example Response

```python
{
    "success": True,
    "message": "You are currently in Chennai, Tamil Nadu, India.",
    "location": {
        "ip": "203.xxx.xxx.xxx",
        "city": "Chennai",
        "region": "Tamil Nadu",
        "country": "India",
        "postal": "600001",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "timezone": "Asia/Kolkata",
        "org": "ISP Name"
    }
}
```

---

## Data Source

The plugin uses an IP-based geolocation service:

- `https://ipapi.co/json/`

The reported location is an approximation based on the public IP address and may not reflect the device's precise GPS location.

---

## Dependencies

Python package:

- `requests`

Standard library:

- `webbrowser`

Internet connectivity is required.

---

## Privacy

- The plugin only requests approximate geolocation data from the configured service.
- It does **not** access GPS hardware.
- No location history is stored by the plugin.

---

## Future Enhancements

Planned capabilities include:

- GPS support (when available)
- Reverse geocoding
- Nearby places search
- Distance calculations
- Weather integration
- Live location updates
- Offline location cache
- Map provider selection
- Geofencing support
- Navigation integration

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.