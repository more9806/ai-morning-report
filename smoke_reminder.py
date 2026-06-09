import os
import requests

WEBHOOK = os.environ["SMOKE_WEBHOOK"]

content = "温馨提示，到点了该抽烟了！"

payload = {
    "msgtype": "text",
    "text": {
        "content": content
    }
}

r = requests.post(WEBHOOK, json=payload, timeout=30)

print("企业微信返回状态码：", r.status_code)
print("企业微信返回内容：", r.text)

r.raise_for_status()

result = r.json()
if result.get("errcode") != 0:
    raise Exception(f"企业微信发送失败：{result}")

print("整点提醒已发送")
