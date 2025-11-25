from flask import Flask,render_template
import os
import psycopg2
from psycopg2.extras import RealDictCursor

application = Flask(__name__)

def get_db_connection():
    """
    Create and return a new connection to the PostgreSQL database
    using environment variables configured in Elastic Beanstalk.
    """
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv("DB_PORT", 5432),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        cursor_factory=RealDictCursor
    )
    return conn

def init_db():
    """
    Ensures the 'visits' table exists.
    This runs once when the app starts.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS visits (
                    id SERIAL PRIMARY KEY,
                    path TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        #For Production, you'd use proper logging. This is fine for local testing.
        print("Error during init_db:", e)

#Initialize DB once at startup
init_db()

@application.route('/')
def home():
    #return "Hello from Flask on AWS Elastic Beanstalk!"
    return render_template('index.html')

@application.route('/secret')
def secret():        
    message = os.getenv('SECRET_GREETING',"No secret set!")
    return render_template("secret.html", message = message)

@application.route('/health')
def health():
    return {"status": "OK" },200

@application.route('/stats')
def stats():
    """
    Insert a new visit and show the total count.
    Every time someone hits /stats, we insert a new row into 'visits' and then count how many total visits have ever happened.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    #Record this visit
    cur.execute(
        "INSERT INTO visits(path) VALUES(%s) RETURNING id;", 
        ("/stats",)
    )
    conn.commit()
    #Count total visits
    cur.execute("SELECT COUNT(*) AS total_visits FROM visits;")
    row = cur.fetchone()

    cur.close()
    conn.close()

    total_visits = row['total_visits']
    return render_template("stats.html",total_visits=total_visits)

#Running locally only
if __name__ == "__main__":
    #EB uses a production server, so this is for local testing only
    application.run(host="0.0.0.0", port=8080, debug=True)