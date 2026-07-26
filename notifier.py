import requests
from config import WEBHOOK_URL, LINE_CHANNEL_ACCESS_TOKEN


class Notifier:

    def send(self, product, reason):

        if reason == "new":
            title = "🆕 新商品"

        elif reason == "restock":
            title = "🎉 補貨"

        else:
            title = "📢 商品通知"

        message = (
            f"{title}\n\n"
            f"商品：{product['name']}\n"
            f"狀態：{product['display_status']}\n"
            f"網址：{product['url']}"
        )

        response = requests.post(
            WEBHOOK_URL,
            json={
                "content": message
            },
            timeout=10
        )

        self.send_line(message)

        print("Status:", response.status_code)
        print("Response:", response.text)

        return response.status_code == 204
    def send_line(self, message):

        headers = {
            "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        data = {
            "to": "U2e156da7b872114a21c02277a46bd7a7",
            "messages": [
                {
                    "type": "text",
                    "text": message
                }
            ]
        }

        response = requests.post(
            "https://api.line.me/v2/bot/message/push",
            headers=headers,
            json=data,
            timeout=10
        )

        print("LINE:", response.status_code)
        print(response.text)