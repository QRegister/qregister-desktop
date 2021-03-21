import csv
import random
from tempfile import NamedTemporaryFile
import shutil


def new_count(barcode, count, product_list):
    temp_file = NamedTemporaryFile(mode='w', delete=False)
    with open('../inventory mark1.csv', 'r', newline='') as csv_file, temp_file:

        csv_reader = csv.DictReader(csv_file)
        dict_from_csv = dict(list(csv_reader)[0])
        fields = list(dict_from_csv.keys())

        writer = csv.DictWriter(temp_file, fieldnames=fields)
        writer.writeheader()
        for product in product_list:
            if product['barcode'] == barcode:
                if count < product['storage']:
                    product['storage'] -= count
                    print(f"{product['name']} {product['storage']}")

                else:
                    print('not in stock')
            else:
                print('not this item')

            writer.writerow(product)

    shutil.copy2(temp_file.name, '../inventory mark1.csv')


with open('../inventory mark1.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # created an ordered dictionary for all data
    product_list = []
    for line in csv_reader:
        temp = {'storage': int(line['storage']), 'item_code': int(line['item_code']), 'barcode': int(line['barcode']),
                'name': line['name'], 'unit_price': float(line['unit_price']),
                'unit_of_measurement': line['unit_of_measurement'], 'tax_rate': int(line['tax_rate'])}

        product_list.append(temp)

    fields = ['storage', 'item_code', 'barcode', 'name', 'unit_price', 'unit_of_measurement', 'tax_rate']

    random_barcode = random.randint(1001, 1006)
    count = random.randint(1, 10)
    print(count)
    new_count(random_barcode, count, product_list, fields)
