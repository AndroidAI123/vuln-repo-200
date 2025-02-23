import os
import random
import subprocess
import time

# Thư mục chứa các file "nhạy cảm"
VULN_DIR = "vuln_files"

# Danh sách các loại file "nhạy cảm" có thể được tạo
SENSITIVE_FILES = [".key", ".pat", ".rsa", ".pem"]

# Danh sách các file text thông thường
TEXT_FILES = ["data1.txt", "data2.txt", "notes.txt"]

# Số lượng commit cần tạo
NUM_COMMITS = 20

# Đảm bảo thư mục tồn tại
if not os.path.exists(VULN_DIR):
    os.makedirs(VULN_DIR)

def generate_random_files():
    """Tạo file ngẫu nhiên dựa trên xác suất"""
    prob = random.random()  # Xác suất giữa 0 và 1
    files_created = []

    if prob < 0.5:
        # 50% tạo các file chứa thông tin nhạy cảm
        num_files = random.randint(1, 3)  # Tạo từ 1 đến 3 file
        for _ in range(num_files):
            file_name = random.choice(SENSITIVE_FILES)
            file_path = os.path.join(VULN_DIR, f"fake_secret_{random.randint(1000, 9999)}{file_name}")
            with open(file_path, "w") as f:
                f.write(f"Fake sensitive data for {file_name}")
            files_created.append(file_path)
    else:
        # 50% chỉ tạo file .txt bình thường
        num_files = random.randint(1, 3)
        for _ in range(num_files):
            file_name = random.choice(TEXT_FILES)
            file_path = os.path.join(VULN_DIR, f"{random.randint(1000, 9999)}_{file_name}")
            with open(file_path, "w") as f:
                f.write(f"Normal text content for {file_name}")
            files_created.append(file_path)

    return files_created

def git_commit(commit_num):
    """Tạo commit với các file được sinh ra"""
    files = generate_random_files()

    # Add tất cả các file vào Git
    subprocess.run(["git", "add", "."], check=True)

    # Commit với nội dung tùy chỉnh
    commit_message = f"Auto commit #{commit_num}"
    subprocess.run(["git", "commit", "-m", commit_message], check=True)

    print(f"✅ Commit {commit_num}/20 created with files: {files}")

def main():
    for i in range(1, NUM_COMMITS + 1):
        git_commit(i)
        time.sleep(1)  # Chờ 1 giây để tránh commit trùng timestamp

    # Push lên remote (nếu cần)
    push_confirm = input("Bạn có muốn push lên GitHub không? (y/n): ").strip().lower()
    if push_confirm == "y":
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("🚀 Code đã được push lên GitHub!")

if __name__ == "__main__":
    main()
