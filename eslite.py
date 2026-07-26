import requests
import model_manager
from athena import Athena

class Eslite:

    BASE_URL = "https://holmes.eslite.com/v1/search"

    def __init__(self, keyword):

        self.keyword = keyword

    def get_products(self):

        athena = Athena()

        products = []

        page = 1

        while True:

            print(f"讀取誠品 Page {page}")

            added = 0

            params = {
                "q": self.keyword,
                "page_size": 20,
                "page_no": page,
                "sort": "desc",
                "branch_id": 0,
                "facet": "false"
            }

            try:

                response = requests.get(
                    self.BASE_URL,
                    params=params,
                    timeout=20
                )

                response.raise_for_status()

            except requests.RequestException as e:

                print("誠品連線失敗")

                return []

            data = response.json()

            results = data.get("results", [])

            if len(results) == 0:
                break

            for item in results:

                import json

                name = item["name"]

                model = model_manager.extract_model(name)

                if not model:
                    continue

                # 到這裡代表是真正要監控的商品才印
                print(
                    name,
                    item.get("availability"),
                    item.get("button_status")
                )

                guid = item["id"]

                athena_data = athena.get_price(guid)

                print(guid)
                print(athena_data)

                if athena_data:

                    button = athena_data["button_status"]

                    can_buy = athena_data["inventory"] == 1

                    inventory = athena_data["inventory"]

                else:

                    button = item.get("button_status", "")

                    can_buy = (button == "add_to_shopping_cart")

                    inventory = 1 if can_buy else 0

            
                display_status = "可購買" if can_buy else "不可購買"

                products.append({

                    "site": "Eslite",

                    "model": model,

                    "id": item["id"],

                    "name": item["name"],

                    "url": f"https://www.eslite.com/product/{item['id']}",

                    "inventory": inventory,

                    "availability": item.get("availability"),

                    "button_status": button,

                    "price": athena_data["price"] if athena_data else None,

                    "can_buy": can_buy,

                    "display_status": display_status

                })

                added += 1

                print(f"API 回傳 {len(results)} 筆，符合條件 {added} 筆")

            if len(results) < 20:
                break

            page += 1

        return products