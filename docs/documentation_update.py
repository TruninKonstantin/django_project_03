# Should be run with Python 2.7
# File paths should be changed

import subprocess
import pathlib

root_folder_path = r"C:\KosMain\Code\python\projects\Django\django_project_03\mysite\output_pressure"

full_file_names = list(pathlib.Path(root_folder_path).glob('*.py'))

full_file_names_str = []
for file_name in full_file_names:
    if "__init__" not in str(file_name):
        full_file_names_str.append(str(file_name))

full_file_names_str.append(
    r"C:\KosMain\Code\python\projects\Django\django_project_03\mysite\output_pressure\static\output_pressure\app.js")
full_file_names_str.append(
    r"C:\KosMain\Code\python\projects\Django\django_project_03\mysite\output_pressure\constants\constants.py")
for file_name in full_file_names_str:
    print (file_name)

str_command = "pycco "
destination_folder = "-d " +r"C:\KosMain\Code\python\projects\Django\django_project_03\docs" + " "
create_index = "-i "

start_str = str_command + destination_folder + create_index
for file_name in full_file_names_str:
    start_str = start_str + file_name + " "

print (start_str)
subprocess.call(start_str, shell=True)
