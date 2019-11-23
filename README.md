# TCC API

This repository contains a basic flask API.


## Setup

- Ensure you have the right versions of the dependencies. Run:

    ```bash
    pip install -r requirements.txt
    ```
- Create a `.env` file using the `.env.sample`:

    ```bash
    cp .env.sample .env
    ```
- Set the variables at the `.env` file

- If there is a version of docker installed on the machine, you can run a Postgres Container:

  ```bash
    docker-compose up -d
    ```

- If needed, create migrations by running:

    ```bash
    flask db migrate
    ```
- Then, update the database:

  ```bash
    flask db upgrade
    ```