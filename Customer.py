#(c) 2020 Nathan Thimothe

class Customer(object):
    """
    Customer Class for Duke Beverages
    """
    __slots__ = ["_name","_year", "_phone",  "_email", "_deliveryDate", "_beverages", "_quantities", "_price"]

    def __init__(self, name, year, phone, email, deliveryDate, beverages, quantities, price):
        self._name = name
        self._year = year
        self._phone = phone
        self._email = email
        self._deliveryDate = deliveryDate
        self._beverages = beverages
        self._quantities = quantities
        self._price = price
    @property
    def name(self):
        return self._name
    @property
    def year(self):
        return self._year
    @property
    def phone(self):
        return self._phone
    @property
    def email(self):
        return self._email
    @property
    def deliveryDate(self):
        return self._deliveryDate
    @property
    def beverages(self):
        return self._beverages
    @property
    def quantities(self):
        return self._quantities
    @property
    def price(self):
        return self._price
    def __repr__(self):
        return ("Customer({},{},{},{},{},{},{},{})".format(self._name,self._year,self._phone,self._email,self._deliveryDate,self._beverages,self._quantities, self._price)) 
    def __str__(self):
            return("Name: {}\nPhone: {} \nEmail: {}\nDeliveryDate: {}\nBeverages: {}\nQuantity: {}\nPrice: {}\n".format(self._name,self._year,self._phone,self._email,self._deliveryDate,self._beverages,self._quantities, self._price))
