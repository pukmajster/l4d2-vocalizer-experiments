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

for file in filesToCheck:

  results = []

  # Open the file and read all the lines.
  try:
    f = open(file, "r")
    lines = f.readlines()
    print("Reading file: " + file)
    f.close()
  except:
    print("Error reading file: " + file)
    continue

  isInRuleBlock = False

  # Loop through each line.
  for _line in lines:
    readLine = _line.lower().strip()

    if "criteria ConceptRemark IsGambler Isc5m4pooltable IsNotSaidc5m4pooltable IsNotCoughing NotInCombat IsTalk IsTalkGambler IsWorldTalkGambler IsSubjectNear200 ChanceToFire20Percent TimeSinceGroupInCombat02 AutoIsNotScavenge AutoIsNotSurvival IsNotSpeakingWeight0" in _line:
      results.append("crietria ConceptRemark isGambler")
      continue

    results.append(_line)

  # Write file to disk
  # I used to write all the data into one file and that worked great until the gigabytes took our land.
  fPath = file.replace("l4d2_scripts", "ilovepool") 
  fPath = fPath.split("/")
  fileName = fPath.pop()
  fPath = "/".join(fPath) + "/"

  if not os.path.exists(fPath):
    os.makedirs(fPath)

  textFileName = fPath + fileName  

  f = open(textFileName, "w+")
  f.writelines(results)
  f.close()





print("Done!")
