# Tesla Challenge

This project is a site layout webpage that allows users to mockup the build of materials and site layout for an Industrial Energy Battery site.

## Project Structure

The project is divided into two main parts:

- `backend`: Python-based backend service
- `frontend`: React-based frontend application

## Running the Application

## Docker

The project includes Dockerfiles for both backend and frontend, as well as a `docker-compose.yml` file for easy deployment.

To run the entire application using Docker:
1. Navigate to the root directory
2. Run `docker-compose up --build`

### Backend

To run the backend:

1. Navigate to the `backend` directory
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `python main.py`

### Frontend

To run the frontend:

1. Navigate to the `frontend` directory
2. Install dependencies: `npm install`
3. Start the development server: `npm run start:frontend`

### Running the entire application

1. Install dependencies for both frontend and backend with the above instructions
2. Navigate to the `frontend` directory
3. Start the development server: `npm run start`


