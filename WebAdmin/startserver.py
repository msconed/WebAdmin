


import os
import time
import webbrowser
from django.core.management import execute_from_command_line



def run_server():
    execute_from_command_line(["manage.py", "runserver", "--noreload"])

if __name__ == "__main__":
    run_server() 







