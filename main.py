import pandas as pd
import datetime
import sys

INPUT_CSV_FILE = "./item_list.csv"
OUTPUT_TEXT_PATH = "./receipt/{datetime}.txt"

#商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self):
        return self.price

#オーダークラス
class Order:
    def __init__(self,item_master):
        self.order_code_list = []
        self.item_master = item_master
        self.set_datetime()

    def set_datetime(self):
        self.datetime=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    
    def add_order_list(self,item_code,amount):
        self.order_code_list.append([item_code,amount])

    def input_order(self):
        flag = True
        while flag:
            order_code = input("注文したい商品のコード番号を入力してください >> ")
            if self.get_item_data(order_code)[0]:
                amount_input = input("数量を入力してください >> ")
                self.add_order_list(order_code,amount_input)
            else:
                print("商品が見つかりません")
                continue
            while True:
                continue_or_not = input("続けて入力しますか？(y/n) >> ") 
                if continue_or_not == "y":
                    flag = True
                    break
                elif continue_or_not == "n":
                    flag = False
                    break
                else:
                    print("y/nで選択してください")
                    continue
        
    def view_item_list(self):
        self.write_receipt("-----購入商品-----")
        for order_code in self.order_code_list:
            self.write_receipt(f"商品コード:{order_code[0]} 商品名:{self.get_item_data(order_code[0])[1]} 値段:{self.get_item_data(order_code[0])[2]} 個数:{order_code[1]}")
        self.write_receipt("------------------")

    def get_item_data(self,order_code):
        for item in self.item_master:
            if item.item_code == order_code:
                return True, item.item_name, item.price
        print("商品コードに対応するアイテムが見つかりませんでした")
        return False,"None","None"

    def input_money(self):
        money = input("お金を入力してください")
        self.write_receipt(f"お預かり金額:{money}")
        return money

    def sum_calc(self):
        sum = 0
        for order_code in self.order_code_list:
            sum += self.get_item_data(order_code[0])[2] * int(order_code[1])
        self.write_receipt(f"合計:{sum}")
        money = int(self.input_money())
        change = money - sum
        self.write_receipt(f"お釣り:{change}")

    def write_receipt(self,text):
        print(text)
        with open(OUTPUT_TEXT_PATH.format(datetime=self.datetime),mode="a",encoding="utf-8_sig") as f:
            f.write(text+"\n")

#CSVファイルからマスタを読み込み
def get_item_master_from_csv(path):
    try:
        df = pd.read_csv(path,dtype={0:object})
        # マスタ登録
        item_master=[]
        for row in df.itertuples():
            item_master.append(Item(row[1],row[2],row[3]))
        print("-----商品リスト-----")
        for i in item_master:
            print(f"{i.item_code}  {i.item_name}  {i.price}")
        print("--------------------")
        return item_master
    except:
        print("登録失敗")
        sys.exit()
    
#メイン処理
def main():
    item_master = get_item_master_from_csv(INPUT_CSV_FILE)
    order = Order(item_master)
    order.input_order()
    order.view_item_list()
    order.sum_calc()

if __name__ == "__main__":
    main()