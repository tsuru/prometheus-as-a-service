# Prometheus as a Service for Tsuru

## What is Prometheus as a Service?
It is a service created for Tsuru[1]. It creates a prometheus time series database in Tsuru to get all the app's metrics that can be exposed to the user using grafana

## Diagram
![PaaS Diagram](https://github.com/tsuru/prometheus-as-a-service/blob/master/images/diagram.png?raw=true)

## Workflow
1- The client creates a prometheus instance: 
```
tsuru service-instance-add prometheus my-instance
```
2- The prometheus instance is created and can be accessed by its url: prometheus-cloud.tsuru.com  
3- The app should expose /metrics with the TSDB notation[2]:  
```
api_http_requests_total{method="GET", handler="/path1"} 172
api_http_requests_total{method="GET", handler="/path2"} 774
```
4- Prometheus instance will gather these metrics exposed by the app by bindind prometheus instance to the app:  
```
tsuru service-instance-bind prometheus my-instance -a my-app
```

## The Project
First, it was necessary to build a custom prometheus' docker image because we needed to change the custom target to the app by setting an environment var in Tsuru.  
It was built on the prometheus official repo[3]  
So we needed to build this image using 'make' and running 'docker build' with the Dockerfile the repo provides.  
We had to create a shell script(prometheus.sh) to get the tsuru's enviroment and set it to the default prometheus target  
We've created an api to handle all the calls from tsuru's api to create/remove/update/bind/unbind prometheus' service instances.  
We also had to create the service on tsuru using this doc[4]  

## Creating an app with metrics exposed
There's an example of app created for testing purposes[5]  

## Next Steps
1- First we need to use kubernetes to mount a tmpfs to write data into memory. Its writing these data to the disk and its bad. =(  
1.1- To accomplish this we must use kubernetes to mount this filer. We use kubernetes through Tsuru or directly.  
2- It should support large memory plans to retain more data  
3- It should scrap(get) metrics from apps from all units. Today its scraping only the app's endpoint  
4- We should finish implementing the status/remove routes for this service. Its only creating the instance and binding it to the app  

## Learning Tsuru
[1] Tsuru's documentation: https://tsuru.io/  
[2] Open TSDB: http://opentsdb.net/  
[3] https://github.com/prometheus/prometheus  
[4] Creating Tsuru's services: https://docs.tsuru.io/stable/services/build.html  
[5] Creating app with metrics: https://github.com/tsuru/prometheus-as-a-service/tree/master/app-demo  
