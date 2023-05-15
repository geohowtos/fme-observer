from os import path
import re


def is_fme_log_file(file_path):
    # Check if file is a valid FME log file
    return file_path.endswith('.log') and path.isfile(path.splitext(file_path)[0] + '.fmw')

def get_file_contents(log_file_path):
    # Return log file contents
    with open(log_file_path, 'r', encoding='utf-8') as f:
        contents = f.read()
    return contents

def get_translation_result(log_file_contents):
    # Read log file contents to see if the last translation was successful or failed
    if 'Translation was SUCCESSFUL' in log_file_contents:
        return 'Translation was successful'
    if 'Translation FAILED' in log_file_contents:
        return 'Translation failed'
    return None

def get_translation_duration(log_file_contents):
    # Extract the duration string using regular expression
    string = r'FME Session Duration: ((\d+) hours)?\s?((\d+) minutes)?\s?((\d+(\.\d+)?) seconds)'
    pattern = re.compile(string, re.MULTILINE)
    match = pattern.search(log_file_contents)

    # If the duration string can be found, extract duration values
    if match:
        hours = int(match.group(2) or 0)
        minutes = int(match.group(4) or 0)
        seconds = float(match.group(6))

        # Return the duration in seconds
        return hours * 3600 + minutes * 60 + seconds

    return 0
