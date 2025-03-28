class Chocolate:
    def __init__(self, price: float, additive: str = None, has_nuts: bool = False, nut_count: int = 0):
        if price <= 0:
            raise ValueError("Цена батончика должна быть больше нуля.")
        
        self.price = price
        self.additive = additive
        self.has_nuts = has_nuts
        self.nut_count = nut_count

    def show_my_chocolate(self):
        if self.additive:
            print(f"Шоколадный батончик, добавка: {self.additive}")
        else:
            print("Обычный шоколадный батончик")

    def count_nuts(self):
        print('*' * self.nut_count)

    def __str__(self):
        return f"Шоколадный батончик, {self.price} рублей"

# Создаем несколько объектов Chocolate
choco1 = Chocolate(50.0, "орехи", True, 5)
choco2 = Chocolate(30.0)
choco3 = Chocolate(20.0, "молоко", False, 0)

# Демонстрируем функционал
print(choco1)
choco1.show_my_chocolate()
choco1.count_nuts()

print(choco2)
choco2.show_my_chocolate()
choco2.count_nuts()

print(choco3)
choco3.show_my_chocolate()
choco3.count_nuts()
