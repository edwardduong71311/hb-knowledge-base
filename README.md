# Health Buddy Knowledge Base

## Description
Health Buddy Knowledge Base is a FastAPI-based project designed to manage and process health-related knowledge efficiently. This project is structured as a PDM package and supports seamless dependency management and script execution.

## Requirements
- Python 3.13
- PDM for package management

## Installation
Ensure you have PDM installed. If not, install it using:
```sh
pip install pdm
```

Clone the repository and install dependencies:
```sh
git clone <repository-url>
cd health-buddy-knowledge-base
pdm install
```

## Project Structure
```
health-buddy-knowledge-base/
├── src/
│   ├── main.py          # Entry point for FastAPI application
│   ├── sync_data.py     # Script to sync data
│   ├── sync_vector.py   # Script to sync vector data
│   ├── sync_chroma_db.py# Script to sync Chroma DB
├── pyproject.toml       # Project configuration
├── README.md            # Documentation
```

## Running the Application
### Development Mode
Run the application in development mode:
```sh
pdm run dev
```

### Production Mode
Run the application with Uvicorn:
```sh
pdm run start
```

## Scripts
The project includes predefined scripts for ease of execution:
- **sync_data**: Syncs data
  ```sh
  pdm run sync_data
  ```
- **sync_vector**: Syncs vector data
  ```sh
  pdm run sync_vector
  ```
- **sync_chroma**: Syncs ChromaDB
  ```sh
  pdm run sync_chroma
  ```
- **check**: Runs `ruff` to check and fix linting issues
  ```sh
  pdm run check
  ```
- **format**: Formats the code using `ruff`
  ```sh
  pdm run format
  ```

## License
This project is licensed under the MIT License.

