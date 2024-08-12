# Production Plan API

## Description

This API is designed to receive a `POST` request at the `/productionplan` endpoint with a json following the same structure as the example_payloads/payload1.json. It is built using FastAPI and configured to run on the local IP address (`127.0.0.1`) and port `8888`.

## Prerequisites

- **Python 3.8+**: You can verify your Python version by running the following command:

  ```bash
  python --version

## Clone the repository:

git clone <REPOSITORY_URL>
cd <DIRECTORY_NAME>

## Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

## Install dependencies:

pip install -r requirements.txt

## Running the API

uvicorn main:app --host 127.0.0.1 --port 8888

## Example using Postman:

Open Postman.
Select the POST method.
Enter the URL http://127.0.0.1:8888/productionplan.
Go to the "Body" tab and select "raw" and "JSON".
Enter the file example_payloads/payload1.json or a similar one.
Click "Send".


