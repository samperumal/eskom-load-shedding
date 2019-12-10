import json 

def readLines():
    with open("py/jhb.txt", "r") as f:
        lines = f.readlines()
        block1 = lines[76:108]
        block2 = lines[158:190]
        block3 = lines[240:272]

        lines = block1 + block2 + block3

        return lines

def createBlockStages(block):
    block = { 
        "block": block, 
        "start": '{:0>2}:00'.format(block * 2), 
        "end": '{:0>2}:30'.format((block + 1) * 2), 
        "stages": [{"stage": stage, "zones":[]} for stage in range(1, 9)] 
    }

    return block

lines = readLines()

data = [{"day": day + 1, "blocks": [createBlockStages(block) for block in range(12)]} for day in range(31)]
zoneSet = set()

block = 0
stage = 0
for line in lines:
    zones = line.split()
    day = 0
    for zone in zones:
        data[day]["blocks"][block]["stages"][stage]["zones"] = [zone]
        zoneSet.add(zone)
        day = day + 1
    stage = stage + 1
    if stage == 8:
        stage = 0
        block = block + 1

zoneList = list(zoneSet)
zoneList.sort()

jhbData = {
    "zones": zoneList,
    "matrix": data
}

with open("src/js/jhb.json", "w") as fout:
    print(json.dumps(jhbData, indent=2), file = fout)

