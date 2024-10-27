# WishMe API

WishMe API is an HTTP REST API that facilitates the placing of wishes within KOLO's WishMe system.

## Build With

1. [Python](https://www.python.org/)
2. [FastAPI](https://fastapi.tiangolo.com/)
3. [PostgreSQL](https://www.postgresql.org/)
4. [Docker](https://www.docker.com/)

## Getting Started

To install and run the application, you need to install a few prerequisites and follow a couple of steps.

### Prerequisites

Install the following programs:

* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)

### Build & Run

The installation of the application is straightforward since it is dockerized. These are the steps to build and run the application:

1. Create `.env` file and place the following variables inside of it:

    ```sh
    JWT_SECRET_KEY="very_secret_key_to_change"  # You need to change this!!
    JWT_ALGORITHM="HS256"  # You can change this
    ACCESS_TOKEN_EXPIRE_MINUTES=30  # You can change this
    ```

2. Build the application:

    ```sh
    docker-compose build
    ```

3. Run the application:

    ```sh
    docker-compose up
    ```

All done! The application is available under <http://0.0.0.0:8000>. You can test the API and see docs via [Swagger](https://swagger.io/tools/swagger-ui/) when you access <http://0.0.0.0:8000/docs>.

## Docs

Docs are deployed and accessible at the [following link](https://patrotom.github.io/kolo-wishme/#/).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Tomáš Patro - <tomas.patro@gmail.com>
