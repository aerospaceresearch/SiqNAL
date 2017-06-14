import sys
import os
from subprocess import call

if __name__ == "__main__":

    files = os.listdir(".")

    for file in files:
        if file.endswith('.py'):
            print("*" * 10 + "Indenting " + file + "*" * 10)
            call(["autopep8", file, "--in-place"])
            print("=" * 25)
