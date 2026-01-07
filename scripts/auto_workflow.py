import argparse
import datetime
import os
import subprocess
import sys
import time

from dotenv import load_dotenv

try:
    import psycopg2
except ImportError:
    psycopg2 = None

try:
    from watchdog.observers import Observer
    from watchdog.events import PatternMatchingEventHandler
except ImportError:
    Observer = None
    PatternMatchingEventHandler = None


load_dotenv()


def run(cmd, check=True):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed ({cmd}): {result.stderr.strip()}")
    return result.stdout.strip()


def git_status():
    return run("git status --porcelain", check=False)


def record_change(commit_hash, message, reason, branch):
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL not set; skipping DB audit.")
        return
    if not psycopg2:
        print("psycopg2 not installed; cannot write audit row.")
        return

    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO change_iterations (commit_hash, message, reason, branch, actor)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (commit_hash) DO NOTHING;
            """,
            (commit_hash, message, reason, branch, os.getenv("USER", "auto")),
        )
        conn.commit()
        cur.close()
        conn.close()
        print(f"Logged {commit_hash} to Postgres audit.")
    except Exception as exc:
        print(f"Failed to log commit to DB: {exc}")


def commit_and_push(reason):
    status = git_status()
    if not status:
        print("No changes to commit.")
        return None

    run("git add -A")
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    prefix = os.getenv("AUTO_COMMIT_PREFIX", "auto")
    branch = os.getenv("AUTO_COMMIT_BRANCH", "main")
    message = f"{prefix}: {reason} @ {ts}"

    try:
        run(f"git commit -m \"{message}\"")
    except RuntimeError as exc:
        print(exc)
        return None

    commit_hash = run("git rev-parse HEAD")
    auto_push = os.getenv("AUTO_PUSH", "true").lower() == "true"

    if auto_push:
        try:
            run(f"git push origin {branch}")
            print("Pushed to remote.")
        except RuntimeError as exc:
            print(f"Push failed: {exc}")
    else:
        print("AUTO_PUSH disabled; commit created locally.")

    record_change(commit_hash, message, reason, branch)
    return commit_hash


def rollback(commit_hash):
    # creates a revert commit rather than destructive reset
    try:
        run(f"git revert --no-edit {commit_hash}")
        new_hash = run("git rev-parse HEAD")
        record_change(new_hash, f"revert: {commit_hash}", "rollback", os.getenv("AUTO_COMMIT_BRANCH", "main"))
        return new_hash
    except RuntimeError as exc:
        print(f"Rollback failed: {exc}")
        return None


def watch(path="."):
    if not Observer or not PatternMatchingEventHandler:
        print("watchdog is not installed. Install deps: pip install -r requirements.txt")
        sys.exit(1)

    ignore_patterns = [".git/*", ".venv/*", "db-data/*", "*.swp", "*.tmp", "*.log"]
    handler = PatternMatchingEventHandler(
        patterns=["*"],
        ignore_patterns=ignore_patterns,
        ignore_directories=False,
        case_sensitive=False,
    )

    last_commit_time = 0

    def on_change(event):
        nonlocal last_commit_time
        now = time.time()
        # debounce to avoid rapid-fire commits
        if now - last_commit_time < 2:
            return
        last_commit_time = now
        reason = f"fs-change:{event.event_type}:{event.src_path}"
        print(f"Detected change: {reason}")
        commit_and_push(reason)

    handler.on_created = on_change
    handler.on_modified = on_change
    handler.on_deleted = on_change
    handler.on_moved = on_change

    observer = Observer()
    observer.schedule(handler, path, recursive=True)
    observer.start()
    print("Watching for file changes. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main():
    parser = argparse.ArgumentParser(description="Auto commit/push/rollback workflow for RYZE.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("once", help="Run a single add/commit/push cycle.")
    subparsers.add_parser("watch", help="Watch filesystem and auto commit on changes.")

    rollback_parser = subparsers.add_parser("rollback", help="Revert a commit hash with a revert commit.")
    rollback_parser.add_argument("hash", help="Commit hash to revert.")

    args = parser.parse_args()

    if args.command == "once":
        commit_and_push("manual-trigger")
    elif args.command == "watch":
        watch()
    elif args.command == "rollback":
        rollback(args.hash)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
