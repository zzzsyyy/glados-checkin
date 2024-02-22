import os
import requests

def glados():
    cookie = os.getenv('COOKIE')
    if not cookie:
        return
    try:
        headers = {
            'cookie': cookie,
            'referer': 'https://glados.one/console/checkin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
            'content-type': 'application/json',
        }
        checkin_response = requests.post('https://glados.one/api/user/checkin', headers=headers, json={"token": "glados.one"})
        checkin = checkin_response.json()
        
        status_response = requests.get('https://glados.one/api/user/status', headers=headers)
        status = status_response.json()
        
        return [
            'Checkin OK',
            f"{checkin['message']}",
            f"Left Days {float(status['data']['leftDays'])}",
        ]
    except Exception as error:
        return [
            'Checkin Error',
            str(error),
            f"<{os.getenv('GITHUB_SERVER_URL')}/{os.getenv('GITHUB_REPOSITORY')}>",
        ]

def notify(data):
    key = os.getenv('KEY')
    if not key:
        return
    url = f'https://sctapi.ftqq.com/{key}.send'
    params = {
        'title': data[0],
        'desp': '\n'.join(data),
    }
    resp = requests.post(url, params=params)
    return resp

def main():
    contents = glados()
    if contents:
        notify(contents)

if __name__ == "__main__":
    main()

