import requests

def door_lock(auth_token, vin):
    url = f"https://localhost:4443/api/1/vehicles/{vin}/command/door_lock"
    url = f"https://localhost:4443/api/1/vehicles/{vin}/vehicle_data"# エンドポイントのURLを指定
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    
    try:
        # POSTリクエストを送信
        response = requests.post(url, headers=headers, verify="./key_for_wolfy/config/tls-cert.pem")
        
        # レスポンスをチェック
        if response.status_code == 200:
            print("Vehicle is waking up successfully!")
            print(response.json())
        else:
            print(f"Failed to wake up vehicle. Status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error during wake up request: {e}")
