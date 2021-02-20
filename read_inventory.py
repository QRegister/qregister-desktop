from random import randint


def generate_receipt() -> (list, int):
    inventory_txt = open('inventory.txt', 'r')
    inventory = inventory_txt.readlines()

    products = []
    total_price = 0
    for i, line in enumerate(inventory):
        product = {}
        number, name, unit_price, unit_of_measurement = line.strip().split('?')

        unit_price = round(float(unit_price), 2)

        count = randint(1, 5)

        product['name'] = name
        product['count'] = count
        product['unit-price'] = unit_price
        product['unit-of-measurement'] = unit_of_measurement
        products.append(product)

        total_price += count * unit_price

    return products, round(float(total_price), 2)
