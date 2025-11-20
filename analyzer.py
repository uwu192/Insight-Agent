import pandas as pd
import sqlite3
import database
from datetime import datetime, timedelta


def categorize_title(title, rules):
    title = str(title).lower()

    for index, row in rules.iterrows():
        keyword_lower = str(row["keyword"]).lower()

        if keyword_lower in title:
            return row["category"]

    return "Khác"


# Get data from database by time range
def get_analysis(start_date, end_date):
    conn = sqlite3.connect(database.DB_FILE)
    query_log = f"""
    SELECT timestamp, window_title
    FROM activity_log
    WHERE timestamp >= '{start_date}' AND timestamp < '{end_date}'
    """

    query_rules = "SELECT keyword, category FROM rules"

    try:
        # ( Command, Database )
        logs = pd.read_sql_query(query_log, conn)
        rules = pd.read_sql_query(query_rules, conn)
    finally:
        conn.close()

    if logs.empty:
        print("No data to analyze in time range.")
        return pd.DataFrame(columns=["timestamp", "window_title", "category"])

    print(f"Analyzing {len(logs)} logs...")
    # Create new column "category", apply function categorize_title to each row with rules as argument
    logs["category"] = logs["window_title"].apply(categorize_title, args=(rules,))

    print("Successfully.")
    return logs


# --- Main block để chạy file này trực tiếp ---
if __name__ == "__main__":
    print("TEST")
    date_today = datetime.now()
    date_7_days_ago = date_today - timedelta(days=7)

    # Format SQL(YYYY-MM-DD HH:MM:SS)
    start_str = date_7_days_ago.strftime("%Y-%m-%d 00:00:00")
    end_str = date_today.strftime("%Y-%m-%d 23:59:59")

    print(f"This data from {start_str} to {end_str}:")

    # Chạy hàm phân tích
    analysis = get_analysis(start_str, end_str)

    if not analysis.empty:
        print(analysis)

        print("\n--- Analysis count ---")
        print(analysis["category"].value_counts())
    else:
        print("No data to analyze.")
