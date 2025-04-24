import sqlite3

# 连接到数据库（如果没有会自动创建）
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# 创建 users 表（如果不存在）
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    email TEXT NOT NULL
)
''')

# 插入用户数据
users = [
    ("admin", "123456", "uceez14@ucl.ac.uk"),
    ("Kitty", "234567", "uceez14@ucl.ac.uk")
]

# 避免重复插入（忽略已存在的主键）
cursor.executemany("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", users)

# 提交更改并关闭连接
conn.commit()
conn.close()

print("Database Established：users.db")
