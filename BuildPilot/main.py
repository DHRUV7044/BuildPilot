import subprocess

command = [
    ['git', '--version'],
    ['git', 'pull'],
    ['dotnet', '--version'],
    ['dotnet', 'build'],
]

def run_command(command):
    result = subprocess.run(
        command,
        text=True,
        capture_output=True
    )
    return result

for cmd in command:
    result = run_command(cmd)
    print(f"Command: {' '.join(cmd)}")
    print(result.stdout.strip())
    print("Return Code:", result.returncode)
    print("-" * 40)


