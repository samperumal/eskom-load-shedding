import json
import math
import re


with open("cpt-raw.csv", 'r') as f:
  state = 0
  stage = 1

  stage_blocks = [[] for _ in range(8)]

  for line in f.readlines():
    state += 1
    if state <= 4:
      continue

    block = line[:12]
    zones = re.sub(', *', '|', line[12:].strip()).split(' ')
    # print(stage, zones)
    
    
    # print(math.floor(stage), [[x for x in "".join(g).split(', ')] for g in m])
    table_data = [[int(x) for x in g.split('|')] for g in zones]
    
    

    if stage < 5:
      stage_blocks[math.floor(stage) - 1].append(table_data + table_data)
    elif math.floor(stage * 10) % 10 == 0:
      stage_blocks[math.floor(stage) - 1].append(table_data)
    else:
      prev_table_data = stage_blocks[math.floor(stage) - 1][state-5]
      stage_blocks[math.floor(stage) - 1][state-5] = prev_table_data + table_data + prev_table_data + table_data

    if state == 16:
      state = 0
      if stage < 5:
        stage += 1
      else:
        stage += 0.5

  # print(json.dumps(stage_blocks, indent=2))
  with open("cpt-stage-block-day-zone.json", 'w') as o:
    print("[", file = o)
    for stage in stage_blocks:
      print("  [", file = o)
      for i in range(len(stage)):
        print("   ", stage[i], "," if i + 1 < len(stage) else "", file = o)
      print("  ],", file = o)
    print("]", file = o)

  # for zone in range(1, 17):
  #   for day in range (0, 31):
  #     for stage in range(0, 8):
  #       stage_blocks[stage].map(lambda b: b[day].includes(zone))
  #       pass

  def map_stage(zone, stage_data):
    [_ for stage_blocks in stage_data]
    pass

  result = [[[[0 for block in range(0, 12)] for day in range(0, 31)] for stage_index in range(0, 8)] for zone in range(0, 17)]
  for zone in range(1, 17):
    for day in range (0, 31):
      for stage_index in range(0, 8):
        block_check = list(map(lambda b: zone in b[day], stage_blocks[stage_index]))
        for block in range(0, 12):
          if result[zone][stage_index][day][block] == 0 and block_check[block]:
            for other_stage in range(stage_index, 8):
              result[zone][other_stage][day][block] = stage_index + 1
        # map(map_stage, stage_blocks) #[stage].map(lambda b: b[day].includes(zone))
        pass

  # print(result)

  with open("cpt-zone-stage-day-block.json", 'w') as o:
    print("[", file = o)
    for zone in result:
      print("  [", file = o)
      for stage_index in range(len(zone)):
        stage = zone[stage_index]
        print("    [", file = o)
        for day_index in range(len(stage)):
          print("     ", stage[day_index], "," if day_index + 1 < len(stage) else "", file = o)
        print("    ]" + ("," if stage_index + 1 < len(zone) else ""), file = o)
      print("  ],", file = o)
    print("]", file = o)  

  with open("cpt-zone-day-block.json", 'w') as o:
    print("[", file = o)
    for zone in result:
      print("  [", file = o)
      stage = zone[-1]
      for day_index in range(len(stage)):
        print("   ", stage[day_index], "," if day_index + 1 < len(stage) else "", file = o)
      print("  ],", file = o)
    print("]", file = o)
