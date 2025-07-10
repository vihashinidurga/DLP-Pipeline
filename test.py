from google.cloud import dlp_v2

client = dlp_v2.DlpServiceClient()
parent = "projects/pii-goldset-9023/locations/us-central1"

print("Inspect Templates:")
for template in client.list_inspect_templates(request={"parent": parent}):
    print(template.name)

print("\nDeidentify Templates:")
for template in client.list_deidentify_templates(request={"parent": parent}):
    print(template.name)
