import os
import sys

try:
    from dotenv import load_dotenv
except ImportError:
    print("[FAIL] Missing python-dotenv")
    print("Run: pip install python-dotenv")
    sys.exit(1)


def check_hardcoded_secrets(file_path):
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
        for line in lines:
            clean_line = line.strip().replace(" ", "")
            for key in ["API_KEY", "PASSWORD", "ACCESS_TOKEN"]:
                if f"{key}=" in clean_line:
                    return False
        return True
    except Exception:
        return False


def show_status(label, value, ok_message, fail_message):
    if value:
        print(f"{label}: {ok_message}")
    else:
        print(f"{label}: {fail_message}")


def main():
    load_dotenv()
    mode = os.getenv("MATRIX_MODE", "development").strip()
    database_url = os.getenv("DATABASE_URL", "").strip()
    api_key = os.getenv("API_KEY", "").strip()
    log_level = os.getenv("LOG_LEVEL", "DEBUG").strip()
    zion_endpoint = os.getenv("ZION_ENDPOINT", "").strip()

    print("ORACLE STATUS: Reading the Matrix...")
    if mode == "production":
        missing: list = []
        if not api_key:
            missing.append("API_KEY")
        if not database_url:
            missing.append("DATABASE_URL")
        if not zion_endpoint:
            missing.append("ZION_ENDPOINT")

        if missing:
            print(f"{missing} is Missing")
            sys.exit(1)
    elif mode == "development":
        print("\nConfiguration loaded:")
        print(f"Mode: {mode}")
        show_status(
            "Database",
            database_url,
            "Connected to local instance",
            "Missing DATABASE_URL",
        )
        show_status("API Access", api_key, "Authenticated", "Missing API_KEY")
        print(f"Log Level: {log_level}")
        show_status(
            "Zion Network", zion_endpoint, "Online", "Missing ZION_ENDPOINT"
        )
    else:
        print("Invalid Mode")

    print("\nEnvironment security check:")

    env_in_gitignore = False
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r") as f:
            if ".env" in f.read():
                env_in_gitignore = True

    if not check_hardcoded_secrets(__file__):
        print("[FAIL] Hardcoded secret detected in source code!")
    else:
        print("[OK] No hardcoded secrets detected")

    if env_in_gitignore:
        print("[OK] .env file properly configured")
    else:
        print("[FAIL] .env file isn't properly configured")

    if mode in ("production", "development"):
        print("[OK] Production overrides available")

    print("\nThe Oracle sees all configurations.")


main()
