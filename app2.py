from google.cloud import secretmanager
from google.api_core.exceptions import NotFound

def get_secret(secret_id, project_id):
    """
    Retrieve the latest version of a secret from Google Cloud Secret Manager.

    :param secret_id: The name of the secret (e.g., "db_password").
    :param project_id: GCP project ID where the secret is stored.
    :return: Secret string if successful, None otherwise.
    """
    client = secretmanager.SecretManagerServiceClient()

    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    try:
        response = client.access_secret_version(request={"name": name})
        secret_value = response.payload.data.decode("UTF-8")
        return secret_value

    except NotFound:
        print(f"Secret '{secret_id}' not found in project '{project_id}'.")
        return None
    except Exception as e:
        print(f"Error accessing secret: {e}")
        return None

if __name__ == "__main__":
    # Replace with your actual GCP project and secret ID
    PROJECT_ID = "my-gcp-project"
    SECRET_ID = "db-password"

    secret = get_secret(SECRET_ID, PROJECT_ID)

    if secret:
        print("✅ Retrieved secret value successfully:")
        print(secret)
    else:
        print("❌ Failed to retrieve secret.")
