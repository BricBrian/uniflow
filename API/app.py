from flask import Flask, request, jsonify
import threading
import uuid
import sqlite3
from datetime import datetime
# Replace 'your_module' with the actual name of the module where ExpandReduceFlow and Node are defined
from uniflow.flow.transform.expand_reduce_flow import ExpandReduceFlow  
from uniflow.node import Node

app = Flask(__name__)

# Path to the database file
DATABASE_FILE = "expand_reduce_flow.db"

# Function to asynchronously execute ExpandReduceFlow
def async_expand_reduce_flow(job_id, input_data):
    try:
        root_node = Node(name="root", value_dict=input_data)
        flow = ExpandReduceFlow(prompt_template=None, model_config={})
        result_nodes = flow.run([root_node])
        # Store the results in the database
        store_results(job_id, result_nodes)
        update_job_status(job_id, "completed")
    except Exception as e:
        update_job_status(job_id, "error")

@app.route('/start-expand-reduce', methods=['POST'])
def start_expand_reduce():
    job_id = str(uuid.uuid4())
    input_data = request.json.get('input_data')
    create_job(job_id)
    threading.Thread(target=async_expand_reduce_flow, args=(job_id, input_data)).start()
    return jsonify({"job_id": job_id, "message": "Job started successfully"}), 202

@app.route('/check-status/<job_id>', methods=['GET'])
def check_status(job_id):
    status = get_job_status(job_id)
    return jsonify({"job_id": job_id, "status": status})

@app.route('/results/<job_id>', methods=['GET'])
def get_results(job_id):
    results = retrieve_results(job_id)
    return jsonify({"job_id": job_id, "results": results})

def create_job(job_id):
    """Create a new job record in the database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jobs (job_id, status) VALUES (?, 'pending')", (job_id,))
    conn.commit()
    conn.close()

def update_job_status(job_id, status):
    """Update the status of a job."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE jobs SET status = ? WHERE job_id = ?", (status, job_id))
    conn.commit()
    conn.close()

def store_results(job_id, nodes):
    """Store the results of a job."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    for node in nodes:
        # Assuming node data is serializable to JSON
        node_data = json.dumps(node.flatten())  # Convert node data to JSON
        cursor.execute("INSERT INTO results (job_id, node_data) VALUES (?, ?)", (job_id, node_data))
    conn.commit()
    conn.close()

def get_job_status(job_id):
    """Retrieve the status of a job."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM jobs WHERE job_id = ?", (job_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def retrieve_results(job_id):
    """Retrieve the results of a job."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT node_data FROM results WHERE job_id = ?", (job_id,))
    results = [json.loads(row[0]) for row in cursor.fetchall()]  # Convert JSON back to Python object
    conn.close()
    return results