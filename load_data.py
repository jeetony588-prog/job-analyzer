import sqlite3
import csv

DB_NAME = "jobs.db"
CSV_FILE = "jobs.csv"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            city TEXT,
            min_salary INTEGER,
            max_salary INTEGER,
            skills TEXT
        )
    ''')
    conn.commit()
    conn.close()

def import_csv():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute('''
                INSERT INTO jobs (title, city, min_salary, max_salary, skills)
                VALUES (?, ?, ?, ?, ?)
            ''', (row['title'], row['city'], int(row['min_salary']), int(row['max_salary']), row['skills']))
    conn.commit()
    conn.close()
    print(f"已导入 {CSV_FILE} 中的数据")

if __name__ == "__main__":
    create_table()
    import_csv()
    print("数据库初始化完成")