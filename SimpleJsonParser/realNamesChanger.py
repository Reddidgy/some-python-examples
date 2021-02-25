import json

filename = 'input/source.json'
filename_opened = open(filename,mode='r')

j = json.load(filename_opened)
filename_opened.close()

'''
{
    "resourceName": "RESOURCENAME",             1
    "parameterList": [                          2
      "PARAM1",
      "PARAM2"
    ],
    "resourceGroup": "General",                 3
    "enabledReport": "false"                      4
}
'''



resourceNameDict = {}
currentResourceNameID = 0
parametersDict = {}
parametersArray = []
currentParameterID = 0
groupsDict = {}
currentGroupID = 0
readyArray = []

for resource in j:
    newResourceDict = {}
    # changing resource name and putting to new resource dict.
    # We have unic resource names so we don't use if here
    currentResourceNameID += 1
    resourceNameDict.update({currentResourceNameID:resource["resourceName"]})
    replacedResourceName = "RESOURSE_NAME_" + str(currentResourceNameID)
    newResourceDict.update({"resourceName":replacedResourceName})


    # saving params count and changing param names. Also putting it to newResourceDict
    parametersArray = []
    for p in resource["parameterList"]:
        if p not in parametersDict.values():
            currentParameterID += 1
            parametersDict.update({currentParameterID:p})
            replacedParameterName = "PARAM" + str(currentParameterID)
            parametersArray.append(replacedParameterName)
        else:
            for id, value in parametersDict.items():
                if value == p:
                    replacedParameterName = "PARAM" + str(id)
                    parametersArray.append(replacedParameterName)
    newResourceDict.update({"parameterList": parametersArray})

    # changing resource group. We don't have only unic group. So we should use conditions about existing groups
    realGroupName = resource["resourceGroup"]
    if realGroupName not in groupsDict.values():
        currentGroupID += 1
        groupsDict.update({currentGroupID:realGroupName})
        replacedGroupName = "GROUP" + str(currentGroupID)
    else:
        for id, group in groupsDict.items():
            if group == realGroupName:
                replacedGroupName = "GROUP" + str(id)
    newResourceDict.update({"resourceGroup":replacedGroupName})

    # Adding information about EnabledResource. Just repeating true or false here.
    newResourceDict.update({"enabledResource":str(resource["enabledResource"]).lower()})
    # Adding newResourceDict as object in new array list for final json
    readyArray.append(newResourceDict)
    newResourceDict = {}

for i in readyArray:
    print(i)
# readyArray is ready :) for json dump

fileToRecord = 'input/newSourceFile' + '.json'
filename_opened = open(fileToRecord,mode='w')

json.dump(readyArray, filename_opened)
filename_opened.close()