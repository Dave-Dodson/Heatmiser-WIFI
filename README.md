Only supports reading and setting the temperature on one thermostat right now. The files here are a mash up of the built in heatmiser component and the wifi code I found at https://github.com/midstar/heatmiser_wifi so they get the real credit.

To install put these files in config/custom_components/climate/ and in your config yaml put

climate:
  - platform: heatmiserWIFI
    ipaddress: 192.168.0.12       # ip address of your thermostat
    port: 8068                    # port of thermostat. 8068 is the default
    pin: !secret thermostat_pin   # access pin for thermostat. Default is 0000

This is a work in progress so use at your own risk. After testing I'll clean up the files and submit a pull request to get them into Home Assistant properly.