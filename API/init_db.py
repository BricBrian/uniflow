import sqlite3

DATABASE_FILE = "expand_reduce_flow.db"  # Change to your desired database file path

def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Create the Jobs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create the Results table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            job_id TEXT,
            node_data TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (job_id) REFERENCES jobs (job_id)
        )
    ''')

    conn.commit()
    conn.close()