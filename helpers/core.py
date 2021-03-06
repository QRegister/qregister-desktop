import csv
from random import randint, uniform


def round_n_decimals(number: float, decimal: int):
    return round(float(number), decimal)


def read_csv(file: str):
    product_list = []

    with open(f'data/csv/{file}.csv', 'r') as csv_file:
        return csv.DictReader(csv_file)


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
        unit_price = round_n_decimals(float(line['unit_price']), 2)

        temp['barcode'] = int(line['barcode'])
        temp['item-code'] = int(line['item_code'])
        temp['name'] = line['name']
        temp['storage'] = storage
        temp['unit-of-measurement'] = line['unit_of_measurement'].upper()
        temp['unit-price'] = unit_price
        temp['tax-rate'] = int(line['tax_rate'])

        products_list.append(temp)

    return products_list


def convert_inventory_to_stores() -> list:
    """
    Convert inventory to list

    :return: List of dict of inventory items
    """

    csv_reader = read_csv('stores')
    products_list = []

    for line in csv_reader:
        temp = {}

        temp['address'] = line['address']
        temp['curreny'] = line['currency']
        temp['id'] = line['id']
        temp['item-code'] = int(line['item_code'])
        temp['location'] = line['location']
        temp['location-id'] = line['location_id']
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


# def convert_inventory_to_list() -> list:
#     """
#     Convert inventory to list
#
#     :return: List of dict of inventory items
#     """
#
#     products = []
#     inventory = read_lines('inventory')
#     for line in inventory:
#         product = {}
#         item_code, barcode, name, unit_price, unit_of_measurement, tax_rate = line.strip().split('?')
#
#         tax_rate = int(tax_rate)
#         unit_price = round(float(unit_price), 2)
#
#         product['name'] = name
#         product['barcode'] = barcode
#         product['item-code'] = item_code
#         product['tax-rate'] = tax_rate
#         product['unit-price'] = unit_price
#         product['unit-of-measurement'] = unit_of_measurement.upper()
#
#         products.append(product)
#
#     return products


# def convert_stores_to_list() -> list:
#     """
#     Convert stores to list
#
#     :return: List of dict of store items
#     """
#
#     store_list = []
#     stores = read_lines('stores')
#
#     for line in stores:
#         store = {}
#         item_code, slag, name, location, address, id, location_id = line.strip().split('?')
#
#         store['address'] = address
#         store['id'] = id
#         store['item-code'] = item_code
#         store['location'] = location
#         store['location-id'] = location_id
#         store['name'] = name
#         store['slag'] = slag
#
#         store_list.append(store)
#
#     return store_list


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

    for product in inventory:
        if randint(0, 1) == 1:
            if product.get('unit-of-measurement') == 'KG':
                count = uniform(1, 5)
            else:
                count = randint(1, 5)
            receipt[product.get('barcode')] = count

    if not bool(receipt):
        generate_sample_receipt()
    else:
        return receipt
