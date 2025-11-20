import sqlite3
import os

DB_FILE = "Data.db"


def create_db():
    # Check if the database file already exists
    db_exists = os.path.exists(DB_FILE)
    # Connect database (automatically create file if it doesn't exist)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    if not db_exists:
        print(f"Creating new database: {DB_FILE}")

        """ --- Table 1: activity_log ---
            This table will store the activity logs. """
        cursor.execute(
            """
        CREATE TABLE activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT (DATETIME('now', 'localtime')),
            window_title TEXT NOT NULL,
            process_name TEXT
        )
        """
        )

        """ --- Table 2: rules ---
            This table will store the rules(users can create their own). """
        cursor.execute(
            # Bạn có thể tạo ra thêm xếp loại mới tại đây.
            """
        CREATE TABLE rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL CHECK(category IN ('Học tập', 'Giải trí', 'Khác'))
        )
        """
        )

        # --- Default rules ---
        # keyword, category
        default_rules = [
            ("Visual Studio Code", "Học tập"),
            ("PyCharm", "Học tập"),
            ("Bài giảng", "Học tập"),
            ("Google Docs", "Học tập"),
            ("Tài liệu", "Học tập"),
            ("Stack Overflow", "Học tập"),
            ("Facebook", "Giải trí"),
            ("YouTube", "Giải trí"),
            ("Netflix", "Giải trí"),
            ("Spotify", "Giải trí"),
            ("Steam", "Giải trí"),
        ]

        cursor.executemany(
            "INSERT INTO rules (keyword, category) VALUES (?, ?)", default_rules
        )

        print("Successfully created.")

    else:
        print(f"Database '{DB_FILE}' đã tồn tại.")
    conn.commit()
    conn.close()


# This function is called by agent.py
def add_log(window_title, process_name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO activity_log (window_title, process_name) VALUES (?, ?)",
        (window_title, process_name),
    )

    conn.commit()
    conn.close()


def get_rules():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = (
        sqlite3.Row
    )  # sqlite3.Row return dict, so we can access column by name, instead of index
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rules ORDER BY category")
    rules = cursor.fetchall()
    conn.close()
    return rules


def add_rule(keyword, category):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO rules (keyword, category) VALUES (?, ?)", (keyword, category)
        )
        conn.commit()
        conn.close()
        return True, "Thêm quy tắc thành công!"
    except sqlite3.IntegrityError:  # UNIQUE constraint failed.
        conn.close()
        return False, f"Từ khóa '{keyword}' đã tồn tại."
    except Exception as e:
        conn.close()
        return False, f"Lỗi không xác định: {e}"


def delete_rule(rule_id):
    try:
        if rule_id not in [rule["id"] for rule in get_rules()]:
            return False, "Mã(ID) Quy tắc không tồn tại."
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM rules WHERE id = ?", (rule_id,))
        conn.commit()
        conn.close()
        return True, "Xóa quy tắc thành công!"
    except Exception as e:
        conn.close()
        return False, f"Lỗi khi xóa: {e}"


if __name__ == "__main__":
    pass
