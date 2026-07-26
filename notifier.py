import requests
from config import WEBHOOK_URL


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

        print("Status:", response.status_code)
        print("Response:", response.text)

        return response.status_code == 204