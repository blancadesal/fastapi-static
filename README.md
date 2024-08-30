# Toolforge Python ASGI Tutorial

This is a simple FastAPI application that fetches random quotes from the Quotable API and displays them on a web page.

## Features

- Backend API endpoint to fetch random quotes
- Frontend interface to display quotes and request new ones
- Health check endpoint
- Auto-generated API documentation

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

This application has only been tested with Python 3.11 and later.
You can check your Python version by running:

```bash
python --version
```

You will also need to install `poetry` to manage the dependencies. <https://python-poetry.org/>

### Installing

Clone the repository:

```bash
git clone https://gitlab.wikimedia.org/toolforge-repos/sample-python-buildpack-asgi.git
cd sample-python-buildpack-asgi
```

Install the required packages:

```bash
poetry install
```

## Running the Application

Start the development server:

```bash
poetry run fastapi dev
```

The application will start running at <http://127.0.0.1:8000/>

If you need it to run on a different port, you can specify the port number:

```bash
fastapi dev --port 8080
```

## Usage

- Open your web browser and navigate to <http://127.0.0.1:8000/>
- You will see a random quote displayed on the page
- Click the "New Quote" button to fetch and display a new random quote

## API Endpoints

- GET /: Serves the main HTML page with the quote interface
- GET /quote: Returns a JSON object containing a random quote

The API documentation (Swagger UI) is available at <http://127.0.0.1:8000/docs>

## Project Structure

- `app.py`: The main FastAPI application file
- `static/index.html`: The HTML file for the frontend interface
- `requirements.txt`: List of Python dependencies
- `Procfile`: Configuration file for deployment to Toolforge using the Build Service

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Tutorial

For the full tutorial on how to deploy the app on Toolforge, see [My first buildpack Python ASGI tool](https://wikitech.wikimedia.org/w/index.php?title=Help:Toolforge/Build_Service/My_first_Buildpack_Python_ASGI_tool).
