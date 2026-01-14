import subprocess
import socket
import time
import sys


def run_test():
    server_port = 12000  # You can change this port if needed
    server_number = 700  # You can change this number if needed

    input_string = "hello, this is inha"  # test your own string
    input_number = 53535  # test your own number

    expected_string = input_string.upper()
    expected_number = str(input_number + server_number)

    server_cmd = ["python3", "server.py", "--port", str(server_port), "--number", str(server_number)]
    server_proc = subprocess.Popen(server_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1)

    try:
        client_cmd = ["python3", "client.py", "--host", "127.0.0.1", "--port", str(server_port)]
        input_data = f"{input_string}\n{input_number}\n"  # string + number
        result = subprocess.run(client_cmd, input=input_data, text=True, capture_output=True, timeout=5)

        # print("[CLIENT OUTPUT]")
        # print(result.stdout.strip())

        if expected_string in result.stdout and expected_number in result.stdout:
            print("\n✅ Test passed.")
        else:
            print("\n❌ Test failed. Check your client/server logic.")

    except Exception as e:
        print("❌ Test failed with exception:", e)

    server_proc.terminate()
    try:
        server_proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        server_proc.kill()


if __name__ == "__main__":
    run_test()
