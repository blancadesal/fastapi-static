# Toolforge Python ASGI Tutorial

This is a simple FastAPI application that fetches a random quote from the Quotable API.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need Python 3.7 or later to run this application. You can check your Python version by running:

```bash
python --version
```

### Installing

First, clone the repository to your local machine:

```bash
git clone https://gitlab.wikimedia.org/toolforge-repos/sample-python-buildpack-asgi.git
cd sample-python-buildpack-asgi
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Application

You can start the development server by running:

```bash
uvicorn app:app --reload
```

The application will start running at <http://127.0.0.1:8000/>.

## Endpoints

- GET /: Returns a simple greeting.
- GET /quote: Fetches and returns a random quote from the Quotable API.

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Tutorial

For the full tutorial on how to deploy the app on Tooloforge, see [My first buildpack Python ASGI tool](https://wikitech.wikimedia.org/w/index.php?title=Help:Toolforge/Build_Service/My_first_Buildpack_Python_ASGI_tool).
