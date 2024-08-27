from django.conf import settings

def write_log(msg):
    path = "/logs/log.txt" if not  settings.DEBUG else "log.txt" 
    with open(path, "a") as f:
        f.write("\n")
        f.write(msg)
        f.write("\n")
        f.write("-" * 100)