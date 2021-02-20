from random import randint


def read_inventory() -> list:
    inventory_txt = open('inventory.txt', 'r')
    return inventory_txt.readlines()


def convert_inventory_to_list():
    products = []
    inventory = read_inventory()
    for i, line in enumerate(inventory):
        product = {}
        item_code, barcode_number, name, unit_price, unit_of_measurement, tax_rate = line.strip().split('?')

        tax_rate = int(tax_rate)
        unit_price = round(float(unit_price), 2)

        product['name'] = name
        product['barcode-number'] = barcode_number
        product['item-code'] = item_code
        product['tax-rate'] = tax_rate
        product['unit-price'] = unit_price
        product['unit-of-measurement'] = unit_of_measurement

        products.append(product)

    return products


def generate_hash(receipt: dict) -> str:
    inventory = convert_inventory_to_list()
    qr_hash = ''
    for product in inventory:
        barcode = product.get('barcode-number')

        if barcode in receipt.keys():
            item_code = str(product.get('item-code'))
            item_count = str(receipt.get(barcode))
            qr_hash += item_code + '?' + item_count + '%'

    return qr_hash


def generate_sample_receipt():
    inventory = convert_inventory_to_list()
    receipt = {}

    for product in inventory:
        if randint(0, 1) == 1:
            count = randint(1, 5)
            receipt[product.get('barcode-number')] = count

    return receipt


def convert_receipt_to_firebase(receipt: dict):
    inventory = convert_inventory_to_list()
    products = []

    for product in inventory:
        barcode = product.get('barcode-number')

        if barcode in receipt.keys():
            item = product
            item['count'] = int(receipt.get(barcode))
            products.append(item)

    return products


# def generate_receipt() -> (list, int):
#     inventory = convert_inventory_to_list()
#     total_price = 0
#     total_tax = 0
#
#     for product in inventory:
#         count = randint(1, 5)
#         product['count'] = count
#
#         price_sum = count * unit_price
#         total_tax += price_sum * (tax_rate / 100.0)
#         total_price += price_sum
#
#     return products, round(float(total_price), 2), round(float(total_tax), 2)

sample = generate_sample_receipt()
print(sample)
print(generate_hash(receipt=sample))
print(convert_receipt_to_firebase(receipt=sample))
