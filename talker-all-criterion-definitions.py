import os

scriptsPath = "./l4d2_scripts"
filesToCheck = [""]
filesToCheck.clear()

# Walk through the scripts folder and get all the files that are present within the "talker" directory
for root, dirs, files in os.walk(scriptsPath):
  for file in files:
    if file.endswith(".txt"):
      if "talker" in root:
        fullPath = os.path.join(root, file)
        # print("Found file: " + fullPath)
        filesToCheck.append(fullPath)

        # Convert to utf-8 because some files got weird characters
        # Not my finest work but it does the job
        #f = open(fullPath, "rb")
        #content = f.read().decode("ISO-8859-1", "ignore")
        #f.close()

        #f = open(fullPath, "w", encoding="utf-8")
        #f.write(content)
        #f.close()

results = []
uniqueCriteria = []

for file in filesToCheck:
  # Open the file and read all the lines.
  try:
    f = open(file, "r")
    lines = f.readlines()
    print("Reading file: " + file)
    f.close()
  except:
    print("Error reading file: " + file)
    continue

  results.append("\n\n// --------------------------------------------------\n")
  results.append("// " + file + "\n")
  results.append("// --------------------------------------------------\n\n")

  # Loop through each line.
  for _line in lines:
    readLine = _line.lower().strip()

    if "criteria " in readLine:
      results.append(_line.strip() + "\n")

      split = _line.strip().split(" ")
      criteria = split.pop(0)
      concept = split.pop(0)

      for criterion in split:
        if criterion not in uniqueCriteria:
          uniqueCriteria.append(criterion)
      continue

uniqueCriteria = " ".join(uniqueCriteria)

f = open("criteria/all criteria.txt", "w+")
f.writelines(results)
f.close()

f = open("criteria/unique crietira.txt", "w+")
f.writelines(uniqueCriteria)
f.close()

print("Done!")
