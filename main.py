import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import time

columns = ['Магазин', 'Координаты', 'Дата и время', 'Товар', 'Производитель', 
           'Номер карты', 'Количество', 'Цена', 
            ]

item_dict = { # 18 unique categories
    'платье': 'одежда',
    'куртка': 'одежда',
    'свитер': 'одежда',
    'пальто': 'одежда',
    'костюм': 'одежда',
    'толстовка': 'одежда',
    'футболка': 'одежда',
    'кеды': 'обувь',
    'шапка': 'одежда',
    'спортивные брюки': 'одежда',
    'кроссовки': 'обувь',
    'ботинки': 'обувь',
    'рубашка': 'одежда',
    'джинсы': 'одежда',
    'шорты': 'одежда',
    'юбка': 'одежда',
    'галстук': 'одежда',
    'поло': 'одежда',
    'джемпер': 'одежда',
    'пюре': 'еда готовая',
    'сок': 'напиток',
    'йогурт': 'молочный продукт',
    'кефир': 'молочный продукт',
    'молоко': 'молочный продукт',
    'творог': 'молочный продукт',
    'масло': 'молочный продукт',
    'мясо': 'мясные продукты',
    'курица': 'мясные продукты',
    'индейка': 'мясные продукты',
    'специи': 'приправы',
    'кетчуп': 'соус',
    'майонез': 'соус',
    'шоколад': 'сладости',
    'конфеты': 'сладости',
    'суп': 'еда готовая',
    'консервы': 'еда готовая',
    'чипсы': 'снэки',
    'батончики': 'снэки',
    'овсянка': 'завтрак',
    'колонки': 'аудиотехника',
    'наушники': 'аудиотехника',
    'наушники беспроводные': 'аудиотехника',
    'усилитель': 'аудиотехника',
    'телевизор': 'бытовая техника',
    'ноутбук': 'компьютерная техника',
    'планшет': 'компьютерная техника',
    'смартфон': 'компьютерная техника',
    'пылесос': 'бытовая техника',
    'микроволновка': 'бытовая техника',
    'камера': 'фото и видео техника',
    'проигрыватель': 'аудиотехника',
    'рюкзак': 'одежда',
    'ремень': 'одежда',
    'супы': 'еда готовая',
    'сметана': 'молочный продукт',
    'крекеры': 'снэки',
    'творог обезжиренный': 'молочный продукт',
    'напитки': 'напиток',
    'соус': 'соус',
    'холодильник': 'бытовая техника',
    'хлопья': 'завтрак',
    'фотоаппарат': 'фото и видео техника',
    'умные часы': 'часовая техника',
    'часы': 'часовая техника',
    'мышь': 'компьютерная техника',
    'монитор': 'компьютерная техника',
    'фитнес-трекер': 'фитнес техника',
    'мюсли': 'завтрак',
    'бекон': 'мясные продукты',
    'колбаса': 'мясные продукты',
    'крупы': 'еда готовая',
    'газированные напитки': 'напиток',
    'гарнитура': 'аудиотехника',
    'снеки': 'снэки',
    'саундбар': 'аудиотехника',
    'вода': 'напиток',
    'кепка': 'одежда',
    'процессор': 'компьютерная техника',
    'консервированные овощи': 'еда готовая',
    'десерты': 'сладости',
    'проектор': 'аудиовизуальная техника',
    'молоко 1.5%': 'молочный продукт',
    'туфли': 'обувь',
    'видеокарта': 'компьютерная техника',
    'соки': 'напиток',
    'приправы': 'приправы',
    'компьютер': 'компьютерная техника',
    'носки': 'одежда',
    'сыр': 'молочный продукт',
    'колбасы': 'мясные продукты',
    'утюг': 'бытовая техника',
    'сосиски': 'мясные продукты',
    'плеер': 'аудиотехника',
    'роутер': 'компьютерная техника',
    'брюки': 'одежда',
    'молоко 3.2%': 'молочный продукт',
    'адаптер': 'компьютерная техника',
    'модем': 'компьютерная техника',
    'объектив': 'фото и видео техника',
    'клавиатура': 'компьютерная техника',
    'ряженка': 'молочный продукт',
    'лампа': 'бытовая техника',
    'зарядное устройство': 'компьютерная техника',
    'лапша': 'еда готовая',
    'квас': 'напиток',
    'пуховик': 'одежда',
    'материнская плата': 'компьютерная техника',
    'горчица': 'соус',
    'соусы': 'соус',
    'макароны': 'еда готовая',
    'спортивная куртка': 'одежда',
    'датчик сердечного ритма': 'фитнес техника',
    'пиво': 'напиток',
    'вермишель': 'еда готовая',
    'бейсболка': 'одежда',
    'стиральная машина': 'бытовая техника',
    'мясные продукты': 'мясные продукты',
    'штатив': 'фото и видео техника'
}


def read_csv(file_name, delimiter=';') -> pd.DataFrame: 
    df_csv = pd.read_csv(file_name, sep=delimiter)
    return df_csv


def calculate_k_anonymity(df, quasi_identifiers, all='no'):
    if all == 'yes':
        quasi_identifiers = df.columns
    
    # Группируем по квазиидентификаторам и считаем количество строк в каждой группе
    grouped = df.groupby(quasi_identifiers).size().reset_index(name='k-anonymity')
    
    # df_with_k теперь содержит только уникальные строки с k-анонимностью
    df_with_k = grouped.copy()

    
    # Сортируем по 'k-anonymity', чтобы найти строки с наибольшей и наименьшей k-анонимностью
    worst_k_anonymity = df_with_k.sort_values('k-anonymity').head(3)
    best_k_anonymity = df_with_k.sort_values('k-anonymity', ascending=False).head(3)
    
    # Подсчитываем количество строк с k-анонимностью меньше 5
    count_k_less_than_5 = (df_with_k['k-anonymity'] < 7).sum()
    print(f"\nКоличество строк с k-анонимностью меньше 7: {count_k_less_than_5}")

    return worst_k_anonymity, best_k_anonymity

def item_mask(df, col):
    out = []
    for item,general_category in df[[col,'Магазин']].values:
        if item in item_dict:
            out.append(item_dict[item])
        else:
            out.append(general_category)
    df[col] = out
    return df

def card_mask(df, col):
    df[col] = df[col].apply(lambda card: str(card)[:4] + "X" * 12)
    return df

def coordinates_mask(df, col):
    # df[col] = df[col].apply(lambda coordinates: ', '.join([coord[:-3] for coord in coordinates.split(', ')]))
    output = []
    for coordinates in df[col]:
        X, Y = coordinates.split(', ')
        X,Y = X[:-3], Y[:-3]
        if(len(X) < 6):
            X += '0'
        if(len(Y) < 6):
            Y += '0'
        output.append(str(X) + ', ' + str(Y))
    df[col] = output
    return df

def date_mask(df, col):
    mask = []
    for data in df[col]:
        date = data[:8] + "XXTXX" + ":" + "XX"
        mask.append(date) 
    df[col] = mask
    return df

def get_shop_category(df, shop_name):
    # Находим строку, где название магазина совпадает с переданным
    category = df.loc[df['shop_name'] == shop_name, 'category_type']

    if not category.empty:
        return category.values[0]  # Возвращаем первый найденный тип продукта
    else:
        return 'None'
    
def shop_mask(df,col):
    df_shops = pd.read_csv('input_data/shop_locations.csv', sep=';',names=['category_type','shop_name', 'coordinates'])
    out = []
    for shop_name in df[col]:
        out.append(get_shop_category(df_shops,shop_name))
    df[col] = out
    return df

def amount_mask(df,col):
    out = []
    for amount in df[col]:
        if(amount == 1):
            out.append('one')
        elif(amount <= 4):
            out.append('some')
        else:
            out.append('a lot')
    df[col] = out
    return df

def price_mask(df,col):
    out = []
    for price,amount in df[[col,'Количество']].values:
        price /= amount
        if price < 100:
            out.append('< 100')
        elif price < 500:
            out.append('< 500')
        elif price < 1500:
            out.append('< 1500')
        elif price < 5000:
            out.append('< 5000')
        elif price < 10000:
            out.append('< 10000')
        elif price >= 10000:
            out.append('>= 10000')
    df[col] = out
    return df

def calculate_k_anonymity_2(df, columns, k):
    group_counts = df.groupby(columns).size().reset_index(name='count')
    return all(group_counts['count'] >= k)
    
if __name__ == '__main__':
    # TODO : shop_name, item_name, brand_name, amount, price
    df = read_csv(file_name='input_data/all_types_10k.csv',delimiter=';')

    
    coordinates_mask(df,'Координаты')
    date_mask(df,'Дата и время')
    shop_mask(df,'Магазин')
    card_mask(df,'Номер карты')
    price_mask(df,'Цена')
    amount_mask(df,'Количество') # always after price_mask
    item_mask(df,'Товар')
    quasi_identifiers = ['Магазин','Дата и время','Координаты','Номер карты','Количество', 'Цена','Товар'] # 
    worst_k, best_k = calculate_k_anonymity(df, quasi_identifiers,all='no')
    
    
    
    print("Топ-3 худших строк по k-анонимности:")
    print(worst_k)

    print("\n Топ-3 лучших строк по k-анонимности:")
    print(best_k,'\n\n')
    print(df.head())

    """
    root = tk.Tk()
    root.title("Обезличиватель датасета")
    root.geometry("500x600")

    greeting_label = tk.Label(root, text="Добро пожаловать! Выберите квази-идентификаторы:", font=("Arial", 14))
    greeting_label.pack(pady=20)
    #load_button = tk.Button(root, text="Загрузить файл", command=load_file, font=("Arial", 12), bg="lightblue")
    #load_button.pack(pady=10)
    file_label = tk.Label(root, text="", font=("Arial", 12))
    file_label.pack(pady=10)

    attribute_vars = {}

    for attribute in columns:
        var = tk.IntVar(value=0)
        attribute_vars[attribute] = var
        checkbox = tk.Checkbutton(root, text=attribute, variable=var, font=("Arial", 12))
        checkbox.pack(anchor=tk.W)

    #process_button = tk.Button(root, text="Обезличить и вычислить", command=handle_attributes, font=("Arial", 12), bg="green", fg="white")
    #process_button.pack(pady=20)
    #load_button2 = tk.Button(root, text="Вычислить k-anonymity", command=k_anon, font=("Arial", 12), bg="green", fg="white")
    #load_button2.pack(pady=25)

    root.mainloop()
    """