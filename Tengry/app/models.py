from django.db import models
from django.contrib.auth.models import User

# Create your models here.
STATE_CHOICES = (
    ('Астана', 'Астана'),
    ('Алматы', 'Алматы'),
    ('Караганда', 'Караганда'),
    ('Шымкент', 'Шымкент'),
    ('Кокшетау', 'Кокшетау'),
    ('Актобе', 'Актобе'),
    ('Конаев', 'Конаев'),
    ('Атырау', 'Атырау'),
    ('Семей', 'Семей'),
    ('Усть-Каменогорск', 'Усть-Каменогорск'),
    ('Тараз', 'Тараз'),
    ('Талдыкорган', 'Талдыкорган'),
    ('Уральск', 'Уральск'),
    ('Костанай', 'Костанай'),
    ('Кызылорда', 'Кызылорда'),
    ('Актау', 'Актау'),
    ('Павлодар', 'Павлодар'),
    ('Петропавловск', 'Петропавловск'),
    ('Туркестан', 'Туркестан'),
    ('Жезказган', 'Жезказган'),
)

CATEGORY_CHOICES=(
    ('OP', 'Огнетушители ОП (Порошковые)'),
    ('OU', 'Огнетушители ОУ (углекислотные)'),
    ('OV', 'Воздушно-пенные огнетушители (ОВП)'),
    ('PSh', 'Пожарные шкафы, люки, рамы для шкафов'),
    ('ShP', 'Щиты пожарные, стенды'),
    ('RP', 'Рукава пожарные'),
    ('PT', 'Пожарно-техническое оснащение'),
    ('PA', 'Противопожарная арматура'),
    ('SIZ', 'Все виды СИЗ (средства индивидуальной защиты)'),
    ('PO', 'Перезарядка Огнетушителей ОП (порошковые)'),
    ('YP', 'Ящики для песка'),
    ('PK', 'Пожарное обмундирование и комплектующие'),
    ('KP', 'Клапаны пожарных кранов'),
    ('GP', 'Генераторы пены средней кратности'),
    ('MS', 'Монтаж системы противопожарной сигнализации')
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    diskounted_price = models.FloatField()
    discription = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=4)
    product_image = models.ImageField(upload_to='product')

    def __str__(self):
        return self.title

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price

STATUS_CHOICES = (
    ('Заказ принят', 'Заказ принят'),
    ('Заказ собирается', 'Заказ собирается'),
    ('В пути', 'В пути'),
    ('Доставлено', 'Доставлено'),
    ('Заказ отклонен', 'Заказ отклонен'),
    ('В ожидании', 'В ожидании'),
)
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="")
    @property
    def total_cost(self):
        if self.quantity >= 5:
            return self.quantity * self.product.discounted_price
        else:
            return self.quantity * self.product.selling_price

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)














