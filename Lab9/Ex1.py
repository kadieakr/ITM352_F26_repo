# Calculating an extended price for a product (with tax)
product = {
    "name": 'small gumball', 
    "price":'$0.34'
}

tax_rate = 0.045

total = float(product["price"][1:]) + float(product["price"][1:]) * tax_rate

print(f"A {product['name']} costs ${total:.2f}")
