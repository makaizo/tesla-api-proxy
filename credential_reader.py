import json

# credentials.jsonから認証情報を読み取る関数
def read_credentials(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            auth_token = data["authToken"]
            vin = data["vin"]
            mqtt_token = data["beebotteToken"]
            return auth_token, vin, mqtt_token
    except Exception as e:
        print(f"Error reading credentials: {e}")
        raise
