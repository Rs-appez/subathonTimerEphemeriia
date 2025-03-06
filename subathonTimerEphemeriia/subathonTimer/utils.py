from django.conf import settings

import re


def write_log(msg):
    path = "/logs/log.txt" if not settings.DEBUG else "log.txt"
    with open(path, "a") as f:
        f.write("\n")
        f.write(msg)
        f.write("\n")
        f.write("-" * 100)


def get_logs():
    path = "/logs/log.txt" if not settings.DEBUG else "log.txt"
    with open(path, "r") as f:
        lines = f.readlines()
    return lines[::-1]


def get_tippers():
    logs = get_logs()
    tippers = []

    for log in logs:
        start_sub = re.search(r"Subathon started", log)
        if start_sub:
            break
        match = re.search(r"New donation: (\w+) - (\d+\.\d+)", log)
        if match:
            for tipper in tippers:
                if tipper["name"] == match.group(1):
                    tipper["total"] = float(tipper["total"]) + float(match.group(2))
                    break

            else:
                tippers.append({"name": match.group(1), "total": float(match.group(2))})

    tippers = sorted(tippers, key=lambda x: x["total"], reverse=True)
    return tippers
