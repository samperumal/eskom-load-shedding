import json
import city_sites
import re
from datetime import datetime as dt, timedelta
from dateutil.parser import parse


def get_cpt_input():
  with open("cpt-input.txt", "r") as f:
    return f.readlines()

def parse_cpt_input(lines):
  last_date = dt.utcnow().date()
  stages = []
  for line in lines:
    stage_match = re.match(r'Stage (\d+): (\d+:\d+) - (\d+:\d+)', line)
    date_match = re.match(r'([0-9]+) (\w+)', line)

    if stage_match is not None:
      start_time = dt.combine(last_date.date(), parse(stage_match[2]).time())
      end_time = dt.combine(last_date.date(), parse(stage_match[3]).time())
      if end_time < start_time:
        end_time += timedelta(1)
      stages.append({
        "stage": int(stage_match[1]), 
        "start": start_time.isoformat(), 
        "end": end_time.isoformat()
        })
    elif date_match is not None:
      last_date = parse(date_match[0])

  return stages

def writeBlob(key):
    from azure.storage.blob import BlobServiceClient, ContentSettings

    service = BlobServiceClient(account_url="https://cptloadshed.blob.core.windows.net/", credential=key)

    blob = service.get_blob_client("stage", "current.json")

    data = {
        "Cape Town": {
          "stages": parse_cpt_input(get_cpt_input()), #city_sites.parseCpt(),
          "url": "https://www.capetown.gov.za/Family%20and%20home/Residential-utility-services/Residential-electricity-services/Load-shedding-and-outages",
          "site": "CoCT",
          "time": dt.strftime(dt.now(), "%H:%M, %Y-%m-%d")
        },
        "Johannesburg": None, #city_sites.parseJhb(),
        "Durban": None,
        "Tshwane (Pretoria)": None, #city_sites.parsePta()
    }

    with open("current.json", "w") as fout:
        print(json.dumps(data, indent=2), file = fout)

    with open("current.json", "rb") as fin:
        blob.upload_blob(fin, overwrite = True)
        blob.set_http_headers(ContentSettings(content_type = "application/json"))

    print("Successfully wrote blob")

if __name__ == "__main__":
    with open("key.txt", "r") as key_file:
        key = key_file.read()
        writeBlob(key)
