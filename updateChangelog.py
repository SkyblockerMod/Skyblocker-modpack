import sys
import re

# Read the Git diff from standard input
diff = sys.stdin.read()

# Patterns for searching for added, removed, and modified entries
added_pattern = re.compile(r'^\+name = "(.*)"$')
removed_pattern = re.compile(r'^-name = "(.*)"$')
modified_pattern = re.compile(r'^@@.*name = "(.*)"$')

# Initialize lists for added, removed, and modified entries
added = []
removed = []
modified = []

# Process the lines of the Git diff
for line in diff.split('\n'):
    added_match = added_pattern.match(line)
    removed_match = removed_pattern.match(line)
    modified_match = modified_pattern.match(line)
    if added_match:
        added.append(added_match.group(1))
    elif removed_match:
        removed.append(removed_match.group(1))
    elif modified_match:
        modified.append(modified_match.group(1))

# Generate the desired output
with open("CHANGELOG.md", "r+") as file:
    first_line = file.readline()

    # Extract the version number from the first line
    match = re.match(r"# Release (\d+\.\d+\.\d+)", first_line)
    if match:
        old_version = match.group(1)
        print(f"Old version number: {old_version}")

        # Increase the version number by 1
        major, minor, patch = map(int, old_version.split("."))
        new_version = f"{major}.{minor}.{patch+1}"

        print(f"New version number: {new_version}")

        file.seek(0)
        content = file.read()
        file.seek(0)

        file.write(f"# Release {new_version}\n\n")
        if modified:
            file.write('**Updated**\n')
            for item in modified:
                file.write(f'- {item}\n')

        if added:
            file.write('**Added**\n')
            for item in added:
                file.write(f'- {item}\n')

        if removed:
            file.write('**Removed**\n')
            for item in removed:
                file.write(f'- {item}\n')

        file.write("\n"+content)
        file.close
