import json

def parseCoCTSite():

    return None

def writeBlob(key):
    from azure.storage.blob import BlobServiceClient

    service = BlobServiceClient(account_url="https://cptloadshed.blob.core.windows.net/", credential=key)

    blob = service.get_blob_client("stage", "current.json")

    data = {
        "Cape Town": parseCoCTSite(),
        "Johannesburg": None,
        "Durban": None
    }

    with open("current.json", "w") as fout:
        print(json.dumps(data, indent=2), file = fout)

    with open("current.json", "rb") as fin:
        blob.upload_blob(fin, overwrite = True)

    print("Successfully wrote blob")

key = ""

writeBlob(key)