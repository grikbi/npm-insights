# npm-insights

This repository contains the code that is used to power NPM package companion
recommendations.
The approached used is based off of CVAE, see citation below.

```
Li, Xiaopeng, and James She. "Collaborative variational autoencoder for recommender systems."  
In Proceedings of the 23rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining,  
pp. 305-314. ACM, 2017.
```

It also requires graph services `gremlin-http` to work in tandem with npm-insights to provide end-users a companion recommendation with a specific version.

## Data set

- It consists of trained model comprising of 29k unique packages and around 29k user-item matrix known as a stack in developer's parlance.
- Graph data consists of a subset of packages based on the manifests received on [Dependency Analytics Platform](https://marketplace.visualstudio.com/items?itemName=redhat.fabric8-analytics).

### Run this locally via container

- cd to root directory
- docker-compose up -d
- Acces the service at `http://localhost:6005`

### Swagger

Swagger is available at `/docs` and redoc is available at `/redoc` endpoint.

### Run the tests locally

- cd to root directory
- sh runtest.sh

## LICENSE

Licensed under the GNU GPL v3.0, copyright Red Hat Inc., 2018. Licenses for vendor code are included in the respective files/folders.
