import time
import os
import datetime
from rich.console import Console
console = Console()
count = 0
for i in range(1):
    count = count + 1
    console.log(str(count) + ". This prints 1 times every 5secs.")
    time.sleep(5)

path = "data/output.txt"
os.makedirs(os.path.dirname(path), exist_ok=True)
f = open(path, "w")
f.write("Das hat geklappt, hurra!")
f.close()
