import json
from datetime import datetime, date, time

filename = 'input/source.json'
filename_opened = open(filename,mode='r')

j = json.load(filename_opened)
filename_opened.close()
fullParamList = []
fullParamListWoR = []

for x in range(0,len(j)):
    fullParamList = fullParamList + j[x]["parameterList"]

for x in fullParamList:
    if x not in fullParamListWoR:
        fullParamListWoR.append(x)
fullParamListWoR.sort()                     # filling array of parameters without repeates

nplist = []                                 # creating array for cover each parameter with saving IDs
for p in range(0,len(fullParamListWoR)):    # for future tasks ID is always 0 on this step
    if len(nplist) > 0:
        nplist.append([{fullParamListWoR[p]:0},0])
    else:
        nplist = [[{fullParamListWoR[p]:0},0]]


for e in range(0,len(nplist)):                                  # it's crazy. I'm so sad I didn't write
    for fkey in nplist[e][0].keys():                            # comments here.... I can't understand
        for r in range(0, len(j)):                              # the logic of past Rodion here. sorry
            if fkey in j[r]["parameterList"]:
                if nplist[e][0][fkey] == 0:                             # it's matching how much parameters
                    nplist[e][0].update({fkey:j[r]["resourceName"]})    # and re-checking that covered all ones

                    nplist[e][1] = len(j[r]["parameterList"])
                else:
                    if len(j[r]["parameterList"]) > nplist[e][1]:
                        nplist[e][0].update({fkey:j[r]["resourceName"]})


finalList = []

finalJsonList = []
for i in nplist:
    for r in i[0].values():
        if r not in finalList:
            finalList.append(r)

for i in range(0,len(j)):
    if j[i]["resourceName"] in finalList:
        finalJsonList.append(j[i])

d = str(datetime.now(tz=None))
clearDateTime = ''

for i in d:
    if i == ".":
        break
    if i == ":":
        clearDateTime = clearDateTime + "-"
    if i in "1234567890 -":
        clearDateTime = clearDateTime + i

fileToRecord = 'output/output' + clearDateTime + '.json'
filename_opened = open(fileToRecord,mode='w')

json.dump(finalJsonList, filename_opened)
filename_opened.close()
unicParamCount = {}
for i in range(0, len(finalJsonList)):
    for p in finalJsonList[i]["parameterList"]:
        if p not in unicParamCount:
            unicParamCount.update({p:1})
        else:
            unicParamCount.update({p: unicParamCount[p] + 1})
unicParamCount = [unicParamCount]

fileToRecord = 'output/UnicParamCount' + clearDateTime + '.json'
filename_opened = open(fileToRecord,mode='w')

json.dump(unicParamCount, filename_opened)
filename_opened.close()

print(nplist)