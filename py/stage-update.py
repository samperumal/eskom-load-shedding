import json
import city_sites

def writeBlob(key):
    from azure.storage.blob import BlobServiceClient, ContentSettings

    service = BlobServiceClient(account_url="https://cptloadshed.blob.core.windows.net/", credential=key)

    blob = service.get_blob_client("stage", "current.json")

    data = {
        "Cape Town": city_sites.parseCpt(),
        "Johannesburg": city_sites.parseJhb(),
        "Durban": None,
        "Tshwane (Pretoria)": city_sites.parsePta()
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
