import json
import os

def verificar_refresh_token():
    token_path = "credentials/token.json"
    if not os.path.exists(token_path):
        print("❌ No existe el archivo token.json.")
        return

    with open(token_path, "r") as f:
        try:
            data = json.load(f)
            refresh_token = data.get("refresh_token")
            if refresh_token:
                print("✅ El archivo token.json contiene un refresh_token válido.")
            else:
                print("⚠️ El archivo token.json NO contiene un refresh_token.")
        except json.JSONDecodeError:
            print("❌ El archivo token.json no tiene un formato JSON válido.")

if __name__ == "__main__":
    verificar_refresh_token()
