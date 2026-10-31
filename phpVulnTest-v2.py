import argparse
import requests
import os
from time import sleep, perf_counter

# Logo ASCII text PHPOOMTS
logo = '''
  ____  _   _ ____   ___   ___  __  __ _____ _____
 |  _ \| | | |  _ \ / _ \ / _ \|  \/  | ____|_   _|
 | |_) | |_| | |_) | | | | | | | |\/| |  _|   | |
 |  __/|  _  |  __/| |_| | |_| | |  | | |___  | |
 |_|   |_| |_|_|    \___/ \___/|_|  |_|_____| |_|
BY: 49U5.RMD - 10/2026
'''

# Menampilkan logo dan informasi penulis
print(logo)

def send_large_file(url, file_path):
    # Create a large file to upload
    with open(file_path, 'wb') as f:
        for _ in range(args.file_size * 1024 * 1024):  # 1 MB per chunk
            f.write(b'x')

    files = {'file': (os.path.basename(file_path), open(file_path, 'rb'), 'application/octet-stream')}
    response = requests.post(url, files=files)
    
    if os.path.exists(file_path):
        try:
            sleep(2)  # Tunda sebelum menghapus file
            os.remove(file_path)  # Clean up the temporary large file
        except PermissionError as e:
            print(f"Failed to remove file: {e}")

    return response.status_code

def main():
    parser = argparse.ArgumentParser(description='PHP Out-of-Memory Exploit Tester')
    parser.add_argument('--url', type=str, required=True, help='URL to test')
    parser.add_argument('--file-size', type=int, default=10, help='Size of the large file in MB (default: 10 MB)')
    global args
    args = parser.parse_args()

    # Create a temporary large file
    temp_file_path = f'{os.getcwd()}/largefile.tmp'
    
    total_chunks = args.file_size * 1024 * 1024 // (1024 * 1024)
    chunk_size = 1024 * 1024

    print(f"Creating Large File to Upload: 0%")
    with open(temp_file_path, 'wb') as f:
        start_time = perf_counter()
        for i in range(total_chunks):
            f.write(b'x')
            current_chunk_percentage = ((i + 1) / total_chunks) * 100
            print(f"\rCreating Large File to Upload: {current_chunk_percentage:.2f}%", end="")
    
    print("\nSending Large File:", end="")
    start_time = perf_counter()
    response_status = send_large_file(args.url, temp_file_path)
    elapsed_time = perf_counter() - start_time
    print(f"\rSending Large File: Done ({elapsed_time:.2f}s)")

    print("Chunk Upload Number:", end=" ")
    for i in range(1, total_chunks + 1):
        if i % 10 == 0:
            print(i)
        else:
            print(i, end=", ")

    print("\nWaiting respond from Web Server: \\|/-")
    response_symbols = ['\\', '|', '/', '-']
    for _ in range(3):  # Rotate symbols 3 times
        for symbol in response_symbols:
            print(f"\rWaiting respond from Web Server: {symbol}", end="")
            sleep(0.5)
    
    print("\nStatus:", response_status)

    oom_detected = False
    if response_status == 200:
        # Check for Out-of-Memory condition by analyzing the request and response times
        if elapsed_time > 10:  # Adjust threshold as needed
            oom_detected = True

    print("OOM Detection:", "True" if oom_detected else "False")
    if not oom_detected:
        print("PHP2Shell Exploitation not detected")
    else:
        print("PHP2Shell Exploitation Detected, Please Upgrade your PHP based on PHP Security Advisories")

if __name__ == "__main__":
    main()
