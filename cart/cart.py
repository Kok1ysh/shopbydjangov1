from decimal import Decimal

from django.conf import settings

from shop.models import Product


class Cart(object):
    def __init__(self, request):
        "initial object cart"
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __str__(self):
        return str(self.cart)

    def add(self, product, count_product=1, update_count_product=False):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'count_product': 0, 'price': str(product.price)}
        if update_count_product:
            self.cart[product_id]['count_product'] = count_product
        else:
            self.cart[product_id]['count_product'] += count_product
        self.save()

    # card="{'1':{'count_product':'1','price':'123000'},'2':{'count_product':'3','price':'123000'}}"

    def save(self):
        # Визначаємо сесію, як така, що була змінена
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        print(products)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            print(item['price'])

            item['price'] = Decimal(item['price'])
            # print(item['price'].replace('.',','))
            item['result_price'] = item['price'] * item['count_product']
            print(item['result_price'])
            yield item

    def __len__(self):
        # Повертаємо загальну кількість товарів в корзині
        count_product = [item['count_product'] for item in self.cart.values()]
        return sum(count_product)

    def get_total_price(self):
        # Підраховуємо суму вартості всіх товарів
        list_price_all_product = []
        for item in self.cart.values():
            list_price_all_product.append(Decimal(item['price']) * item['count_product'])
        return sum(list_price_all_product)

    def clear(self):
        # Очищаємо корзину
        del self.session[settings.CART_SESSION_ID]
        self.save()