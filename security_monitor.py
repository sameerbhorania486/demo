import os
import socket
import hashlib
import datetime
import psutil

LOG_FILE = "security_monitor.log"


def log_event(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print("=" * 60)
    print("        SECURITY MONITOR - DEFENSIVE TOOL")
    print("=" * 60)


def system_info():
    print("\n[ SYSTEM ]")
    print(f"CPU Usage: {psutil.cpu_percent()}%")
    print(f"RAM Usage: {psutil.virtual_memory().percent}%")


def scan_ports():
    print("\n[ OPEN PORTS ]")
    found = False

    for port in [21, 22, 23, 25, 53, 80, 110, 443, 3306, 8080]:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)

        if s.connect_ex(("127.0.0.1", port)) == 0:
            print(f"Port {port} OPEN")
            found = True

        s.close()

    if not found:
        print("No common ports open.")


def file_hash(path):
    try:
        with open(path, "rb") as f:
            digest = hashlib.sha256(f.read()).hexdigest()

        print("\n[ FILE HASH ]")
        print(digest)

        log_event(f"Hash checked: {path}")

    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("Error:", e)


def view_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            print("\n[ LOGS ]")
            print(f.read())
    else:
        print("No logs found.")


def menu():
    while True:
        clear()
        banner()

        print("\n1. System Information")
        print("2. Scan Local Ports")
        print("3. Generate File SHA256")
        print("4. View Logs")
        print("5. Exit")

        choice = input("\nChoice: ")

        if choice == "1":
            system_info()

        elif choice == "2":
            scan_ports()

        elif choice == "3":
            path = input("Enter file path: ")
            file_hash(path)

        elif choice == "4":
            view_logs()

        elif choice == "5":
            print("Exiting Security Monitor...")
            break

        else:
            print("Invalid choice!")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    menu()