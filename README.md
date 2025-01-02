# FastAPI Application

## Overview

This is a FastAPI application designed to [brief description of what your application does].

## Features

- has only one api -> /chat takes query

## Installation

Follow these steps to set up the project on your local machine.

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Steps

1. Clone the repository:

    ```bash
    git clone git@github.com:MahmoudEzz/Kagool-chat-bot.git
    cd your-dir
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate # On Windows, use `env\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file and add your environment variables:

    ```plaintext
    OPENAI_AZURE_END_POINT = open_ai_url
    OPENAI_API_KEY= api_key
    OPENAI_API_VERSION= 2024-..
    OPENAI_MODEL= gpt-4
    BACKEND_URL= http://127.0.0.1:8000 
    ```

## Running the Backend

To run the FastAPI application, use the following command:

```bash
fastapi dev main.py
```
## Running the Frontend

To run the FastAPI application, use the following command:

```bash
streamlit run streamlt.py
```
