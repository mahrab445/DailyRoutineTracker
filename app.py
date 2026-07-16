from flask import Flask, render_template, request, jsonify
import mysql.connector
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)

db = mysql.connector.connect(
    host="thomas.proxy.rlwy.net",
    port=17894,
    user="root",
    password="SaGNihjdshpLSEhVxhSoSsMueJrvYpVu",
    database="railway"
)

cursor = db.cursor()

cursor.execute("SELECT DATABASE();")
print(cursor.fetchone())

cursor.execute("SHOW TABLES;")
print(cursor.fetchall())

cursor = db.cursor(dictionary=True)


@app.route("/")
def home():

    # Bangladesh Time
    today = datetime.now(ZoneInfo("Asia/Dhaka")).date().isoformat()

    selected_date = request.args.get("date")

    if not selected_date:
        selected_date = today

    cursor.execute("""
        SELECT *
        FROM tasks
        ORDER BY id
    """)
    tasks = cursor.fetchall()

    routine = {}

    cursor.execute("""
        SELECT task_id, status
        FROM routine_status
        WHERE routine_date = %s
    """, (selected_date,))

    rows = cursor.fetchall()

    for row in rows:
        routine[row["task_id"]] = row["status"]

    return render_template(
        "index.html",
        tasks=tasks,
        routine=routine,
        today=selected_date,
        current_date=today
    )
@app.route("/save", methods=["POST"])
def save():

    try:
        data = request.json

        task_id = data["task_id"]
        status = data["status"]
        routine_date = data["date"]

        cursor.execute("""
            SELECT *
            FROM routine_status
            WHERE routine_date=%s
            AND task_id=%s
        """, (routine_date, task_id))

        exist = cursor.fetchone()

        if status:

            if exist:
                cursor.execute("""
                    UPDATE routine_status
                    SET status=1
                    WHERE routine_date=%s
                    AND task_id=%s
                """, (routine_date, task_id))
            else:
                cursor.execute("""
                    INSERT INTO routine_status
                    (routine_date, task_id, status)
                    VALUES(%s,%s,1)
                """, (routine_date, task_id))

        else:

            if exist:
                cursor.execute("""
                    DELETE FROM routine_status
                    WHERE routine_date=%s
                    AND task_id=%s
                """, (routine_date, task_id))

        db.commit()

        return jsonify({"message": "Saved Successfully"})

    except Exception as e:
        print("SAVE ERROR:", e)
        return jsonify({"message": str(e)}), 500
    


    
@app.route("/history/<selected_date>")
def history(selected_date):

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    cursor.execute("""
        SELECT task_id,status
        FROM routine_status
        WHERE routine_date=%s
    """,(selected_date,))

    rows = cursor.fetchall()

    routine = {}

    for row in rows:
        routine[row["task_id"]] = row["status"]

    return jsonify({
        "tasks":tasks,
        "routine":routine
    })


@app.route("/progress/<selected_date>")
def progress(selected_date):

    cursor.execute("""
        SELECT COUNT(*) total
        FROM tasks
    """)

    total = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) completed
        FROM routine_status
        WHERE routine_date=%s
        AND status=1
    """,(selected_date,))

    completed = cursor.fetchone()["completed"]

    percent = 0

    if total != 0:
        percent = round((completed/total)*100)

    return jsonify({
        "completed":completed,
        "total":total,
        "percent":percent
    })

@app.route("/summary")
def summary():

    cursor.execute("""
        SELECT
            rs.routine_date,
            COUNT(rs.task_id) AS completed_tasks,
            (SELECT COUNT(*) FROM tasks) AS total_tasks,
            ROUND(
           (COUNT(rs.task_id) * 100.0) /
           (SELECT COUNT(*) FROM tasks)
           ) AS percentage
        FROM routine_status rs
        GROUP BY rs.routine_date
        ORDER BY rs.routine_date DESC
    """)

    summary = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(DISTINCT routine_date) AS total_days
        FROM routine_status
    """)
    total_days = cursor.fetchone()["total_days"]

    cursor.execute("""
        SELECT COUNT(*) AS total_completed
        FROM routine_status
    """)
    total_completed = cursor.fetchone()["total_completed"]

    cursor.execute("""
        SELECT COUNT(*) AS total_tasks
        FROM tasks
    """)
    total_tasks = cursor.fetchone()["total_tasks"]

    average = 0

    if total_tasks > 0:
        average = round(((total_completed / total_tasks) * 100)/total_days)

    return render_template(
        "summary.html",
        summary=summary,
        total_days=total_days,
        total_completed=total_completed,
        total_tasks=total_tasks,
        average=average
    )

if __name__ == "__main__":
    app.run(debug=True)
