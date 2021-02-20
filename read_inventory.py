from random import randint


def generate_receipt() -> (list, int):
    inventory_txt = open('inventory.txt', 'r')
    inventory = inventory_txt.readlines()

    products = []
    total_price = 0
    total_tax = 0
    for i, line in enumerate(inventory):
        product = {}
        number, name, unit_price, unit_of_measurement, tax_rate = line.strip().split('?')

        tax_rate = int(tax_rate)
        unit_price = round(float(unit_price), 2)

        count = randint(1, 5)

        product['name'] = name
        product['count'] = count
        product['tax-rate'] = tax_rate
        product['unit-price'] = unit_price
        product['unit-of-measurement'] = unit_of_measurement
        products.append(product)

        price_sum = count * unit_price
        total_tax += price_sum * (tax_rate / 100.0)
        total_price += price_sum

    return products, round(float(total_price), 2), round(float(total_tax), 2)
