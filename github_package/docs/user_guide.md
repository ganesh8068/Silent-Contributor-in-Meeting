# Silent Contributor Detector

A web application designed to identify and analyze engagement of participants who may not speak much during meetings but contribute in other ways.

## Overview

The Silent Contributor Detector tracks voice participation, analyzes cross-modal contributions, generates engagement scores, includes a nudging system, and provides a dashboard view.

## Key Features

1. **Voice Participation Tracker** - Analyze meeting transcripts/audio to identify speaker activity
2. **Cross-Modal Contribution Analyzer** - Integrate chat logs, shared documents, and task management tools
3. **Engagement Score** - Generate an inclusivity metric per participant based on both verbal and written input
4. **Nudging System** - Gently notify managers about silent contributors
5. **Dashboard View** - Visualize speaking time vs. actual impact

## Live Demo

A static version of the frontend is deployed at: https://kchfqwki.manus.space

Note: This is a static deployment without backend functionality. For full features, follow the local setup guide below.

# Complete Guide to Running Silent Contributor Detector Locally

Here's a comprehensive guide to set up and run the full application (both frontend and backend) on your local machine:

## Step 1: Extract the ZIP File

Extract the `silent_contributor_detector_github.zip` file to a location on your computer.

## Step 2: Set Up the Backend

### Prerequisites:

- Python 3.11 or newer
- MySQL database (or you can use SQLite for testing)

### Backend Setup:

1. **Create a project directory**:

   ```bash
   mkdir -p silent_contributor_detector/backend
   cd silent_contributor_detector/backend
   ```

2. **Copy backend files**:
   Copy all files from the extracted `github_package/backend_src` to your `silent_contributor_detector/backend/src` directory.

3. **Create a virtual environment**:

   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment**:

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. **Install dependencies**:

   ```bash
   pip install Flask==3.1.0 Flask-SQLAlchemy==3.1.1 PyMySQL==1.1.1 SQLAlchemy==2.0.40 bcrypt PyJWT
   ```

6. **Create a file structure like this**:

   ```
   backend/
   ├── src/
   │   ├── models/
   │   ├── routes/
   │   ├── static/
   │   └── main.py
   └── venv/
   ```

7. **Run the backend**:
   ```bash
   cd src
   python main.py
   ```
   The backend should now be running on http://localhost:5000

## Step 3: Set Up the Frontend

### Prerequisites:

- Node.js (v16 or newer)
- npm or pnpm

### Frontend Setup:

1. **Create a project directory**:

   ```bash
   mkdir -p silent_contributor_detector/frontend
   cd silent_contributor_detector/frontend
   ```

2. **Initialize a new React project**:

   ```bash
   npx create-react-app . --template typescript
   ```

   Or if you prefer using Vite:

   ```bash
   npm create vite@latest . -- --template react-ts
   ```

3. **Install dependencies**:

   ```bash
   npm install react-router-dom recharts lucide-react tailwindcss
   ```

4. **Copy frontend files**:
   Copy all files from the extracted `github_package/frontend_src` to your `silent_contributor_detector/frontend/src` directory, replacing the existing files.

5. **Set up Tailwind CSS**:

   ```bash
   npx tailwindcss init -p
   ```

   Create a `tailwind.config.js` file with:

   ```javascript
   module.exports = {
     content: ["./src/**/*.{js,jsx,ts,tsx}"],
     theme: {
       extend: {},
     },
     plugins: [],
   };
   ```

6. **Run the frontend**:
   ```bash
   npm start
   ```
   Or if using Vite:
   ```bash
   npm run dev
   ```
   The frontend should now be running on http://localhost:3000 or http://localhost:5173 (for Vite)

## Step 4: Connect Frontend to Backend

1. **Update API endpoints**:
   In your frontend code, ensure API calls point to your local backend:

   ```javascript
   // Example API call
   fetch("http://localhost:5000/api/meetings")
     .then((response) => response.json())
     .then((data) => console.log(data));
   ```

2. **Enable CORS on backend**:
   Add this to your Flask backend:

   ```python
   from flask_cors import CORS

   app = Flask(__name__)
   CORS(app)  # Enable CORS for all routes
   ```

   Install the CORS extension:

   ```bash
   pip install flask-cors
   ```

## Step 5: Testing the Application

1. **Register a new user**:

   - Navigate to http://localhost:3000 (or your frontend URL)
   - Click "Don't have an account? Register"
   - Fill in the registration form
   - Submit the form to create a new user

2. **Login with your credentials**:

   - Use the username and password you just created
   - You should be redirected to the dashboard

3. **Explore the features**:
   - View the silent contributor dashboard
   - Check the analytics tab
   - Test all functionality

## Troubleshooting

1. **Database issues**:

   - Ensure MySQL is running
   - Check database connection string in `backend/src/main.py`
   - For testing, you can switch to SQLite by changing the connection string

2. **CORS errors**:

   - Verify CORS is properly configured on the backend
   - Check that API URLs are correct in frontend code

3. **Missing dependencies**:
   - Run `pip freeze > requirements.txt` to generate a complete list of backend dependencies
   - Run `npm list --depth=0` to see frontend dependencies

## Project Structure

- `backend_src/`: Contains the Flask backend code
- `frontend_src/`: Contains the React frontend code
- `docs/`: Contains documentation including architecture, user guide, and feature validation

## License

This project is available for personal and commercial use.
