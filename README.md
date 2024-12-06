# TripPlanner Project

## Overview
This project consists of a frontend and a backend, built using Django and Nuxt respectively. You can either use Docker Compose
to run the entire project without installing dependencies on your local machine, or follow the installation instructions
provided in the `README.md` files within the `front` and `back` directories.

## Prerequisites
- Docker
- Docker Compose

## Running the Project with Docker Compose
To run the project using Docker Compose, follow these steps:

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd TripPlanner
    ```

2. Build and start the containers:
    ```sh
    docker-compose up --build
    ```

3. Access the frontend application at `http://localhost:3000` and the backend API at `http://localhost:8000`.

**Note:** The database is not dockerized yet !

## Manual Installation
If you prefer to install the dependencies manually, please refer to the `README.md` files in the `front` and `back` directories for detailed instructions.

- [Frontend Installation](front/README.md)
- [Backend Installation](back/README.md)

## Additional Information
- The frontend is built using Vue.js and Nuxt.js.
- The backend is built using Python and Django.

Let's get started ! 🚀