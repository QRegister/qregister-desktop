# -- coding: utf-8 --

item_name = ["Chiquta Banana", "Rees Buttercup", "Kanken Milk", "Barillla Linguini", "Creamson Heavy Cream",
             "Lore Shampoo", "Epola Paper Towels", "Pampa Dipers", "Shay Tomatoes", "Gawin Grapefruits"]
item_prize = [11.90, 17.90, 55.90, 44.95, 12.95, 10.95, 13.55, 24.90, 2.90, 3.90]
barcode = [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010]
item_prize_type = ['kg x', 'x 1', 'x 1', 'x 1', 'x 1', 'x 1', 'x 1', 'x 1', 'kg x', 'kg x']
# text import edicez burda da scann edilen barkodları olucak
scanned_items = [1002, 1003, 1004, 1005]
amount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
item_code = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# ilk etapta inventory yapmaya gerek yok ondan direk buraya yazdım bilgileri

for x in range(len(barcode)):
    for y in range(len(scanned_items)):
        if scanned_items[y] == barcode[x]:
            amount[x] += 1

qr_hash = ""

for x in range(len(barcode)):
    if amount[x] != 0:
        qr_hash += (str(item_code[x]) + '?' + str(amount[x]) + '%')

# bundan sonrası ters algoritma print için
print('hash', qr_hash)
backwards_num_item = []
backwards_amount_item = []

for x in range(len(qr_hash)):
    if qr_hash[x] == '?':
        stop_index = x
        backwards_num_item.append(qr_hash[x - 1])

    elif qr_hash[x] == '%':
        stop_index = x
        backwards_amount_item.append(qr_hash[x - 1])
print(backwards_num_item)
print(backwards_amount_item)

total = 0
for x in range(len(backwards_num_item)):
    for y in range(len(item_code)):
        if (item_code[y]) == int(backwards_num_item[x]):
            print("item name:", item_name[y])
            print("price: {} , {}, x: {}".format(item_prize[y], item_prize_type[y], backwards_amount_item[x]))
            total = total + float(backwards_amount_item[x]) * float(item_prize[y])

print("Your TOTAL is: {} TL".format(total))
