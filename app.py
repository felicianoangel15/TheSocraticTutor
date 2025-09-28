import os
import time
import requests
# Added render_template to serve the index.html file
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

# --- CRITICAL: FLASK SETUP AND CONFIGURATION ---
app = Flask(__name__)

# NOTE: In a real environment, these environment variables must be set correctly
# for the GCP/Discovery Engine API calls to work. They are simulated here.
GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID', 'your-gcp-project-id')
GCS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME', 'your-gcs-bucket-name')
PERMANENT_DATA_STORE_ID = 'document-data_1759014897974' # Matches the ID in index.html for clarity

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Checks if a file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- SIMULATED GCP FUNCTIONS (Replace with actual GCP SDK logic) ---

def simulate_upload_to_gcs(filepath, filename):
    """Simulates uploading a file to Google Cloud Storage (GCS)."""
    # NOTE: In a real application, you would use google.cloud.storage here
    print(f"Simulating GCS upload of {filename}...")
    time.sleep(1) # Simulate network delay
    # Full path in GCS will be 'gs://{GCS_BUCKET_NAME}/{filename}'
    return f"gs://{GCS_BUCKET_NAME}/{filename}"

def simulate_data_store_import(gcs_uri, data_store_id):
    """Simulates starting the import job for the Discovery Engine Data Store."""
    # NOTE: In a real application, you would use Discovery Engine API here
    print(f"Simulating Discovery Engine import for Data Store ID: {data_store_id}")
    time.sleep(2) # Simulate job submission
    return "Import job successfully started (simulated)."

def simulate_data_store_reset(data_store_id):
    """Simulates resetting (purging) all documents from the Data Store."""
    # NOTE: In a real application, this is an asynchronous purge operation
    print(f"Simulating complete purge of Data Store ID: {data_store_id}")
    time.sleep(3) # Simulate the time taken for the API call to start the purge
    return "Purge job successfully initiated (simulated)."


# --- FLASK ROUTES ---

@app.route('/')
def index():
    """Serves the main application page."""
    # Flask looks for index.html inside a 'templates' folder
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles PDF file upload, saves it locally, and simulates GCP processing."""
    if 'textbook_file' not in request.files:
        return jsonify(status='error', message='No file part in the request'), 400

    file = request.files['textbook_file']

    if file.filename == '':
        return jsonify(status='error', message='No selected file'), 400

    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            local_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(local_filepath)

            # 1. Upload to GCS (Simulated)
            gcs_uri = simulate_upload_to_gcs(local_filepath, filename)

            # 2. Start Discovery Engine Import (Simulated)
            import_message = simulate_data_store_import(gcs_uri, PERMANENT_DATA_STORE_ID)

            # Clean up the local file after simulation (optional in real use)
            os.remove(local_filepath)

            return jsonify(
                status='success',
                message=f'File "{filename}" uploaded and indexing started. {import_message}'
            )
        except Exception as e:
            print(f"Server error during upload: {e}")
            return jsonify(status='error', message=f'Server Error during processing: {str(e)}'), 500

    return jsonify(status='error', message='File type not allowed (must be PDF).'), 400

@app.route('/reset', methods=['POST'])
def reset_knowledge_base():
    """Handles the request to purge all documents from the Data Store."""
    try:
        reset_message = simulate_data_store_reset(PERMANENT_DATA_STORE_ID)
        return jsonify(
            status='success',
            message=f'Knowledge base reset requested. {reset_message}'
        )
    except Exception as e:
        print(f"Server error during reset: {e}")
        return jsonify(status='error', message=f'Server Error during reset: {str(e)}'), 500


# --- RUNNING THE SERVER ---
if __name__ == '__main__':
    print(f"Starting Flask server. To access the app, open your browser to http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
