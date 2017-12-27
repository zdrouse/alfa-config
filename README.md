# alfa-config

## Purpose

USB ALFA adapters always use default configurations on system boot, including VMs.
This project is an automated solution that will configure the following:

1. `macchanger -r wlan#` - Changes ALFA interface to use randomized MAC address
2. `iw reg set GY` - Sets wireless configuration to other country region (this allows increasing Tx Power)
3. `iwconfig wlan# txpower 30` - Sets Tx Power to 30 dBm

