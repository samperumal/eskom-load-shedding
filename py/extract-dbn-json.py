import json 

def readLines():
    with open("py/dbn.tsv", "r") as f:
        lines = f.readlines()
        
        return lines[1:13] + lines[14:26] + lines[27:39] + lines[40:52] + lines[53:65] + lines[66:78] + lines[79:91]

def createBlockStages(block):
    block = { 
        "block": block, 
        "start": '{:0>2}:00'.format(block * 2), 
        "end": '{:0>2}:30'.format((block + 1) * 2), 
        "stages": [{"stage": stage, "zones":[]} for stage in range(1, 9)] 
    }

    return block

lines = readLines()
print(len(lines) /12)
dayNames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

data = [{"day": dayNames[day], "blocks": [createBlockStages(block) for block in range(12)]} for day in range(7)]
zoneSet = set()

block = 0
stage = 1
for line in lines:
    parts = line.split()
    block = parts[0]
    blockNumber = int(block[0:2]) // 2
    day = int(parts[5])
    stages = [[str(y) for y in x.replace("\"", "").split(',')] for x in parts[1:5]]
    # print(blockNumber, block, stages, day)
    for stageNumber in range(8):
        if stageNumber  < len(stages):
            zones = stages[stageNumber]
        else: zones = stages[-1]
        data[day]["blocks"][blockNumber]["stages"][stageNumber]["zones"] = zones
        for zone in zones:
            zoneSet.add(zone)

zoneList = list(zoneSet)
zoneList.sort(key = lambda x: int(x))

dbnData = {
    "zones": zoneList,
    "matrix": data
}

with open("src/js/dbn.json", "w") as fout:
    print(json.dumps(dbnData, indent=2), file = fout)

