from flask import Flask, request, jsonify
import requests
import time
from rich.console import Console
from rich.progress import Progress

app = Flask(__name__)
console = Console()

def check_player_info(target_id):
    with Progress() as progress:
        task = progress.add_task("[cyan]Fetching player data...", total=100)

        cookies = {
            '_ga': 'GA1.1.2123120599.1674510784',
            '_fbp': 'fb.1.1674510785537.363500115',
            '_ga_7JZFJ14B0B': 'GS1.1.1674510784.1.1.1674510789.0.0.0',
            'source': 'mb',
            'region': 'MA',
            'language': 'ar',
            '_ga_TVZ1LG7BEB': 'GS1.1.1674930050.3.1.1674930171.0.0.0',
            'datadome': '6h5F5cx_GpbuNtAkftMpDjsbLcL3op_5W5Z-npxeT_qcEe_7pvil2EuJ6l~JlYDxEALeyvKTz3~LyC1opQgdP~7~UDJ0jYcP5p20IQlT3aBEIKDYLH~cqdfXnnR6FAL0',
            'session_key': 'efwfzwesi9ui8drux4pmqix4cosane0y',
        }

        headers = {
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Origin': 'https://shop2game.com',
            'Referer': 'https://shop2game.com/app/100067/idlogin',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
            'accept': 'application/json',
            'content-type': 'application/json',
            'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'x-datadome-clientid': '6h5F5cx_GpbuNtAkftMpDjsbLcL3op_5W5Z-npxeT_qcEe_7pvil2EuJ6l~JlYDxEALeyvKTz3~LyC1opQgdP~7~UDJ0jYcP5p20IQlT3aBEIKDYLH~cqdfXnnR6FAL0',
        }

        json_data = {
            'app_id': 100067,
            'login_id': target_id,
            'app_server_id': 0,
        }

        try:
            progress.update(task, advance=50)
            res = requests.post('https://shop2game.com/api/auth/player_id_login',
                                cookies=cookies, headers=headers, json=json_data)

            if res.status_code != 200 or not res.json().get('nickname'):
                return {"error": "ID NOT FOUND"}

            progress.update(task, advance=50)
            player_data = res.json()
            nickname = player_data.get('nickname', 'N/A')
            region = player_data.get('region', 'N/A')

            return {
                "nickname": nickname,
                "region": region
            }

        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

@app.route('/api/player/check-region', methods=['GET'])
def get_region_info():
    uid = request.args.get('uid')
    if not uid:
        return jsonify({
            "status": "error",
            "message": "UID parameter is required",
            "credit": "@Ujjaiwal",
            "channel": "https://t.me/GlobleEarth_Gaming"
        }), 400

    start_time = time.time()
    result = check_player_info(uid)
    end_time = time.time()

    if "error" in result:
        return jsonify({
            "status": "error",
            "message": result["error"],
            "credit": "@Ujjaiwal",
            "channel": "https://t.me/GlobleEarth_Gaming"
        }), 404

    return jsonify({
        "status": "success",
        "message": "Player region fetched successfully",
        "response_time_ms": int((end_time - start_time) * 1000),
        "credit": "@Ujjaiwal",
        "channel": "https://t.me/GlobleEarth_Gaming",
        "data": result
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)