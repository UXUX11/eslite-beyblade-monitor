from pathlib import Path
from datetime import datetime


class Logger:

    def __init__(self):

        Path("logs").mkdir(exist_ok=True)

        today = datetime.now().strftime("%Y%m%d")

        self.filename = f"logs/{today}.log"

    def write(self, text):

        now = datetime.now().strftime("%H:%M:%S")

        message = f"[{now}] {text}"

        print(message)

        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")

    def line(self):

        self.write("-" * 60)