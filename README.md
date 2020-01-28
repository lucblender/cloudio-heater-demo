# cloudio-EndpointHeater-demo

## Description

This is an implementation of a smart heating system with the [cloud.iO java librarie](https://github.com/cloudio-project/cloudio-Endpoint-java) (using 2.0 snapshot). A naive implementation of a heater trying to regulate the ambient temperature following a set point.

This software is the cloud.iO MQTT Endpoint interface. It is needed to have Endpoint certificates to use this software and to have an instance of the [cloud.iO core](https://github.com/cloudio-project/cloudio-services) running. This software has for goal to be used with the [cloudio-heater-demo](https://github.com/lucblender/cloudio-heater-demo) GUI software, but it is not mandatory.

## Requirement

As explained earlier, you'll need cloud.iO Endpoint certificates, those are available through cloud.iO RESTfull API, contact your cloud.iO administrator if you don't know how to retrieve them.

You'll have to have the following files in the resources/cloud.io directory accoarding to your own "EndpointUUID":
  - "EndpointUUID".properties --> can follow the given example
  - "EndpointUUID".p12
  - ca-cert.jks

You'll also have to modify the [Heater.java](https://github.com/lucblender/cloudio-EndpointHeater-demo/blob/master/src/main/java/Heater.java) at line 14 and insert your endpointUUID.

## cloud.iO Endpoint structure

The model (following cloud.iO Endpoint->Node->Object->Attribute template) of the heater is the following:
  - "enpointUUID".myHeater.temperatures.temperature
    - Represent the ambiant temperature, will try to follow the set point
  - "enpointUUID".myHeater.temperatures.setPointTemperature
    - Represent the set point temperature

Those two Attributes can be access via grafana, the RESTFull API or with mqtt subscribes:
  - @update/"enpointUUID"/myHeater/temperatures/temperature
  - @set/"enpointUUID"/myHeater/temperatures/setPointTemperature
