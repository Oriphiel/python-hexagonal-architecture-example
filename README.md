# Hexagonal Architecture Example: E-commerce Discounts API
This repository provides a clear and practical implementation of the Hexagonal Architecture (also known as the Ports and Adapters pattern) using Python. The project is a simple yet robust API for managing e-commerce discounts, designed to showcase how to keep the core application logic (the domain) completely isolated from external infrastructure concerns like web frameworks, databases, or message brokers.

### Key goals of this project:

**🎯 Domain-Centric**: The business logic is pure and has no dependencies on external frameworks.

**🔌 Decoupled Infrastructure**: Adapters for FastAPI, in-memory repositories, and log-based event publishers can be swapped out with zero changes to the core application.

**🧪 High Testability**: The separation of concerns makes the core logic and application services extremely easy to unit test.

---


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Make sure you have the following installed on your system:
*   Python 3.8+
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository** to your local machine:
    ```bash
    git clone <your-repository-url>
    cd ecommerce_discounts
    ```

2.  **Create and activate a virtual environment** (recommended):
    *   On macOS and Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install the required dependencies** from the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

The application has two different entry points (input adapters): a REST API and a command-line batch process.

### 1. Running the API Server

This will start the FastAPI web server, allowing you to interact with the application via HTTP requests.

*   Run the following command from the root directory (`ecommerce_discounts/`):
    ```bash
    uvicorn main:app --reload
    ```
*   The server will start, and the API will be available at `http://127.0.0.1:8000`.
*   The `--reload` flag enables auto-reloading, so the server will restart automatically whenever you save a change in the code.

### 2. Running the Batch Process

This script simulates a scheduled job that creates discounts, using the same core application logic as the API.

*   **Open a new terminal window** (keep the API server running in the first one).
*   Make sure your virtual environment is activated in the new terminal.
*   Run the batch script with the following command:
    ```bash
    python src/discounts/adapters/input/batch/create_seasonal_discounts.py
    ```

## How to Use and Test

### Interacting with the API

The easiest way to test the API is through the interactive documentation provided by Swagger UI.

1.  With the server running, open your web browser and navigate to:
    **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

2.  **Create a new discount:**
    *   Expand the `POST /api/discounts` endpoint.
    *   Click "Try it out".
    *   Modify the request body to create a new discount, for example:
        ```json
        {
          "code": "WELCOME10",
          "percentage": 10
        }
        ```
    *   Click "Execute". You should receive a `201 Created` response.
    *   **Check the Uvicorn terminal.** You will see detailed log messages showing the flow: `API Adapter -> Service -> Repository Adapter`.

3.  **Request a discount validation:**
    *   Expand the `POST /api/validate-discount` endpoint.
    *   Click "Try it out".
    *   Fill in the details, using the code you just created:
        ```json
        {
          "code": "WELCOME10",
          "cart_id": "cart-123",
          "total_amount": 150.5,
          "user_id": "user-abc"
        }
        ```
    *   Click "Execute". You will get an immediate `202 Accepted` response.
    *   **Check the Uvicorn terminal.** You will see logs showing that the request was received and an event was published to the "Log Publisher", simulating an asynchronous process.

### Observing the Batch Job

1.  Run the batch script as described in the section above.
2.  Observe the output in its terminal. You will see logs from the "Batch Adapter" as it tries to create seasonal discounts like `VERANO25`.
3.  If you try to run the batch script a second time, it will fail to create the same discounts, demonstrating that the core domain logic (`"discount code already exists"`) is being correctly applied, regardless of which adapter is calling it.

---

## ✍️ Author

*   **A. H.** - [github.com/oriphiel](https://github.com/oriphiel)