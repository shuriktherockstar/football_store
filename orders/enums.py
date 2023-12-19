from products.enums import BaseProperty


class OrderStatus(BaseProperty):
    accepted = 'Принят'
    processing = 'В обработке'
    shipping = 'Отправлен'
    delivered = 'Доставлен'
