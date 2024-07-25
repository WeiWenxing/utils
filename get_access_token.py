SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
#SCOPES = ['https://www.googleapis.com/auth/cloud-speech']
SERVICE_ACCOUNT_FILE = '/home/ubuntu/super_key.json'
#SERVICE_ACCOUNT_FILE = '/etc/.1f19339104faee58f0668bcb55603ab83dbcb011'

from google.oauth2 import service_account
from google.auth.transport.requests import Request

creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
creds.refresh(Request())
token = creds.token
print(token)
