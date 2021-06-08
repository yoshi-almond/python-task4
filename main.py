import pandas as pd
import datetime

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self):
        return self.price

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.order_code_list=[]
        self.item_master=item_master
    
    def add_order_list(self,item_code,amount):
        self.order_code_list.append([item_code,amount])
        
    def view_item_list(self,f):
        print("-----購入商品-----")
        f.write("-----購入商品-----\n")
        for order_code in self.order_code_list:
            print(f"商品コード:{order_code[0]} 商品名:{self.get_item_data(order_code[0])[1]} 値段:{self.get_item_data(order_code[0])[2]} 個数:{order_code[1]}")
            f.write(f"商品コード:{order_code[0]} 商品名:{self.get_item_data(order_code[0])[1]} 値段:{self.get_item_data(order_code[0])[2]} 個数:{order_code[1]}\n")
        print("------------------")
        f.write("------------------\n")

    def get_item_data(self,order_code):
        for item in self.item_master:
            if item.item_code == order_code:
                return True, item.item_name, item.price
        print("商品コードに対応するアイテムが見つかりませんでした")
        return False,"None","None"
    
    def sum_calc(self):
        sum = 0
        for order_code in self.order_code_list:
            sum += self.get_item_data(order_code[0])[2] * int(order_code[1])
        print(f"合計:{sum}円")
        return sum
    
    
### メイン処理
def main():
    path = './item_list.csv'
    df = pd.read_csv(path,dtype={0:object})
    # マスタ登録
    item_master=[]
    for row in df.itertuples():
        item_master.append(Item(row[1],row[2],row[3]))
    print("-----商品リスト-----")
    for i in item_master:
        print(f"{i.item_code}  {i.item_name}  {i.price}")
    print('--------------------')
    
    # オーダー登録
    order=Order(item_master)
    flag = True
    while flag:
        order_input = input("注文したい商品のコード番号を入力してください >> ")
        if order.get_item_data(order_input)[0]:
            amount_input = input("数量を入力してください >> ")
            order.add_order_list(order_input,amount_input)

        else:
            continue
        while True:
            continue_input = input("続けて入力しますか？(y/n) >> ") 
            if continue_input == "y":
                flag = True
                break
            elif continue_input == "n":
                flag = False
                break
            else:
                print("y/nで選択してください")
                continue
        
    
    # オーダー表示
    order.view_item_list(f)
    sum = order.sum_calc()
    pay_input = input("受け取り金額を入力してください　>> ")
    change = int(pay_input) - sum
    print(f"{change}円のお釣りです")
    f.write(f"合計 : {sum}\n")
    f.write(f"お預かり : {pay_input}\n")
    f.write(f"お釣り : {change}\n")

if __name__ == "__main__":
    OUTPUT_TEXT_PATH="./receipt/{datetime}.txt".format(datetime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    f = open(OUTPUT_TEXT_PATH,"w")
    main()
    f.close()