import git
import sys
import os

while not os.path.isdir('.//RpiAI'):
    os.chdir("..//")

print("Start pulling")
sys.stdout.flush()

try:
    g = git.cmd.Git(".//RpiAI")
    g.pull()
except Exception as e:
    print(e)

print("Done pulling")
sys.stdout.flush()