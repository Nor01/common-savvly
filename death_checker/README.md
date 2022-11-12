# template-python-service

This repository is a template for creating new python services. It contains:

* Sample service which just prints "pong" periodically, with a timestamp
* A two-stage `Dockerfile` to build the container
* A `deployment.yml` to deploy the container in Kubernetes

All of these will need to be adjusted for a new service, but that should be relatively simple, versus 
having to come up with them whole cloth. 

If the service is a web service that must be exposed outside of Kubernetes, you'd need to expose
it via a `Service` and an `Ingress`. (There are other options, but this is the simplest/most common.)

