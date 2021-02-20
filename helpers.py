from random import randint


def read_inventory() -> list:
    """
    Read inventory from 'inventory.txt'

    :return: Lines of 'inventory.txt'
    """

    inventory_txt = open('inventory.txt', 'r')
    return inventory_txt.readlines()


def convert_inventory_to_list() -> list:
    """
    Convert inventory to list

    :return: List of dict of inventory items
    """

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
        product['unit-of-measurement'] = unit_of_measurement.upper()

        products.append(product)

    return products


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
        barcode = product.get('barcode-number')

        if barcode in receipt.keys():
            item = product

            count = int(receipt.get(barcode))
            unit_price = item.get('unit-price')
            tax_rate = item.get('tax-rate')

            item['count'] = count

            price_sum = count * unit_price
            total_tax += price_sum * (tax_rate / 100.0)
            total_price += price_sum

            products.append(item)

    total_price, total_tax = round(float(total_price), 2), round(float(total_tax), 2)

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
        barcode = product.get('barcode-number')

        if barcode in receipt.keys():
            item_code = str(product.get('item-code'))
            item_count = str(receipt.get(barcode))
            qr_hash += item_code + '?' + item_count + '%'

    return qr_hash


def generate_sample_receipt() -> dict:
    """
    Generate sample receipt dict

    :return: Receipt dict in form "{'barcode_number': 'count'}"
    """

    inventory = convert_inventory_to_list()
    receipt = {}

    for product in inventory:
        if randint(0, 1) == 1:
            count = randint(1, 5)
            receipt[product.get('barcode-number')] = count

    if not bool(receipt):
        generate_sample_receipt()
    else:
        return receipt
