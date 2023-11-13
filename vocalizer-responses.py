import os
import json

# These tell us to which survivor each line belongs to.
playerNames = [
  #l4d1
  "TeenGirl", "NamVet", "Biker", "Manager",
  #l4d2
  "Coach", "Mechanic", "Gambler", "Producer"
]

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

  resultsJson = {
    "Coach": {},
    "Mechanic": {},
    "Gambler": {},
    "Producer": {},
    "TeenGirl": {},
    "NamVet": {},
    "Manager": {},
    "Biker": {},
  }

  # Open the file and read all the lines.
  try:
    f = open(file, "r")
    lines = f.readlines()
    print("Reading file: " + file)
    f.close()
  except:
    print("Error reading file: " + file)
    continue

  isInResponseBlock = False
  isInRuleBlock = False
  isInCriterionBlock = False

  currentResponseBlockName = ""
  currentRuleBlockName = ""

  ruleBuilder = ""

  results.append("-------------------------------------------------------\n  " + file + "\n-------------------------------------------------------\n\n")
  

  # Loop through each line.
  for _line in lines:
    line = _line.strip().lower()
 
    # ----------------------------------------------------
    #
    # Response blocks
    #
    # ----------------------------------------------------
    if isInResponseBlock:
      if "scene" in line and "//" in line:
     
        # Get the scene player
        scenePlayer = ""

        for playerName in playerNames:
          if ("scenes/" + playerName.lower()) in line:
            scenePlayer = playerName
            break

        # Not a survivor line, skip it.
        if scenePlayer == "":
          continue

        # Explode the line to get the scene subtitles
        lineParts = _line.split("//")
        sceneSubtitles = lineParts[1].strip()

        # Store the scene data
        sceneResults = []
        sceneResults.append("RESPONSE " + currentResponseBlockName + " ")
        sceneResults.append("CHARACTER " + scenePlayer + " SUBTITLE \"" + sceneSubtitles + "\"\n" )
        results.extend(sceneResults)

        #Skip empty subtitles
        if sceneSubtitles == "":
          continue

        alreadyPresentKey = resultsJson[scenePlayer].get(currentResponseBlockName)
        if alreadyPresentKey == None:
          resultsJson[scenePlayer][currentResponseBlockName] = [sceneSubtitles]
        else:
          isAlreadyIncluded = sceneSubtitles in resultsJson[scenePlayer][currentResponseBlockName]
          if not isAlreadyIncluded:
            resultsJson[scenePlayer][currentResponseBlockName].append(sceneSubtitles)

        continue

    # ----------------------------------------------------
    #
    # Rule blocks
    #
    # ----------------------------------------------------
    if isInRuleBlock:
      if "criteria" in line:
        criteria = _line.split(" ")
        criteria.pop(0)
        criteria = " ".join(criteria).strip()
        ruleBuilder += " CRITERIA " + criteria 
        continue

      if "response" in line:
        response = _line.split(" ")[1].strip()
        ruleBuilder += " RESPONSE " + response
        continue

    # We are entering a response block
    if line.startswith("response"):
      isInResponseBlock = True
      currentResponseBlockName = _line.split(" ")[1].strip()
      continue
  
    # We are entering a rule block
    if line.startswith("rule"):
      isInRuleBlock = True
      currentRuleBlockName = _line.split(" ")[1].strip()
      ruleBuilder = "RULE " + currentRuleBlockName
      continue
  
    # We are entering a criterion block
    if line.startswith("criterion"):
      isInCriterionBlock = True
      continue

    # We are exiting a block
    if "}" in line:

      if isInRuleBlock:
        results.append(ruleBuilder + "\n")

      isInCriterionBlock = False
      isInRuleBlock = False
      isInResponseBlock = False
      currentResponseBlockName = ""
      currentRuleBlockName = ""
      ruleBuilder = ""
      continue
  
  results.append("\n\n\n")

  # Write file to disk
  # I used to write all the data into one file and that worked great until the gigabytes took our land.
  fPath = file.replace("l4d2_scripts", "out") 
  fPath = fPath.split("/")
  fileName = fPath.pop()
  fPath = "/".join(fPath) + "/"

  if not os.path.exists(fPath):
    os.makedirs(fPath)

  textFileName = fPath + fileName  
  jsonFileName = fPath + fileName.replace(".txt", ".json")

  f = open(textFileName, "w+")
  f.writelines(results)
  f.close()

  json_data = json.dumps(resultsJson, indent=2)
  with open(jsonFileName, 'w+') as outfile:
    outfile.write(json_data)
    outfile.close()



print("Done!")
