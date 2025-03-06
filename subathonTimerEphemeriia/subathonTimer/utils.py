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


def get_donators():
    logs = get_logs()
    donators = []

    for log in logs:
        start_sub = re.search(r"Subathon started", log)
        if start_sub:
            break
        match = re.search(r"New donation: (\w+) - (\d+\.\d+)", log)
        if match:
            for donator in donators:
                if donator["name"] == match.group(1):
                    donator["total"] = float(donator["total"]) + float(match.group(2))
                    break

            else:
                donators.append(
                    {"name": match.group(1), "total": float(match.group(2))}
                )

    donators = sorted(donators, key=lambda x: x["total"], reverse=True)
    return donators


def get_gifters():
    logs = get_logs()
    gifters = []

    for log in logs:
        start_sub = re.search(r"Subathon started", log)
        if start_sub:
            break
        match = re.search(r"New sub: \w+ - \d+ - offered by (\w+)", log)
        if match:
            for gifter in gifters:
                if gifter["name"] == match.group(1):
                    gifter["total"] = gifter["total"] + 1
                    break

            else:
                gifters.append({"name": match.group(1), "total": 1})

    gifters = sorted(gifters, key=lambda x: x["total"], reverse=True)
    return gifters
