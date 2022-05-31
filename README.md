# ls-auth-api

This repository is part of the skillsgraph project created by LearnerShape with support from Cardano Project Catalyst. Our project proposal can be found [here](https://cardano.ideascale.com/c/idea/368250).

ls-auth-api is intended to provide a flexible backend to support different skills authentication use cases and user interfaces. We currently have one [user interface](https://github.com/LearnerShape/ls-auth-ui) that supports peer-to-peer and small group skills authentication.

## Run with docker-compose

The easiest way to get started is with docker-compose.

To install docker-compose, instructions are available [here](https://docs.docker.com/compose/install/).

To interact with Atala Prism  you will need their SDK. This is automatically downloaded during the build process but requires you to have and set the `PRISM_SDK_PASSWORD` environment variable.

The images can then be built with:

```
docker-compose build
```

To facilitate communication between ls-auth-api and ls-auth-ui they are configured to use a shared network. This can be created with:

```
docker network create ui-api-bridge
```

Finally the services can be started with:

```
docker-compose up
```

The API will then be accessible at http://localhost:5000/

Some of the other containers also have publicly accessible interfaces:
* If desired, the low-level Atala Prism commands can be accessed at http://localhost:8080
* The database is accessible on port `5432` and user postgres, database postgres
* The task queue is managed using a rabbitmq broker, accessible at http://localhost:15672 using the default guest username and password.


# Contributing

For guidance on reporting issues, suggesting new features and contributing to project development, see the [contributing guidelines](https://github.com/LearnerShape/ls-auth-api/blob/main/CONTRIBUTING.md).
