# Airflow Deployment Guide

This guide provides step-by-step instructions on how to deploy the Airflow setup.

## Prerequisites

- Docker installed
- Docker Compose installed

## Steps to Deploy

1. **Bring Down Existing Docker Containers**

    Ensure any existing Docker containers are stopped and removed:

    ```sh
    docker-compose down -v
    ```

2. **Initialize Airflow**

    Initialize the Airflow database and other configurations:

    ```sh
    docker-compose up airflow-init
    ```

3. **Start Airflow Services**

    Start the Airflow services in detached mode:

    ```sh
    docker-compose up -d
    ```

## Accessing Airflow

Once the services are up and running, you can access the Airflow web interface by navigating to `http://localhost:8080` in your web browser.

## Stopping Airflow

To stop the Airflow services, run:

```sh
docker-compose down
```

## Environment Configuration

Ensure you have a `.env` file in the root directory with the following content:

```env
DATABASE_URL=your_database_url
```

The database specified by `DATABASE_URL` should have a table named `ticker_quotes` defined.

## Additional Information

For more detailed information, refer to the official [Airflow documentation](https://airflow.apache.org/docs/).

