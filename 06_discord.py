import requests
import datetime


discord = "https://discord.com/api/webhooks/1177931669756461196/KzVlnTu3__p664r35nqvntU6eBBg3m9xWO1pVnTbpo-nx_fHlIfw7c00LsYFm9wt0dia"

def send_message(msg):
    """디스코드 메세지 전송"""
    now = datetime.datetime.now()
    message = {"content": f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {str(msg)}"}
    requests.post(discord, data=message)
    print(message)

send_message(f"====주식 보유잔고====")
