import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import time

columns = ['Магазин', 'Координаты', 'Дата и время', 'Товар', 'Производитель', 
           'Номер карты', 'Количество', 'Цена', 
            ]
bad_locations = set(['Технополис Политехнический' ,'Красные Зори' ,'Технопарк Мебельная' ,'Глобус Джус' ,'Туристическое агентство Глобус' ,'Технопарк Рот Фронт' ,'Приневский технопарк' ,'СберМаркет' ,'Издательство Утконос' ,'Технопарк Боровая' ,'Технопарк Арсенал' ,'Азбука Вкуса' ,'Звезда' ,'Павловский коммунальный технопарк' ,'Промышленный Парк на Дерибасовской' ,'Hiker' ,'Промышленный Парк' ,'Ленполиграфмаш' ,'Машиностроительный технопарк Гагарин' ,'Технопарк Санкт-Петербурга' ,'Индустриальный парк Greenstate' ,'Технопарк Мариенбург' ,'Технопарк Новикова' ,'Рандеву' ,'Технопарк' ,'re:Store' ,'PiterGSM' ,'Street Beat Kids' ,'Технопарк Нарвский'])

item_dict = { # 11 unique categories
    'платье': 'одежда',
    'куртка': 'одежда',
    'свитер': 'одежда',
    'пальто': 'одежда',
    'костюм': 'одежда',
    'толстовка': 'одежда',
    'футболка': 'одежда',
    'кеды': 'одежда',
    'шапка': 'одежда',
    'спортивные брюки': 'одежда',
    'кроссовки': 'одежда',
    'ботинки': 'одежда',
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
    'специи': 'соус',
    'кетчуп': 'соус',
    'майонез': 'соус',
    'шоколад': 'еда готовая',
    'конфеты': 'еда готовая',
    'суп': 'еда готовая',
    'консервы': 'еда готовая',
    'чипсы': 'еда готовая',
    'батончики': 'еда готовая',
    'овсянка': 'еда готовая',
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
    'крекеры': 'еда готовая',
    'творог обезжиренный': 'молочный продукт',
    'напитки': 'еда готовая',
    'соус': 'соус',
    'холодильник': 'бытовая техника',
    'хлопья': 'еда готовая',
    'фотоаппарат': 'фото и видео техника',
    'умные часы': 'фото и видео техника',
    'часы': 'фото и видео техника',
    'мышь': 'компьютерная техника',
    'монитор': 'компьютерная техника',
    'фитнес-трекер': 'фото и видео техника',
    'мюсли': 'еда готовая',
    'бекон': 'мясные продукты',
    'колбаса': 'мясные продукты',
    'крупы': 'еда готовая',
    'газированные напитки': 'напиток',
    'гарнитура': 'аудиотехника',
    'снеки': 'еда готовая',
    'саундбар': 'аудиотехника',
    'вода': 'напиток',
    'кепка': 'одежда',
    'процессор': 'компьютерная техника',
    'консервированные овощи': 'еда готовая',
    'десерты': 'еда готовая',
    'проектор': 'компьютерная техника',
    'молоко 1.5%': 'молочный продукт',
    'туфли': 'одежда',
    'видеокарта': 'компьютерная техника',
    'соки': 'напиток',
    'приправы': 'соус',
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
    'датчик сердечного ритма': 'фото и видео техника',
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
    
    # df_with_k теперь содержит уникальные строки с добавленным столбцом 'k-anonymity'
    df_with_k = grouped.copy()

    # Сортировка по столбцу 'k-anonymity'
    df_with_k_sorted = df_with_k.sort_values(by='k-anonymity')
    
    # Удаление нижних 5% строк
    percent_to_remove = 0.05
    n_rows_to_remove = int(len(df_with_k_sorted) * percent_to_remove)
    df_with_k_trimmed = df_with_k_sorted.iloc[n_rows_to_remove:]
    
    # Сортируем по 'k-anonymity', чтобы найти строки с наибольшей и наименьшей k-анонимностью
    worst_k_anonymity = df_with_k_trimmed.sort_values('k-anonymity').head(3)
    best_k_anonymity = df_with_k_trimmed.sort_values('k-anonymity', ascending=False).head(3)
    
    # Подсчитываем количество строк с k-анонимностью меньше 7
    count_k_less_than_7 = (df_with_k_trimmed['k-anonymity'] < 7).sum()
    print(f"\nКоличество строк с k-анонимностью меньше 7: {count_k_less_than_7}")

    return worst_k_anonymity, best_k_anonymity


def item_mask(df, col):
    out = []
    for item,general_category in df[[col,'Магазин']].values:
        if item in item_dict:
            out.append(item_dict[item])
        else:
            print(item)
            out.append(general_category)
    df[col] = out
    return df

def brand_mask(df, col):
    out = []
    for brand,general_category in df[[col,'Магазин']].values:
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
        X,Y = X[:-4], Y[:-4]
        if(len(X) < 5):
            X += '0'
        if(len(Y) < 5):
            Y += '0'
        if(len(X) < 5):
            X += '0'
        if(len(Y) < 5):
            Y += '0'
        output.append(str(X) + ', ' + str(Y))
    df[col] = output
    return df

def coordinates_mask_alternative(df, col):
    output = []
    for coordinates,shop_name in df[[col,'Магазин']].values:
        if shop_name in bad_locations:
            output.append('- , -')
        elif shop_name in location_stores:
            output.append(location_stores[shop_name])
        else:
            output.append('0.00 , 0.00')
            
    df[col] = output
    return df

def date_mask(df, col):
    mask = []
    for data in df[col]:
        date = data[:5] + "XXXXTXX" + ":" + "XX"
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
        if(amount <= 4):
            out.append('some')
        else:
            out.append('a lot')
    df[col] = out
    return df

def price_mask(df,col):
    out = []
    for price,amount in df[[col,'Количество']].values:
        price /= amount
        if price < 500:
            out.append('< 1000')
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

def get_store_coordinates(csv_file):
    # Чтение CSV файла с использованием ';' в качестве разделителя
    df = pd.read_csv(csv_file, delimiter=';', header=None, names=['category', 'store', 'coordinates'])
    
    # Создание словаря для хранения результата
    store_coordinates = {}
    
    # Проходим по уникальным названиям магазинов
    for store in df['store'].unique():
        # Получаем любые координаты для текущего магазина
        coords = df[df['store'] == store]['coordinates'].iloc[0]
        # Добавляем в словарь
        store_coordinates[store] = coords

    return store_coordinates
# Пример использования

    
if __name__ == '__main__':
    # TODO : shop_name, item_name, brand_name, amount, price
    df = read_csv(file_name='input_data/all_types_100k.csv',delimiter=';')

    location_stores = get_store_coordinates('input_data/shop_locations.csv')
    coordinates_mask_alternative(df,'Координаты')
    date_mask(df,'Дата и время')
    shop_mask(df,'Магазин')
    card_mask(df,'Номер карты')
    price_mask(df,'Цена')
    amount_mask(df,'Количество') # always after price_mask
    item_mask(df,'Товар')
    brand_mask(df,'Производитель')
    
    # Удаление нижних 5% строк

    quasi_identifiers = ['Магазин','Координаты','Номер карты','Количество', 'Цена','Товар','Производитель'] # 
    worst_k, best_k = calculate_k_anonymity(df, quasi_identifiers,all='no')
    
    
    
    print("Топ-3 худших строк по k-анонимности:")
    print(worst_k)

    print("\n Топ-3 лучших строк по k-анонимности:")
    print(best_k,'\n\n')
    print(df.head(n=1000))

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