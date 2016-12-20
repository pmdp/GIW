# -*- coding: utf-8 -*-

# Sixto Jansa Sanz,
# Jorge Utrilla Olivera,
# y Jose Miguel Maldonado Del Pozo
# declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal.
# No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie.
# Declaramos además que no hemos realizado de manera deshonesta ninguna otra actividad
# que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

from mongoengine import *

db = connect('giw_mongoengine')


class CreditCard(EmbeddedDocument):
    name = StringField(required=True, min_length=3, max_length=40)
    number = StringField(required=True, regex="^(\d{16})$")
    month = StringField(required=True, regex="^(0[1-9]|1[0-2])$")
    year = StringField(required=True, regex='^\d{2}$')
    cvv = StringField(required=True, regex='^\d{3}$')


class Item (Document):
    barcode = StringField(required=True, unique=True, regex="^\d{13}$")
    name = StringField(required=True, min_length=3, max_length=30)
    category = IntField(required=True, min_value=0)
    categories_list = ListField(IntField(min_value=0))

    def clean(self):
        reverse = self.barcode[::-1]
        control_digit = int(self.barcode[-1])
        reverse = reverse[1:]
        #print("Reverse sin control: ", reverse)
        #print("Digito de control: ", control_digit)
        sum = 0
        for i, digit in enumerate(reverse):
            if (i+1) % 2 == 0:
                sum += int(digit)
            else:
                sum += int(digit) * 3
        digit = (10 - (sum % 10)) % 10
        #print(u"El digito de control debería ser: ", digit)
        if control_digit != digit:
            raise ValidationError(u"El dígito de control EAN-13 no es válido")
        #Si tiene categorías secundarias comprobar que la principal está en la primera posición
        if self.categories_list and (self.categories_list[0] != self.category):
            raise ValidationError(u"La categoría principal no está en la primera posición de las secundarias")


class OrderLines(EmbeddedDocument):
    quantity = IntField(required=True)
    price = FloatField(required=True, min_value=0.0)
    name = StringField(required=True, min_length=3, max_length=30)
    total_price = FloatField(required=True, min_value=0.0)
    item = ReferenceField(Item, required=True)

    def clean(self):
        if (float(self.quantity) * float(self.price)) != float(self.total_price):
            raise ValidationError(u"El precio total de la línea no corresponde con el precio y el número de productos")
        if self.name != self.item.name:
            raise ValidationError(u"El nombre de la línea de prodcuto no corresponde con el nombre del producto referenciado")

class Order(Document):
    total_price = FloatField(required=True, min_value=0.0)
    order_date = ComplexDateTimeField(required=True)
    order_lines = EmbeddedDocumentListField(OrderLines, required=True)

    def clean(self):
        sum = 0.0
        for ol in list(self.order_lines):
            sum += float(ol.total_price)
        if float(self.total_price) != sum:
            raise ValidationError(u"El precio total del pedido no corresponde a la suma de todas sus líneas")


class User(Document):
    dni = StringField(required=True, unique=True, regex="^(([X-Z]{1})(\d{7})([A-Z]{1}))|((\d{8})([A-Z]{1}))$")
    name = StringField(required=True, min_length=3, max_length=30)
    surname = StringField(required=True, min_length=3, max_length=30)
    second_surname = StringField(min_length=3, max_length=30)
    birthdate = StringField(required=True, regex='^([0-9]{4})([-])([0-9]{2})([-])([0-9]{2})$')
    last_access = ListField(ComplexDateTimeField)
    credit_cards = EmbeddedDocumentListField(CreditCard)
    orders = ListField(ReferenceField(Order, reverse_delete_rule=PULL))

    def clean(self):
        #Letras en orden según el resto de la división de los números del DNI por 23
        letters = "TRWAGMYFPDXBNJZSQVHLCKE"
        #Si el dni es NIE de extranjeros (empieza por letra)
        if self.dni[0].isalpha():
            if self.dni[0] == 'X':
                v = '0'
            elif self.dni[0] == 'Y':
                v = '1'
            elif self.dni[0] == 'Z':
                v = '2'
            if self.dni[1:8].isdigit() and (letters[int(v + self.dni[1:8]) % 23] != self.dni[8]):
                raise ValidationError(u"La letra del NIE no es válida")
        #Si es NIF
        else:
            #Coge los 8 primeros digitos del DNI
            if self.dni[:8].isdigit() and (letters[int(self.dni[:8]) % 23] != self.dni[8]):
                raise ValidationError(u"La letra del NIF no es válida")



def insertar():
    #Prodcutos, Líneas de pedido y Pedidos

    i1 = Item(barcode="1234567890418", name="pan", category=2, categories_list=[2, 4, 5])
    i2 = Item(barcode="7684846473780", name="cebolla", category=2)
    i3 = Item(barcode="7456573483840", name="oreo", category=3)
    i4 = Item(barcode="6667753988647", name="helado", category=4)
    i1.save()
    i2.save()
    i3.save()
    i4.save()

    ol1 = OrderLines(quantity=2, price=0.55, name="pan", total_price=1.1, item=i1)
    ol2 = OrderLines(quantity=3, price=0.32, name="cebolla", total_price=0.96, item=i2)
    ol3 = OrderLines(quantity=1, price=2.0, name="oreo", total_price=2.0, item=i3)
    ol4 = OrderLines(quantity=7, price=3.0, name="helado", total_price=21.0, item=i4)

    o1 = Order(total_price=2.06, order_date="2016,12,15,12,34,21,888283", order_lines=[ol1, ol2])
    o2 = Order(total_price=23, order_date="2016,12,20,12,34,21,888283", order_lines=[ol3, ol4])
    o3 = Order(total_price=24.1, order_date="2016,12,20,12,34,21,888283", order_lines=[ol1, ol3, ol4])
    o4 = Order(total_price=21.96, order_date="2016,12,20,12,34,21,888283", order_lines=[ol4, ol2])
    o1.save()
    o2.save()
    o3.save()
    o4.save()


    #Tarjetas de credito y Usuarios
    c1 = CreditCard(name='Pedro', number='1234567891234567', month='02', year='20', cvv='455')
    c2 = CreditCard(name='María', number='7684874647484837', month='11', year='17', cvv='345')
    c3 = CreditCard(name='Irving', number='0383537847236284', month='12', year='22', cvv='566')

    p = User(dni='08264947N', name='Pedro', surname='Hernandez', birthdate='1993-06-20',
             credit_cards=[c1, c2], orders=[o1, o2])
    p1 = User(dni='Z7334448Y', name='Irving', surname='Mendez', birthdate='1993-06-20',
              credit_cards=[c3], orders=[o3, o4])
    p.save()
    p1.save()

    #Comprobación de eliminado de un pedido de la lista de un usuario al borrar dicho pedido
    print(u"Borrando pedido o1")
    nP = len(User.objects.get(name="Pedro").orders)
    print(u"Número de pedidos de Pedro antes de borrar:", nP)
    o1.delete()
    nP2 = len(User.objects.get(name="Pedro").orders)
    print(u"Número de pedidos de Pedro después de borrar:", nP2)

if __name__ == "__main__":
    db.drop_database('giw_mongoengine')
    insertar()