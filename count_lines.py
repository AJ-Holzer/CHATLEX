import os

line_num: int = 0

# Count all lines in every file
for root, _, filenames in os.walk("./"):
    if any(word in root for word in ["build", ".history", ".backup", ".trunk"]):
        continue

    for filename in filenames:
        if not filename.endswith(".py"):
            continue

        file_path: str = os.path.join(root, filename)

        print(f"Analyzing '{file_path}'...")

        with open(file_path, "r", encoding="UTF-8") as f:
            for line in f.readlines():
                converted_line: str = line.strip()

                if converted_line.startswith("#") or not line:
                    continue

                line_num += 1

print(line_num)
