from azure.keyvault import KeyVaultClient, KeyVaultAuthentication
from azure.common.credentials import ServicePrincipalCredentials
import os

credentials = None

credentials = ServicePrincipalCredentials(
    client_id = os.getenv('APP_ID'),
    secret = os.getenv('SECRET_APP_KEY'),
    tenant = os.getenv('TENANT_ID')
)
token = credentials.token

VaultUrl = os.getenv('VAULT_URL')

client = KeyVaultClient(credentials)

azureSendGrid = client.get_secret(VaultUrl, 'AzureSendGridUser', '').value
azureSendGridPassword = client.get_secret(VaultUrl, 'AzureSendGridPassword', '').value
dbHostServer = client.get_secret(VaultUrl, 'DatabaseHostServer', '').value
dbPassword = client.get_secret(VaultUrl, 'DatabasePassword', '').value
dbName = client.get_secret(VaultUrl, 'DatabaseName', '').value
dbUser = client.get_secret(VaultUrl, 'DatabaseUser', '').value
djangoSecretKey = client.get_secret(VaultUrl,'DjangoSecretKey','').value
apiKeyTMDB = client.get_secret(VaultUrl,'APIKeyTMDB','').value

f = open("config.py", "w")
f.write("AZURE_SEND_GRID = '"+ azureSendGrid + "'\n")
f.write("AZURE_SEND_GRID_PASSWORD = '"+azureSendGridPassword+"'\n")
f.write("DATABASE_HOST_SERVER = '"+ dbHostServer+ "'\n")
f.write("DATABASE_PASSWORD = '"+ dbPassword+ "'\n")
f.write("DATABASE_NAME = '"+ dbName+ "'\n")
f.write("DATABASE_USER = '"+ dbUser+ "'\n")
f.write("DJANGO_SECRET_KEY = '"+ djangoSecretKey+ "'\n")
f.write("TMDB_API_KEY = '"+ apiKeyTMDB + "'\n")