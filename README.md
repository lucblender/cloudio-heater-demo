# cloudio-heater-demo

## Description

This software is a demonstration of a smart heating system using [cloud.iO](http://cloudio.hevs.ch). This software represents the two actors of cloud.iO, the Endpoint and the user, and the cloud part with the two databases of cloud.iO: MongoDB and influxDB.

This software is using the cloud.iO RESTful API. It is needed to have a cloud.iO username and password to use this software and to have an instance of the [cloud.iO core](https://github.com/cloudio-project/cloudio-services) running. You may also need the demo java implementation fo the heater available in this [cloudio-EndpointHeater-demo](https://github.com/lucblender/cloudio-EndpointHeater-demo) repository.

## Requirement

This software run with python 3, tested for 3.6 and above. The following packages are needed:
  - requests
  - tkinter
  - pygubu

## Launch

```python heaterDemo.py``` 

## GUI description

The upper left part represents the actual heater (Endpoint part). It shows the ambient temperature, and the set point temperature, both refreshed every second. The lower left part represents an interaction from the user to the Endpoint: setting the set point temperature. With the spinner, it is possible to change the temperature and with the button under it, to send the temperature to the Endpoint for it to regulate.

The right part represents the data stored in the cloud. On the MongoDB part, we can see the retrieved digital twin on the heater following the cloud.iO model; this model can be updated with the upper right button. On the influxDB part, we can see the temperature evolving through time.

![Test Image 1](img/UI.png)
