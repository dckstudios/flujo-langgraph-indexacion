from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

def get_authenticated_drive():
    creds_dir = "credentials"
    settings_path = os.path.join(creds_dir, "settings.yaml")
    token_file = os.path.join(creds_dir, "token.json")

    gauth = GoogleAuth(settings_file=settings_path)

    if os.path.exists(token_file):
        gauth.LoadCredentialsFile(token_file)
        if gauth.access_token_expired:
            if gauth.refresh_token:
                print("🔄 Refrescando token...")
                gauth.Refresh()
            else:
                print("❌ Token expirado sin refresh_token. Reautenticando...")
                gauth.CommandLineAuth()
                gauth.SaveCredentialsFile(token_file)
        else:
            gauth.Authorize()
    else:
        print("🌐 Autenticación inicial...")
        gauth.CommandLineAuth()
        gauth.SaveCredentialsFile(token_file)

    return GoogleDrive(gauth)
