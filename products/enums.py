from enum import Enum


class BaseProperty(Enum):
    @classmethod
    def get_choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def get_subclasses(cls):
        no_tuple = (('No', 'Нет'),)
        enums_tuple = tuple((sub.__name__, sub.__name__) for sub in cls.__subclasses__() if sub != cls)
        return no_tuple + enums_tuple


class Color(BaseProperty):
    Black = 'Черный'
    White = 'Белый'
    Gray = 'Серый'
    Red = 'Красный'
    Blue = 'Синий'
    Green = 'Зеленый'
    Yellow = 'Желтый'
    Pink = 'Розовый'
    Purple = 'Фиолетовый'
    Light_Blue = 'Голубой'


class ClothingSize(BaseProperty):
    XXS = 'XXS'
    XS = 'XS'
    S = 'S'
    M = 'M'
    L = 'L'
    XL = 'XL'
    XXL = 'XXL'
    XXXL = '3XL'


class ShoeSize(BaseProperty):
    SIZE_38 = '38'
    SIZE_39 = '39'
    SIZE_40 = '40'
    SIZE_41 = '41'
    SIZE_42 = '42'
    SIZE_43 = '43'
    SIZE_44 = '44'
    SIZE_45 = '45'
    SIZE_46 = '46'
    SIZE_47 = '47'
    SIZE_48 = '48'
    SIZE_49 = '49'
    SIZE_50 = '50'


class Sex(BaseProperty):
    Male = 'Мужской'
    Female = 'Женский'
    Unisex = 'Унисекс'


class Material(BaseProperty):
    Cotton = 'Хлопок'
    Polyester = 'Полиэстер'
    Nylon = 'Нейлон'
    Leather = 'Кожа'
    Rubber = 'Резина'
    Plastic = 'Пластик'
    Metal = 'Металл'
    PVC = 'Поливинилхлорид'
    PU = 'Полиуретан'
