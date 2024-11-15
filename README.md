Here’s a README file that’s detailed, concise, and organized to make the project easy to understand and run.

---

# Receipt Processor API

This is a FastAPI-based web service for processing receipts and calculating reward points based on defined criteria. The API accepts receipt data, calculates points, and provides the total points for each receipt.

## Table of Contents

- [Project Overview](#project-overview)
- [Installation and Setup](#installation-and-setup)
- [Running the Application](#running-the-application)
- [Testing the Application](#testing-the-application)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)

---

## Project Overview

The Receipt Processor API provides two main endpoints:
1. **POST /receipts/process** - Processes receipt data and returns a unique ID for each receipt.
2. **GET /receipts/{id}/points** - Returns the points awarded for a given receipt by its ID.

Points are calculated based on rules outlined in the `README.md`, including points for retailer name length, total amount, item counts, and purchase time.

---

## Installation and Setup

### Prerequisites

- **Python 3.10** or higher
- **FastAPI** and **Uvicorn** (for running the server)
- **Docker** (optional, for containerized execution)

### 1. Clone the Repository

```bash
git clone 
cd receipt-processor
```

### 2. Set Up a Virtual Environment

Create and activate a virtual environment to install dependencies.

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Running the Application

To start the server locally, use the following command:

```bash
uvicorn app.main:app --reload
```

- The API will be available at **http://127.0.0.1:8000**.
- Swagger UI documentation is accessible at **http://127.0.0.1:8000/docs** for interactive testing.

### Running with Docker (Optional)

To run the application in a Docker container:

1. **Build the Docker image**:

    ```bash
    docker build -t receipt-processor .
    ```

2. **Run the Docker container**:

    ```bash
    docker run -p 8000:8000 receipt-processor
    ```

---

## Testing the Application

### Running Tests

The application includes comprehensive tests located in the `tests/` directory. These tests cover all rules for point calculation.

1. **Run Tests with Pytest**:

    ```bash
    PYTHONPATH=$(pwd) pytest tests/
    ```

2. **Check Output**: The tests will verify functionality and report results.

---

## API Documentation

### 1. **Process Receipts**

- **Endpoint**: `/receipts/process`
- **Method**: `POST`
- **Description**: Takes in a receipt JSON payload, calculates points, and returns a unique ID.
- **Request Body Example**:

    ```json
    {
      "retailer": "Target",
      "purchaseDate": "2022-01-01",
      "purchaseTime": "13:01",
      "items": [
        {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
        {"shortDescription": "Emils Cheese Pizza", "price": "12.25"}
      ],
      "total": "35.35"
    }
    ```

- **Response Example**:

    ```json
    { "id": "7fb1377b-b223-49d9-a31a-5a02701dd310" }
    ```

### 2. **Get Points**

- **Endpoint**: `/receipts/{id}/points`
- **Method**: `GET`
- **Description**: Retrieves the points awarded for a receipt by its ID.
- **Response Example**:

    ```json
    { "points": 20 }
    ```

---

## Project Structure

The project is divided into specific directories for modularity, readability, and maintainability:

```plaintext
receipt-processor/
│
├── app/
│   ├── main.py                   # Entry point for FastAPI application.
|   ├── controllers/
│   │   └── receipt_controller.py  # Defines the API endpoints for processing receipts and retrieving points.
│   ├── models/
│   │   └── receipt.py             # Data models for Receipt and Item, defined with Pydantic for data validation.
│   ├── services/
│   │   └── receipt_service.py     # Core business logic for calculating points based on receipt data.
│   └── utils/
│       └── id_generator.py        # Utility for generating unique IDs for receipts.
│
├── tests/
│   ├── test_receipt_controller.py # Tests for API endpoints and overall integration.
│   └── test_receipt_service.py    # Unit tests for individual functions in receipt_service.py.
│
├── requirements.txt               # Lists all dependencies required to run the project.
├── Dockerfile                     # Docker configuration for containerized deployment.
└── README.md                      # Project documentation.
```

### Explanation of Folder Structure

1. **app/main.py**: The main entry point that initializes the FastAPI application and sets up routes.

2. **app/controllers**: Contains receipt_controller.py, which defines the API endpoints. This file handles HTTP requests for processing receipts and retrieving points based on receipt ID. By separating controller logic, we make it easy to update or add routes without impacting other parts of the application.
  
3. **app/models**: Contains the data models for `Receipt` and `Item`. Pydantic is used to enforce data structure and validate incoming request data.

4. **app/services**: Houses the `receipt_service.py`, which contains the core logic for calculating points. This separation allows business logic to remain modular, testable, and reusable.

5. **app/utils**: Contains helper utilities like `id_generator.py` for generating unique IDs. Isolating utilities makes the codebase cleaner and more organized.

6. **tests/**: The `tests` folder is split into `test_receipt_controller.py` and `test_receipt_service.py` for clear separation between endpoint testing and business logic testing. This ensures that each component can be individually verified.

## Additional Notes

- **Points Calculation**: The application awards points based on rules outlined in the `README.md`.
- **In-Memory Data**: Data is stored in memory, per the requirements, meaning data is reset upon application restart.
- **Interactive Documentation**: FastAPI’s built-in Swagger UI makes it easy to interact with and test the API.
