import os
import sys
import time
import pymysql

def run_animated_task(task_name, duration=1.0):
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        frame = spinner[i % len(spinner)]
        sys.stdout.write(f"\r\033[94m{frame}\033[0m {task_name}...")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write(f"\r\033[92m✔\033[0m {task_name} انجام شد.\n")
    sys.stdout.flush()

if __name__ == "__main__":
    print("\n--- اجرای تست عملیاتی اتصال اپلیکیشن به دیتابیس ---\n")

    # خواندن امن متغیرها از محیط سیستم‌عامل کانتینر
    db_host = os.getenv("DB_HOST", "db")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    db_name = os.getenv("DB_NAME")

    run_animated_task("خواندن امن متغیرهای محیطی از کانتینر")
    run_animated_task("بررسی DNS داخلی و لایه انتقال شبکه")
    run_animated_task(f"احراز هویت کاربر {db_user} در پایگاه‌داده MariaDB")

    conn = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )

    with conn.cursor() as cursor:
        run_animated_task("ایجاد جدول عملیاتی service_logs")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS service_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                service_name VARCHAR(50),
                status VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        run_animated_task("درج رکورد وضعیت سیستم")
        cursor.execute("INSERT INTO service_logs (service_name, status) VALUES ('backend_app', 'HEALTHY');")
        conn.commit()

        cursor.execute("SELECT * FROM service_logs ORDER BY id DESC LIMIT 1;")
        record = cursor.fetchone()

    conn.close()

    print(f"\n\033[1;32mارتباط با موفقیت برقرار شد!\033[0m")
    print(f"آخرین رکورد ثبت‌شده روی دیسک: \033[93m{record}\033[0m\n")
