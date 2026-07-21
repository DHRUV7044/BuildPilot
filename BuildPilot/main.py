import subprocess


result = subprocess.run(
    ['git', '--version'],
    text=True,
    capture_output=True
)

print("Git Version:", result.stdout.strip())
print("Return Code:", result.returncode)
