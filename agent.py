import pygetwindow
import time
import database
import sys

INTERVAL_TIME = 5


def start_agent():
    print("Đang bắt đầu...")
    print(f"Thời gian ghi log mỗi: {INTERVAL_TIME} giây")
    print("Phím tắt Ctrl+C để dừng.")

    last_title = ""  # Last title recorded

    try:
        while True:
            active_window = pygetwindow.getActiveWindow()
            if active_window:
                title = active_window.title

                if title and title != last_title:

                    database.add_log(title, None)

                    print(f"Active window: {title}")
                    last_title = title

            time.sleep(INTERVAL_TIME)

    except KeyboardInterrupt:
        print("\nInsight Agent đã dừng. Hẹn gặp lại!")
        sys.exit(0)
    except Exception as error:
        print(f"\nError: {error}")
        print("Agent stopped.")
        sys.exit(1)


if __name__ == "__main__":
    database.create_db()
    start_agent()
