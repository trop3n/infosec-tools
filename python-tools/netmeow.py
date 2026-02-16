import argparse
import shlex
import socket
import subprocess
import sys
import textwrap
import threading


def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return


output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
