#!/usr/bin/env python3
"""Run one sitting by hand: opens each prompt's tabs in Dia, copies the prompt, and records your labels.

Usage: python3 run.py check               check that Dia can read the local pages
       python3 run.py <sitting> [log]     sitting is 1, 2, noise-2 or noise-3;
                                          log defaults to private/session1.csv
Prompts that already have an answer type are skipped, so you can stop (Ctrl+C) and rerun.
Nothing here touches Dia's chat: you paste and send every prompt yourself.
"""
import csv
import os
import shutil
import socket
import subprocess
import sys
import time

PORT = 8765
BASE = f"http://localhost:{PORT}/"


def ask(question, allowed=None):
    while True:
        answer = input(question).strip().lower()
        if allowed is None or answer in allowed:
            return answer
        print(f"  Type one of: {' '.join(allowed)}")


def serve():
    """Start the page server unless something already listens on the port."""
    with socket.socket() as s:
        if s.connect_ex(("localhost", PORT)) == 0:
            return None
    server = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "--directory", "pages"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(100):  # wait up to ~5 s so Dia never opens a page before the server listens
        with socket.socket() as s:
            if s.connect_ex(("localhost", PORT)) == 0:
                break
        time.sleep(0.05)
    return server


def open_in_dia(pages):
    for page in reversed(pages):  # the current tab opens last, so it ends up active
        subprocess.run(["open", "-a", "Dia", BASE + page], check=True)


def copy(text):
    subprocess.run("pbcopy", input=text.encode(), check=True)


def check():
    open_in_dia(["check.html"])
    copy("What's the check code on this page?")
    input("Opened check.html in Dia and copied a question. Ask it in a new chat, then press Enter here... ")
    if ask("Did Dia answer PURPLE-42? y/n: ", ["y", "n"]) == "y":
        print("Local pages work. Next: python3 run.py 1")
    else:
        print("Dia can't read localhost pages. The pages/ folder needs a free static host, e.g. GitHub Pages.")


def sitting(name, log):
    if not os.path.exists(log):
        os.makedirs(os.path.dirname(log) or ".", exist_ok=True)
        shutil.copy("sessions/template.csv", log)
    with open(log, newline="") as f:
        rows = list(csv.DictReader(f))
    mine = [r for r in rows if r["sitting"] == name]
    if not mine:
        sys.exit(f"No sitting called {name!r}. Use 1, 2, noise-2 or noise-3.")
    todo = [r for r in mine if not r["answer_type"].strip()]
    if not todo:
        sys.exit(f"Sitting {name} is already done in {log}.")
    print("Use a clean Dia profile with no other tabs open, and start the screen recording.")
    build = ask("Dia version (Dia menu > About Dia): ")
    for r in todo:
        print(f"\n--- Sitting {name}, prompt {r['order']} of {len(mine)} ({r['pair']} {r['version']})")
        pages = r["tabs"].replace(" (current)", "").split(" + ")
        if pages == ["new empty tab"]:
            print("Open a new empty tab (Cmd+T).")
        else:
            open_in_dia(pages)
            print(f"Opened: {' + '.join(pages)}. The first one is the active tab.")
        copy(r["prompt"])
        print(f"Copied: {r['prompt']}")
        input("New chat in the Chat sidebar, paste, send. When the answer has finished, press Enter here... ")
        r["build"] = build
        r["answer_type"] = ask("Answer type? 1 direct, 2 direct + offer, 3 thinking/tools, 4 Report, 5 asked a question: ",
                               list("12345"))
        r["thinking"] = ask("Visible thinking steps? y/n: ", ["y", "n"])
        print(f"Correct answer: {r['gold_answer']}")
        r["correct"] = ask("Was Dia right? y/n: ", ["y", "n"])
        r["notes"] = input("Notes (optional, no long quotes): ").strip()
        with open(log, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print("Saved. Close the tabs (Cmd+W) before the next prompt.")
    print(f"\nSitting {name} done. Fill first_words_s from the recording in {log}, then: python3 tally.py {log}")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    args = sys.argv[1:]
    if not args or len(args) > 2:
        sys.exit(__doc__)
    server = serve()
    try:
        if args[0] == "check":
            check()
        else:
            sitting(args[0], args[1] if len(args) == 2 else "private/session1.csv")
    except KeyboardInterrupt:
        print("\nStopped. Rerun the same command to continue.")
    finally:
        if server:
            server.terminate()
