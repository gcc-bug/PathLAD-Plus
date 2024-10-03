import subprocess
import os

def run_solver(args):
    command = ['./main'] + args  # Construct the full command
    result = subprocess.run(command, capture_output=True, text=True, cwd=os.getcwd())  # Ensure it runs in the current working directory
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result.stdout

if __name__ == "__main__":
    args = ['-p', 'pattern.txt', '-t', 'target.txt', '-f', '-s', '3600']
    output = run_solver(args)
    print(output)
