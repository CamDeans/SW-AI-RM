# Swarm AI Development System

This project implements a Swarm AI Development System that simulates a team of AI agents collaborating to build software projects. The system is structured around the Flower of Life concept, with a central "Lead Developer" agent coordinating specialized agent roles.

## Project Structure

The project is divided into two main parts:

1. Backend: A Flask-based Python application that handles the core logic of the swarm AI system.
2. Frontend: A React-based web application that provides a user interface for interacting with the swarm.

## Implementation and Running Guide

### Prerequisites

Ensure you have the following installed on your system:
- Python 3.7 or higher
- Node.js 12 or higher
- npm (usually comes with Node.js)

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

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

4. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

5. Set up the environment variables:
   - Create a `.env` file in the `backend` directory if it doesn't exist.
   - Add the following content to the `.env` file:
     ```
     ANTHROPIC_API_KEY=your_api_key_here
     FLASK_APP=app.py
     FLASK_ENV=development
     SECRET_KEY=your_secret_key_here
     ```
   - Replace `your_api_key_here` with your actual Anthropic API key.
   - Replace `your_secret_key_here` with a secure random string.

6. Run the Flask application:
   ```
   flask run
   ```

The backend should now be running on `http://localhost:5000`.

### Frontend Setup

1. Open a new terminal window and navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install the required npm packages:
   ```
   npm install
   ```

3. Set up the environment variables:
   - Create a `.env` file in the `frontend` directory if it doesn't exist.
   - Add the following content to the `.env` file:
     ```
     REACT_APP_API_URL=http://localhost:5000
     ```

4. Start the React development server:
   ```
   npm start
   ```

The frontend should now be running on `http://localhost:3000`.

## Using the System

1. Open your web browser and go to `http://localhost:3000`.

2. You should see the Swarm AI Development System interface.

3. Use the interface to:
   - Create new agents
   - Assign tasks
   - Monitor the swarm's progress
   - Generate project artifacts

4. The backend API endpoints are available at `http://localhost:5000` if you need to interact with them directly.

## Troubleshooting

- If you encounter any CORS issues, you may need to add CORS support to the backend. Install the Flask-CORS package and update `app.py` to use it.

- Make sure both the backend and frontend are running simultaneously for the system to work properly.

- Check the console logs in both the backend terminal and the browser's developer tools for any error messages.

## Next Steps

- Implement proper error handling and logging in both backend and frontend.
- Add user authentication and authorization.
- Enhance the UI with more interactive features and real-time updates.
- Implement a database for persistent storage of agents, tasks, and artifacts.

## Contributing

Contributions to the Swarm AI Development System are welcome. Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details."# SW-AI-RM" 
