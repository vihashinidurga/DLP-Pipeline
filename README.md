## 📄 Project Setup Guide

Follow these steps to get started with this project:

---

### ✅ 1. Clone the Repository

```bash
git clone <REPO_URL>
cd <REPO_DIRECTORY>
```

---

### 🔑 2. Configure Google Cloud Service Account

1. Create or locate a **Service Account** in your Google Cloud project.
2. Generate a **Service Account JSON key file** with appropriate permissions (e.g., Cloud Functions Invoker, Storage Admin, DLP User if applicable).
3. Set your environment variable:

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
   ```

---

### 🚀 3. Deploy the Cloud Function

Use the following command to deploy `main.py` as a Google Cloud Function:

```bash
gcloud functions deploy process_uploaded_chunk \
  --runtime python311 \
  --trigger-resource <YOUR_GCS_BUCKET_NAME> \
  --trigger-event google.storage.object.finalize \
  --region us-central1 \
  --entry-point process_uploaded_chunk \
  --service-account <YOUR_CUSTOM_SERVICE_ACCOUNT_EMAIL>
```

**Parameters:**

* Replace `<YOUR_GCS_BUCKET_NAME>` with your bucket name.
* Replace `<YOUR_CUSTOM_SERVICE_ACCOUNT_EMAIL>` with your Service Account’s email.

---

### ⚙️ 4. Run the Chunk and Upload Script

Execute the local chunking and uploading script:

```bash
python chunk_and_upload.py
```

This script will:

* Chunk your files into manageable parts.
* Upload them to your specified GCS bucket.
* Trigger the deployed Cloud Function automatically.

---

## 📌 Notes

* Ensure that the bucket name matches the trigger resource used during deployment.
* Verify your environment variables are set correctly.
* You may need to install required dependencies listed in `requirements.txt`.

---

## ✅ Example Bucket Permissions

Make sure your Service Account has permissions for:

* `storage.objects.create`
* `cloudfunctions.functions.invoke`
* `Cloud Storage`
* `Cloud Functions`
* `Cloud DLP API`
* `BigQuery`

---

**Happy coding! 🚀**
