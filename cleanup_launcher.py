import os
import sys
import time
import psutil

def log(msg, log_path):
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {msg}\n")
    except Exception as e:
        print("[ERROR] Logging failed:", e)

def log_separator(log_path, symbol="=", length=60, end=False):
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(symbol * length + ("\n" if not end else "\n\n"))
    except Exception as e:
        print("[ERROR] Logging separator failed:", e)

def log_start(log_path):
    log_separator(log_path)
    log(">>> START OF SESSION <<<", log_path)

def log_end(log_path):
    log("<<< END OF SESSION >>>", log_path)
    log_separator(log_path, end=True)

def wait_for_delete(process_name, log_path):
    try:
        log(f"[WAIT] Waiting for {process_name} to close...", log_path)
        target = process_name.lower()
        while any(p.name().lower() == target for p in psutil.process_iter()):
            time.sleep(1)
        log(f"[DONE] {process_name} has exited.", log_path)
    except Exception as e:
        log(f"[ERROR] Failed to check process: {e}", log_path)
        sys.exit(1)


def delete_file(path, log_path, retries=5, delay=1):
    for _ in range(retries):
        if not os.path.exists(path):
            return
        try:
            os.remove(path)
            log(f"[OK] Deleted: {path}", log_path)
            return
        except Exception:
            time.sleep(delay)
    if os.path.exists(path):
        log(f"[FAIL] Could not delete: {path}", log_path)

def main():
    files = sys.argv[1:]
    if not files:
        return

    log_path = os.path.join(os.path.dirname(sys.executable), "cleanup.log")

    log_start(log_path)
    wait_for_delete("WorldOfTanks.exe", log_path)

    for file_path in files:
        delete_file(file_path, log_path)

    log_end(log_path)

    sys.exit(0)

if __name__ == "__main__":
    main()