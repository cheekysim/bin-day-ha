# Bin Day Checker - Home Assistant Addon

Check if today is bin day based on week frequency.

## Installation

1. Add this repository to your Home Assistant Add-on Store
2. Install the "Bin Day Checker" addon
3. Configure your options (see Configuration section)
4. Start the addon

## Configuration

```yaml
start_week: 1    # The week number to start the pattern (1-53)
frequency: 2     # How often in weeks (e.g., 2 for fortnightly)
days:
  - 2  # Tuesday
  - 3  # Wednesday
```

**start_week**: The first week number of the year when bins are collected (1-53)
**frequency**: Collection interval in weeks (e.g., 2 = every 2 weeks, 1 = weekly)
**Days of week**: 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday, 6=Saturday, 7=Sunday

### Example Configurations

- **Fortnightly on Tuesdays starting week 1**: `start_week: 1, frequency: 2, days: [2]`
- **Every 3 weeks on Mon/Wed starting week 5**: `start_week: 5, frequency: 3, days: [1, 3]`
- **Weekly on Fridays**: `start_week: 1, frequency: 1, days: [5]`

## Usage

Once running, the addon exposes an HTTP service at port 8099.

### REST Sensor

Add to your `configuration.yaml`:

```yaml
sensor:
  - platform: rest
    resource: http://YOUR_HA_IP:8099/status
    name: Bin Day
    value_template: "{{ value_json.bin_day }}"
    json_attributes:
      - message
      - start_week
      - frequency
      - days
```

### Template Sensor

```yaml
template:
  - binary_sensor:
      - name: "Is Bin Day"
        state: "{{ states('sensor.bin_day') == 'True' }}"
```

### Automation Example

```yaml
automation:
  - alias: "Bin Day Reminder"
    trigger:
      - platform: time
        at: "20:00:00"
    condition:
      - condition: state
        entity_id: binary_sensor.is_bin_day
        state: "on"
    action:
      - service: notify.notify
        data:
          message: "Don't forget - tomorrow is bin day!"
```
