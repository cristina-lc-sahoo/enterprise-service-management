# Enterprise Service Management

A hands-on application project for managing support users and tickets, built with **Python, FastAPI, and PostgreSQL**. The project is also used to practice containerization with Docker and application deployment with Kubernetes.

## Project Overview

The application provides a simple web interface and REST API for common enterprise support workflows, including:

- Viewing and managing users
- Updating user information
- Creating and retrieving support tickets
- Assigning tickets to support engineers
- Retrieving tickets assigned to a particular engineer
- Persisting application data in PostgreSQL

The frontend is served by the FastAPI application. API endpoints can also be explored through FastAPI's automatically generated Swagger UI.

## Technology Stack

| Area | Technologies |
|---|---|
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| Database integration | SQLAlchemy |
| API documentation | Swagger UI / OpenAPI |
| Frontend | HTML, CSS, JavaScript |
| Containerization | Docker |
| Orchestration | Kubernetes |
| Configuration | Environment variables, Kubernetes ConfigMap |

## Architecture

The application runs as a FastAPI service and connects to PostgreSQL for persistent storage.

```text
Browser
   |
   v
FastAPI web application and REST API
   |
   v
SQLAlchemy
   |
   v
PostgreSQL

Docker image
   |
   v
Kubernetes Deployment
   |
   v
Application Pod
   |
   v
Kubernetes ClusterIP Service
```

For local Kubernetes testing with Docker Desktop, the application is exposed to the Mac through `kubectl port-forward`. The Kubernetes Service provides a stable internal endpoint and routes traffic to Pods selected by their application label.

## Running Locally

### Prerequisites

- Python
- PostgreSQL
- Git

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd enterprise-service-management
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database

Create a local `.env` file in the project root. Use the variable names expected by the application:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=enterprise_service_management
DB_USER=<your_postgresql_username>
DB_PASSWORD=<your_postgresql_password>
```

Use your own local PostgreSQL settings. Do not commit `.env` or real credentials to GitHub.

### 5. Start the application

From the project root:

```bash
uvicorn app.main:app --reload
```

Open the application:

- Web interface: http://localhost:8000
- API documentation: http://localhost:8000/docs

## Running with Docker

Build the image from the project root:

```bash
docker build -t enterprise-service-management:v1 .
```

For local Docker Desktop networking, the container can reach PostgreSQL running on the Mac through `host.docker.internal`. Create a separate `.env.docker` file with the appropriate database settings. Keep credentials out of source control.

Run the container:

```bash
docker run -d \
  -p 8000:8000 \
  --env-file .env.docker \
  --name enterprise-service-management \
  enterprise-service-management:v1
```

Open http://localhost:8000 to use the application.

To view container logs:

```bash
docker logs enterprise-service-management
```

To stop the container:

```bash
docker stop enterprise-service-management
```

## Running with Kubernetes

The project includes Kubernetes manifests for the application Deployment, database configuration, and Service.

### 1. Apply the database configuration

```bash
kubectl apply -f configmap.yaml
```

The ConfigMap supplies the database environment variables to the application container. Do not put real passwords or other sensitive values in a ConfigMap. Use a Kubernetes Secret for credentials when needed.

### 2. Deploy the application

```bash
kubectl apply -f deployment.yaml
```

### 3. Create the Kubernetes Service

```bash
kubectl apply -f service.yaml
```

### 4. Check the deployment

```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

The Pod should reach `Running` status and show `1/1` ready when the application container is healthy.

### 5. Access the application locally

For local testing with Docker Desktop Kubernetes:

```bash
kubectl port-forward service/enterprise-service-management 8000:8000
```

Then open:

- Web interface: http://localhost:8000
- API documentation: http://localhost:8000/docs

Port forwarding provides temporary access from the local machine. The Pod, Deployment, and ClusterIP Service continue running in Kubernetes when the port-forward process is stopped.

## Kubernetes Concepts Practiced

- **Deployment:** Defines the desired application state and manages Pod replicas.
- **Pod:** Runs the application container.
- **ConfigMap:** Supplies non-sensitive configuration through environment variables.
- **Service (ClusterIP):** Provides a stable internal endpoint and routes traffic to matching Pods.
- **Port forwarding:** Enables local access to an application running inside the local Kubernetes cluster.

## Planned Enhancements

The following capabilities are planned and are not yet implemented:

- Add secure user authentication and password hashing.
- Implement token-based authentication using OAuth2 and JWT.
- Add role-based access control (RBAC) for administrator, manager, and support roles.
- Restrict API operations according to user roles and permissions.
- Add automated tests for authentication, authorization, API behavior, and database operations.
- Improve Kubernetes deployment configuration with health probes and production-oriented configuration.
- Evaluate external access options such as Ingress or a cloud load balancer for a future cloud deployment.

## Project Purpose

This project is a practical learning exercise in building and operating a database-backed API application. It brings together backend development, relational database integration, Docker image creation, Kubernetes deployment, configuration management, and application troubleshooting.

---

**Note:** This project currently demonstrates local development and local Docker Desktop Kubernetes deployment. It is not presented as a production-hosted service.
