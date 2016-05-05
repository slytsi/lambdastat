# lambdastat
These are python programs that will allow you to poll temperature sensor data from a digital probe from a raspberry pi and send IR commands via AWS lambda to turn on an airconderer. The raspberrypi code is written for python 3.5.1 as it supports TLS v1.2 which is required by AWS IoT service. It will utilize the AWS IoT service to send temperature reading to the AWS IoT service. 
This file is called lambdastat.py and utilizes a DS18B20 digital temperature gauge connected to a raspberry pi 2.
By default it will poll once a minute which roughly equates to a a $.21 AWS IoT bill per month in US-East-1 region.

The AWS Iot service is configured for rule actions to send the temperature data to Cloudwatch. Cloudwatch will be configured to push data to AWS Elasticsearch to maintain it for long term storage and serve as the visualization platform. To enable the thermostat to be remotely controlled, a python Lambda function will be triggered by a Cloudwatch alarm based on the temperature being above or below a certain temperature. This python function is configured to run in python 2.7. The lambda function should cost $.01 a month if it was triggered 48 times a day.
There are a series of lambda functions that all perform a specific function. The lambda functions fire IR codes to an ethernet to IR repeater that is sending remote IR codes to an airconditioning unit.
