#!/usr/bin/env python3

# initialize django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'arcticapi.settings'
import django
django.setup()

# regular imports
from api.models import Category, Product
import json

# main script
def main():
    with open('products.json') as json_file:
        data = json.load(json_file)
    
    products = data['products']
    cats = []

    # Set up categories
    for prod in products:
        #dbcat = Category()
        if prod['category'] not in cats:
            cats.append(prod['category'])

    for cat in cats:
        dbcat = Category()
        dbcat.title = cat
        dbcat.save()

    for prod in products:
        #dbcat = Category()

        dbprod = Product()
        dbprod.name = prod['name']
        dbprod.description = prod['description']
        dbprod.price = prod['price']
        dbprod.filename = prod['filename']
        dbprod.category = Category.object.get(title=prod['category'])

        # for cat in Category.object.all():
        #     if cat.title == prod['category']:
        #         dbprod.category = cat
        dbprod.save()
    
    for cat in Category.object.all():
        print(cat.id, cat.title)
    for prod in Product.object.all():
        print(prod.id, prod.name, prod.category) 


# bootstrap
if __name__ == '__main__':
    main()
