import subprocess

command = [
    ['git', '--version'],
    ['git' , 'pull']
]

result = subprocess.run(
    command[1],
    text=True,
    capture_output=True
)

print(result.stdout.strip())
print("Return Code:", result.returncode)
