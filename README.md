# Shopping List Container - FAST API
## This is a simple app using FAST API to create and store a shopping list. It is inteneded for use with demo purposes. The aim is to create this as a docuker container and deploy to the registry to test with Kubernetes.


### TO RUN API

uvicorn main:app --reload

URL = http://localhost:8000/docs#/default/update_item_items__item_id__put


### DOCUMENTATION:

https://fastapi.tiangolo.com/#installation

Run the UVICORN server

uvicorn main:app --reload

### DOCKER

See Dockerfile for configuration.

#### Build the image

sudo docker build -t shoppinglist .

#### Run the container

sudo docker run shoppinglist

#### Push to registry
sudo docker tag shoppinglist thundercatsho/shoppinglist:latest
sudo docker login
sudo docker push thundercatsho/shoppinglist:latest

### DATABASE

Uses postgres, set the following environment varibales to connect in production environment.

ENVIRONMENT=PROD
PROD_HOST
PROD_PORT
PROD_DATABASE
PROD_USER
PROD_PASSWORD