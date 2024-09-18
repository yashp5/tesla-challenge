# Tesla Challenge

This project is a site layout webpage that allows users to mockup the build of materials and site layout for an Industrial Energy Battery site.

## Table of Contents
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Docker](#docker)
  - [Manual Setup](#manual-setup)
    - [Backend](#backend)
    - [Frontend](#frontend)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Future Improvements](#future-improvements)

## Project Structure

The project is divided into two main parts:
- `backend`: Python-based backend service
- `frontend`: React-based frontend application

## Getting Started

### Docker

The project includes Dockerfiles for both backend and frontend, as well as a `docker-compose.yml` file for easy deployment.

To run the entire application using Docker:
1. Navigate to the root directory
2. Run `docker-compose up --build`

### Manual Setup

#### Backend

1. Navigate to the `backend` directory
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```
3. Install dependencies: `pip install -r requirements.txt`

#### Frontend

1. Navigate to the `frontend` directory
2. Install dependencies: `npm install`

## Running the Application

### Docker
Follow the Docker instructions in the [Getting Started](#docker) section.

### Manual
1. Start both the backend and frontend:
   ```bash
   cd frontend
   npm run start
   ```

## Testing

To run the backend tests:
1. Navigate to the `backend` directory
2. Run `pytest`

## Future Improvements

### Frontend
- Improve layout scaling for a large number of objects
- Ensure consistent scaling of same-size objects
- Enhance visual appeal with images

### Backend
- Implement object rotation
- Research and implement better object placement strategies
- Account for space between objects
- Improve test coverage



