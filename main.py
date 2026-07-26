from time import sleep

from database import Database
from eslite import Eslite
from notifier import Notifier
from config import KEYWORDS, INTERVAL

def main():

    db = Database()
    notifier = Notifier()
   

    while True:

        print("=" * 60)
        print("開始搜尋")

        all_products = []

        for keyword in KEYWORDS:

            print(f"\n搜尋：{keyword}")

            products = Eslite(keyword).get_products()

            print(f"取得 {len(products)} 筆商品")

            all_products.extend(products)


        for product in all_products:

            old = db.get_product(product["id"])

            notify, reason = db.need_notify(old, product)

            if notify:

                success = notifier.send(product, reason)

                if success:
                    db.update_notify_time(product["id"])

            db.save_product(product)

        print(f"等待 {INTERVAL} 秒")
        sleep(INTERVAL)


if __name__ == "__main__":
    main()