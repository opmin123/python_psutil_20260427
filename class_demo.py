"""
python 类demo 20264-24
"""

class Restaurant():
    def __init__(self,restaurant_name,cuisine_type):
        self.cuisine_type = cuisine_type
        self.restaurant_name = restaurant_name

    def describe_restaurant(self):
        print(self.restaurant_name + "clearn and delish!")
        print(self.restaurant_name + "really chiper!")


    def open_restaurant(self):
        print(self.restaurant_name + "have running!")



