import requests


class Athena:

    BASE_URL = "https://athena.eslite.com/api/v2/products"

    def get_price(self, guid):

        url = f"{self.BASE_URL}/{guid}/prices"

        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()

            data = r.json()

            if not data:
                return None

            item = data[0]

            return {
                "price": item.get("final_price"),
                "button_status": item.get("product_button_status"),
                "status": item.get("product_button_status"),
                "inventory": 1 if item.get("product_button_status") == "can_buy" else 0,
            }

        except Exception as e:
            print(f"Athena API 失敗：{guid} -> {e}")
            return None