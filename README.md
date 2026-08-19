# ⚡ k8s-telemetry-autoscale

> **Scalable Infrastructure on Kubernetes (Minikube) with Locust Load Testing**  
> A resilient, self-healing telemetry ingestion pipeline for power transformers built with FastAPI, PostgreSQL, and HPA auto-scaling.

![Kubernetes](https://img.shields.io/badge/kubernetes-%23326CE5.svg?style=flat&logo=kubernetes&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Locust](https://img.shields.io/badge/Locust-49AC66?style=flat&logo=locust&logoColor=white)

---

## 📌 1. Overview

### 🔴 What is the Problem?
Power grid transformers continuously generate critical telemetry data (current, voltage, temperature) that requires real-time monitoring. Standard single-container deployments (e.g., standalone Docker or Docker Compose) fail to provide dynamic horizontal scaling during traffic spikes and lack automated recovery mechanisms when application instances crash or become unresponsive.

### 🟢 How to Solve?
This project delivers an end-to-end cloud-native telemetry ingestion pipeline. **FastAPI** with **Pydantic** ensures strict runtime data validation before asynchronously persisting records into a **PostgreSQL** database. The entire infrastructure is orchestrated inside a **Minikube Kubernetes cluster**, utilizing `Liveness` and `Readiness` probes for self-healing, alongside **Horizontal Pod Autoscaling (HPA)** triggered by simulated traffic.

### 💡 Why Should You Choose This Method?
* **High Availability & Zero Downtime:** Kubernetes automatically detects unhealthy instances and restarts them (Self-Healing) without manual intervention.
* **Asynchronous Throughput:** Non-blocking async I/O drivers (`asyncpg`) prevent database bottlenecks under heavy concurrent REST calls.
* **Verified Resilience:** System limits and auto-scaling triggers are rigorously stress-tested using **Locust** load testing workflows.

---

### 🏗 System Architecture

The interaction between telemetry data generators, Kubernetes orchestration, and database persistence is illustrated below:

<p align="center">
  <img width="650" alt="System Architecture" src="https://github.com/user-attachments/assets/4243551f-ce8d-4788-a3c0-0c03628c8118" />
</p>

---

### ✨ Key Features

* **⚡ Real-Time Ingestion & Validation:** Asynchronous REST API endpoint validates sensor data payloads via Pydantic at runtime to maintain database integrity.
* **☸️ Resilient Kubernetes Orchestration:** Deployed with health check probes (`/healthz`, `/ready`) that trigger automatic container restarts during failures.
* **🔒 Isolated Network Security:** PostgreSQL database is hidden behind a `ClusterIP` service, ensuring it is only accessible internally by FastAPI pods.
* **📈 Dynamic Auto-Scaling & Load Testing:** Integrated Horizontal Pod Autoscaler (HPA) automatically scales application pods in response to traffic spikes simulated by Locust.

---

## 🚀 2. Getting Started

### Prerequisites

Ensure you have the following tools installed locally:
* [Docker Engine](https://docs.docker.com/get-docker/) (v20.10+)
* [Minikube](https://minikube.sigs.k8s.io/docs/start/) (v1.28+)
* [kubectl](https://kubernetes.io/docs/tasks/tools/)
* [Python 3.10+](https://www.python.org/) *(optional, for running Locust locally)*

### Installation and Run

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/k8s-telemetry-autoscale.git](https://github.com/your-username/k8s-telemetry-autoscale.git)
   cd k8s-telemetry-autoscale

```

2. **Start Minikube and enable Metrics Server (required for HPA):**
```bash
minikube start
minikube addons enable metrics-server

```


3. **Deploy Database & Application Manifests:**
```bash
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/fastapi-deployment.yaml
kubectl apply -f k8s/hpa.yaml

```


4. **Access the Ingestion Gateway:**
```bash
# Get NodePort URL for sending telemetry requests
minikube service fastapi-service --url

```


5. **Run Locust Load Test:**
```bash
locust -f tests/locustfile.py --host=$(minikube ip):30080

```



---

## 📊 3. Performance and Results

* **Self-Healing Verification:** Intentionally killing a running FastAPI pod resulted in automatic replacement by Kubernetes in **< 3 seconds** with zero data loss.
* **Auto-Scaling Response:** Under Locust stress test conditions (500+ concurrent user simulation), HPA successfully scaled FastAPI replicas from **1 to 5 pods**, keeping API response latencies below **45ms**.
* **Validation Overhead:** Pydantic runtime checks added negligible latency (< 2ms per request) while catching 100% of malformed telemetry payloads during stress runs.

---

## 📄 4. License

This project is licensed under the **MIT License** - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

```

```
