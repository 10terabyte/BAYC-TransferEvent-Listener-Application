
# TransferEvent Listener Application

This Django application listens for `Bored Ape Yacht Club (BAYC)` Transfer events from the Ethereum blockchain via WebSocket using `AsyncWeb3` and `Infura`. It stores the transfer events in an SQLite database and provides an API to retrieve the history of transfers for a given token ID.

## Table of Contents
- Prerequisites
- Installation
- Configuration
- Running the Application
- API Usage
- Assumptions and Simplifications

## Prerequisites

Before setting up the project, ensure you have the following installed on your machine:
- Python 3.8+
- Django 5+
- Infura account for Ethereum WebSocket API
- `pipenv` or `virtualenv` for virtual environments (optional but recommended)

## Installation

Follow the steps below to set up and run the project:

1. **Clone the Repository:**
   ```
   git clone https://github.com/10terabyte/BAYC-TransferEvent-Listener-Application
   cd BAYC-TransferEvent-Listener-Application
   ```

2. **Set Up Virtual Environment (Optional):**
   ```
   pipenv shell
   ```

3. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Create a `.env` File:**
   In the project root directory, create a `.env` file with the following content (replace the placeholder values with your actual credentials):
   ```
   INFURA_PROJECT_ID=your_infura_project_id
   BAYC_CONTRACT_ADDRESS=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
   ```

5. **Apply Database Migrations:**

   First, generate the migration files for the database:
   ```
   python manage.py makemigrations
   ```

   Then, apply the migrations to create the necessary database tables:
   ```
   python manage.py migrate
   ```

6. **Load Past Events (Optional):**
   If you wish to fetch past transfer events for a given range of blocks, modify the `START_BLOCK` and `END_BLOCK` in the `fetch_past_events()` function in the command file and run:
   ```
   python manage.py load_past_events
   ```

## Configuration

- **Infura Setup:** Sign up at [Infura.io](https://infura.io/) to get your project ID and WebSocket URL for connecting to the Ethereum mainnet.
- **Database Configuration:** The project uses SQLite as the default database, and no additional setup is needed unless you prefer a different database. You can configure the database in `settings.py` if needed.

## Running the Application

1. **Start Django Development Server:**
   ```
   python manage.py runserver
   ```

2. **Run the Transfer Event Listener:**
   To start listening for BAYC transfer events on Ethereum, run the custom Django management command:
   ```
   python manage.py listen_for_events
   ```

## API Usage

- **Get Transfer History for a Token ID:**
   The application exposes a REST API endpoint to get the transfer history for a specific token. You can use this by making a GET request to:

   ```
   GET /api/transfers/<token_id>/
   ```

   Example:
   ```
   curl http://127.0.0.1:8000/api/transfers/12345/
   ```

   This will return a list of all transfers associated with the given `token_id`.

## Assumptions and Simplifications

1. **Infura API**: The application assumes the use of Infura's WebSocket API for connecting to the Ethereum network. Other Ethereum providers or nodes can be used with modifications.
   
2. **Ethereum Blockchain Data**: The application only fetches and listens for `Transfer` events from the `BAYC` contract. No other contract or event types are handled.

3. **Data Storage**: Events are stored in an SQLite database, which is suitable for local development. If you plan to deploy this in production, consider using a more robust database like PostgreSQL.

4. **Error Handling**: The application implements basic error handling, but in production scenarios, more sophisticated logging and retry mechanisms should be used to handle WebSocket disconnections and database integrity errors.

5. **Block Ranges for Past Events**: When fetching past events, a block range (`START_BLOCK` and `END_BLOCK`) is manually set in the management command. This can be automated or modified to pull data incrementally if needed.

## Conclusion

This project provides a simple framework for interacting with the Ethereum blockchain to monitor and store transfer events for specific tokens. You can expand it by adding more features, such as additional event types, support for multiple contracts, or user authentication.
