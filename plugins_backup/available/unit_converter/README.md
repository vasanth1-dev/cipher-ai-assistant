# Unit Converter Plugin

The **Unit Converter Plugin** provides common measurement conversions for Cipher v2. It is intended to power natural-language conversion requests and can also be reused by other plugins.

---

## Features

- Length conversion
- Weight conversion
- Temperature conversion
- Speed conversion
- Digital storage conversion
- Reusable conversion API

---

## Supported Categories

### Length

Supported units:

- mm
- cm
- m
- km
- in
- ft
- yd
- mi

---

### Weight

Supported units:

- mg
- g
- kg
- oz
- lb

---

### Temperature

Supported units:

- °C (`c`)
- °F (`f`)
- Kelvin (`k`)

---

### Speed

Supported units:

- m/s
- km/h
- mph

---

### Storage

Supported units:

- B
- KB
- MB
- GB
- TB

(Current implementation uses binary multiples: 1 KB = 1024 bytes.)

---

## Planned Voice Commands

Examples:

- convert 5 km to miles
- convert 100 fahrenheit to celsius
- convert 512 MB to GB
- convert 70 mph to km/h
- convert 25 kilograms to pounds

These requests will be handled by Cipher's structured conversion-intent pipeline.

---

## Public Methods

```python
convert_length()
convert_weight()
convert_temperature()
convert_speed()
convert_storage()
```

---

## Example Usage

Length:

```python
plugin.convert_length(
    10,
    "km",
    "mi"
)
```

Temperature:

```python
plugin.convert_temperature(
    98.6,
    "f",
    "c"
)
```

Storage:

```python
plugin.convert_storage(
    2048,
    "mb",
    "gb"
)
```

---

## Dependencies

Uses only the Python standard library.

No external packages are required.

---

## Error Handling

The plugin reports errors when:

- unsupported units are requested
- incompatible conversion categories are used
- invalid values are supplied

Errors are also written to Cipher's logging system.

---

## Future Enhancements

Planned capabilities include:

- Area conversion
- Volume conversion
- Pressure conversion
- Energy conversion
- Time conversion
- Currency conversion (online rates)
- Fuel economy conversion
- Scientific notation support
- Unit aliases and natural-language parsing
- AI-assisted conversion explanations

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.