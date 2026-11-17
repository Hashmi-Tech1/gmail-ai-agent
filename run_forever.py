import os
import subprocess
import sys
import time

INTERVAL = 2 * 60 * 60  # every 2 hours
HERE = os.path.dirname(os.path.abspath(__file__))

# UTF-8 so emoji or non-English subjects do not crash the log
ENV = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")

while True:
    with open(os.path.join(HERE, "log.txt"), "a", encoding="utf-8") as f:
        f.write(f"===== {time.ctime()} =====\n")
        f.flush()
        for script in ("classify_emails.py", "reply_drafts.py"):
            subprocess.run([sys.executable, script], cwd=HERE, env=ENV,
                           stdout=f, stderr=subprocess.STDOUT)
    print("Agent ran:", time.ctime(), "- next run in 2 hours")
    time.sleep(INTERVAL)
