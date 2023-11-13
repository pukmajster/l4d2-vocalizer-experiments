import os
import json

# These tell us to which survivor each line belongs to.
playerNames = [
  #l4d1
  "TeenGirl", "NamVet", "Biker", "Manager",
  #l4d2
  "Coach", "Mechanic", "Gambler", "Producer"
]

criteriaToKeep = []

for playerName in playerNames:
  criteriaToKeep.append("Is" + playerName)
  criteriaToKeep.append("IsTalk" + playerName)
  criteriaToKeep.append("IsWorldTalk" + playerName)

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

    # If we're in a rule block, check if the line contains a criterion.
    if isInRuleBlock:

      if "criteria" in readLine:

        # Prep the new line
        reworkedRuleCriteria = "\tcriteria "

        readCriteria = _line.split(" ")
        
        # Remove the "criteria" word from the list
        readCriteria.pop(0)

        # Append the second criterion to the list always
        reworkedRuleCriteria += readCriteria.pop(0)

        # Loop through the remaining criteria and check if they're in the list of criteria to keep.
        for criterion in readCriteria:
          if criterion in criteriaToKeep:
            reworkedRuleCriteria += " " + criterion
        
        # Add the new line to the results
        results.append(reworkedRuleCriteria + "\n")
        continue
    
    if "}" in readLine:
      isInRuleBlock = False

    if "rule" in readLine:
      isInRuleBlock = True

    results.append(_line)




  # Write file to disk
  # I used to write all the data into one file and that worked great until the gigabytes took our land.
  fPath = file.replace("l4d2_scripts", "stfu") 
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
