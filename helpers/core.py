import csv
import shutil
from random import randint, uniform
from tempfile import NamedTemporaryFile


def round_n_decimals(number: float, decimal: int):
    return round(float(number), decimal)


def read_csv(file: str):
    all_lines = []

    with open(f'data/csv/{file}.csv', 'r') as csv_file:
        lines = csv.DictReader(csv_file)
        for line in lines:
            all_lines.append(line)
    return all_lines


def convert_inventory_to_list() -> list:
    """
    Convert inventory to list

    :return: List of dict of inventory items
    """

    csv_reader = read_csv('inventory')
    products_list = []

    for line in csv_reader:
        temp = {}

        storage = round_n_decimals(float(line['storage']), 2)
        unit_price = round_n_decimals(float(line['unit-price']), 2)

        temp['barcode'] = int(line['barcode'])
        temp['item-code'] = int(line['item-code'])
        temp['name'] = line['name']
        temp['storage'] = storage
        temp['unit-of-measurement'] = line['unit-of-measurement'].upper()
        temp['unit-price'] = unit_price
        temp['tax-rate'] = int(line['tax-rate'])

        products_list.append(temp)

    return products_list


def convert_stores_to_list() -> list:
    """
    Convert inventory to list

    :return: List of dict of inventory items
    """

    csv_reader = read_csv('stores')
    products_list = []

    for line in csv_reader:
        temp = {}

        temp['address'] = line['address']
        temp['currency'] = line['currency']
        temp['id'] = line['id']
        temp['item-code'] = int(line['item-code'])
        temp['location'] = line['location']
        temp['location-id'] = line['location-id']
        temp['name'] = line['name']
        temp['slag'] = line['slag']

        products_list.append(temp)

    return products_list


def read_lines(file: str) -> list:
    """
    Read lines from 'file'.txt'

    :return:
    """
    return open(f'data/csv/{file}.txt', 'r').readlines()


def convert_receipt_to_firebase(receipt: dict) -> (list, int, int):
    """
    Add receipt data price and tax value. Then convert it to list.

    :param receipt: Receipt dictionary
    :return:
        products: Products list
        total_price: Total price of the receipt
        total_tax: Total tax of the receipt
    """

    inventory = convert_inventory_to_list()
    products = []
    total_price = 0
    total_tax = 0

    for product in inventory:
        barcode = product.get('barcode')

        if barcode in receipt.keys():
            item = product

            count = round_n_decimals(receipt.get(barcode), 2)
            unit_price = item.get('unit-price')
            tax_rate = item.get('tax-rate')

            item['count'] = count

            price_sum = count * unit_price
            total_tax += price_sum * (tax_rate / 100.0)
            total_price += price_sum

            products.append(item)

    total_price = round_n_decimals(number=total_price, decimal=2)
    total_tax = round_n_decimals(number=total_tax, decimal=2)

    return products, total_price, total_tax


def generate_hash(receipt: dict) -> str:
    """
    Generate hashed receipt from receipt dict.

    :param receipt: Receipt dictionary
    :return: qr_hash: Hashed receipt
    """

    inventory = convert_inventory_to_list()
    qr_hash = ''

    for product in inventory:
        barcode = product.get('barcode')

        if barcode in receipt.keys():
            item_code = str(product.get('item-code'))
            item_count = str(receipt.get(barcode))
            qr_hash += item_code + '?' + item_count + '%'

    return qr_hash


def generate_sample_receipt() -> dict:
    """
    Generate sample receipt dict

    :return: Receipt dict in form "{'barcode': 'count'}"
    """

    inventory = convert_inventory_to_list()
    receipt = {}
    count = 0

    for product in inventory:
        storage = product.get('storage')
        barcode = product.get('barcode')

        if randint(0, 1) == 1:
            if product.get('unit-of-measurement') == 'KG':
                count = round_n_decimals(uniform(1, storage // 2), 2)
            else:
                count = randint(1, storage // 2)

            receipt[product.get('barcode')] = count
            update_csv(barcode=barcode, count=count)

    if not bool(receipt):
        generate_sample_receipt()
    else:
        return receipt


def update_csv(barcode: int, count: float):
    products_list = convert_inventory_to_list()

    temp_file = NamedTemporaryFile(mode='w', delete=False)

    # Read inventory
    with open('data/csv/inventory.csv', 'r', newline='') as csv_read, temp_file:

        # Reading fieldnames
        csv_reader = csv.DictReader(csv_read)
        dict_from_csv = dict(list(csv_reader)[0])
        fieldnames = list(dict_from_csv.keys())

        # Writing temporary file
        writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
        writer.writeheader()
        # Decreasing the storage of the given barcode
        for product in products_list:
            if product['barcode'] == barcode:
                if count < product['storage']:
                    product['storage'] -= round_n_decimals(float(count), 2)

            writer.writerow(product)

    shutil.copy2(temp_file.name, 'data/csv/inventory.csv')
