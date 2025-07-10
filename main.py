import time
# import functions_framework
from google.cloud import storage
from google.cloud import dlp_v2
from google.cloud import bigquery

# ENV CONFIG
PROJECT_ID = "project-id"
BQ_DATASET = "bigquery-dataset-id"
BQ_TABLE = "bigquery-table-id"


INSPECT_TEMPLATE_ID = "inspect-template"
DEID_TEMPLATE_ID = "deid-template"

INSPECT_TEMPLATE_NAME = f"projects/{PROJECT_ID}/locations/us-central1/inspectTemplates/{INSPECT_TEMPLATE_ID}"
DEID_TEMPLATE_NAME = f"projects/{PROJECT_ID}/locations/us-central1/deidentifyTemplates/{DEID_TEMPLATE_ID}"

# Clients
storage_client = storage.Client()
dlp_client = dlp_v2.DlpServiceClient()
bq_client = bigquery.Client()

def read_gcs_file(bucket_name, blob_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    return blob.download_as_text()

def insert_bq_row(row):
    table_ref = f"{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"
    errors = bq_client.insert_rows_json(table_ref, [row])
    if errors:
        print(f"BigQuery errors: {errors}")

def process_file(bucket_name, blob_name):
    gcs_uri = f"gs://{bucket_name}/{blob_name}"
    chunk_id = blob_name

    text = read_gcs_file(bucket_name, blob_name)
    item = {"value": text}

    # Inspect with template
    inspect_response = dlp_client.inspect_content(
        request={
            "parent": f"projects/{PROJECT_ID}/locations/us-central1",
            "inspect_template_name": INSPECT_TEMPLATE_NAME,
            "item": item
        }
    )

    # De-ID with template
    deid_response = dlp_client.deidentify_content(
        request={
            "parent": f"projects/{PROJECT_ID}/locations/us-central1",
            "inspect_template_name": INSPECT_TEMPLATE_NAME,
            "deidentify_template_name": DEID_TEMPLATE_NAME,
            "item": item
        }
    )

    masked_text = deid_response.item.value
    findings = inspect_response.result.findings

    if not findings:
        row = {
            "chunk_id": chunk_id,
            "gcs_uri": gcs_uri,
            "masked_text": masked_text,
            "infoType": None,
            "likelihood": None,
            "start_offset": None,
            "end_offset": None,
            "create_time": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        insert_bq_row(row)
    else:
        for f in findings:
            row = {
                "chunk_id": chunk_id,
                "gcs_uri": gcs_uri,
                "masked_text": masked_text,
                "infoType": f.info_type.name,
                "likelihood": dlp_v2.Likelihood(f.likelihood).name,
                "start_offset": f.location.byte_range.start,
                "end_offset": f.location.byte_range.end,
                "create_time": time.strftime('%Y-%m-%d %H:%M:%S')
            }
            insert_bq_row(row)

# ✅ Cloud Function entry point for GCS file upload
@functions_framework.cloud_event
def process_uploaded_chunk(cloud_event):
    data = cloud_event.data
    bucket = data["bucket"]
    file_name = data["name"]

    print(f"Triggered by file upload: gs://{bucket}/{file_name}")
    process_file(bucket, file_name)
    return "File processed!"
