import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import time

columns = ['Магазин', 'Координаты', 'Дата и время', 'Товар', 'Производитель', 
           'Номер карты', 'Количество', 'Цена', 
            ]

bad_locations = set(['Технополис Политехнический' ,'Красные Зори' ,'Технопарк Мебельная' ,'Глобус Джус' ,'Туристическое агентство Глобус' ,'Технопарк Рот Фронт' ,'Приневский технопарк' ,'СберМаркет' ,'Издательство Утконос' ,'Технопарк Боровая' ,'Технопарк Арсенал' ,'Азбука Вкуса' ,'Звезда' ,'Павловский коммунальный технопарк' ,'Промышленный Парк на Дерибасовской' ,'Hiker' ,'Промышленный Парк' ,'Ленполиграфмаш' ,'Машиностроительный технопарк Гагарин' ,'Технопарк Санкт-Петербурга' ,'Индустриальный парк Greenstate' ,'Технопарк Мариенбург' ,'Технопарк Новикова' ,'Рандеву' ,'Технопарк' ,'PiterGSM' ,'Street Beat Kids' ,'Технопарк Нарвский'])

item_dict = { # 10 unique categories -> micro agreggation
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
    'сок': 'еда готовая',
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
    'колонки': 'фото/видео/аудио техника',
    'наушники': 'фото/видео/аудио техника',
    'наушники беспроводные': 'фото/видео/аудио техника',
    'усилитель': 'фото/видео/аудио техника',
    'телевизор': 'бытовая техника',
    'ноутбук': 'компьютерная техника',
    'планшет': 'компьютерная техника',
    'смартфон': 'компьютерная техника',
    'пылесос': 'бытовая техника',
    'микроволновка': 'бытовая техника',
    'камера': 'фото/видео/аудио техника',
    'проигрыватель': 'фото/видео/аудио техника',
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
    'фотоаппарат': 'фото/видео/аудио техника',
    'умные часы': 'фото/видео/аудио техника',
    'часы': 'фото/видео/аудио техника',
    'мышь': 'компьютерная техника',
    'монитор': 'компьютерная техника',
    'фитнес-трекер': 'фото/видео/аудио техника',
    'мюсли': 'еда готовая',
    'бекон': 'мясные продукты',
    'колбаса': 'мясные продукты',
    'крупы': 'еда готовая',
    'газированные напитки': 'еда готовая',
    'гарнитура': 'фото/видео/аудио техника',
    'снеки': 'еда готовая',
    'саундбар': 'фото/видео/аудио техника',
    'вода': 'еда готовая',
    'кепка': 'одежда',
    'процессор': 'компьютерная техника',
    'консервированные овощи': 'еда готовая',
    'десерты': 'еда готовая',
    'проектор': 'компьютерная техника',
    'молоко 1.5%': 'молочный продукт',
    'туфли': 'одежда',
    'видеокарта': 'компьютерная техника',
    'соки': 'еда готовая',
    'приправы': 'соус',
    'компьютер': 'компьютерная техника',
    'носки': 'одежда',
    'сыр': 'молочный продукт',
    'колбасы': 'мясные продукты',
    'утюг': 'бытовая техника',
    'сосиски': 'мясные продукты',
    'плеер': 'фото/видео/аудио техника',
    'роутер': 'компьютерная техника',
    'брюки': 'одежда',
    'молоко 3.2%': 'молочный продукт',
    'адаптер': 'компьютерная техника',
    'модем': 'компьютерная техника',
    'объектив': 'фото/видео/аудио техника',
    'клавиатура': 'компьютерная техника',
    'ряженка': 'молочный продукт',
    'лампа': 'бытовая техника',
    'зарядное устройство': 'компьютерная техника',
    'лапша': 'еда готовая',
    'квас': 'еда готовая',
    'пуховик': 'одежда',
    'материнская плата': 'компьютерная техника',
    'горчица': 'соус',
    'соусы': 'соус',
    'макароны': 'еда готовая',
    'спортивная куртка': 'одежда',
    'датчик сердечного ритма': 'фото/видео/аудио техника',
    'пиво': 'еда готовая',
    'вермишель': 'еда готовая',
    'бейсболка': 'одежда',
    'стиральная машина': 'бытовая техника',
    'мясные продукты': 'мясные продукты',
    'штатив': 'фото/видео/аудио техника'
}


def read_csv(file_name, delimiter=';') -> pd.DataFrame: 
    df_csv = pd.read_csv(file_name, sep=delimiter)
    return df_csv

# заменяет название товара на одну из категорий (11 штук)
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

# заменяет название бренда на общую категорию (clothes food electronics)
def brand_mask(df, col):
    out = []
    for brand,general_category in df[[col,'Магазин']].values:
        out.append(general_category)
    df[col] = out
    return df

# оставляет только первые 4 цифры карты
def card_mask(df, col):
    # Определение диапазонов для MASTERCARD и VISA
    mastercard_prefixes = ['51', '52', '53', '54', '55']  # основные префиксы MASTERCARD
    visa_prefixes = ['4']  # основной префикс для VISA

    def mask_card(card_number):
        card_str = str(card_number)
        first_four = card_str[:4]
        
        # Определение платежной системы по первым цифрам
        if first_four[:2] in mastercard_prefixes:
            # Для MASTERCARD объединяем
            return "MASTERCARD-" + "X" * 12
        elif first_four[:1] in visa_prefixes:
            # Для VISA объединяем
            return "VISA-" + "X" * 12
        else:
            # Для других карт оставляем только первые 4 цифры
            return first_four + "X" * 12

    # Применение маскирования к каждому значению столбца
    df[col] = df[col].apply(mask_card)
    
    return df


# если у сети магазинов с одним названием много точек по городу, то меняет их общие координаты на коордианыт одного магазина 
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
# сохраняет только год покупки
def date_mask(df, col):
    mask = []
    for data in df[col]:
        date = data[:10] + "TXX" + ":" + "XX"
        mask.append(date) 
    df[col] = mask
    return df

# возваращет категорию магазина (например М.Видео -> electronics, Zara -> clothes)
def get_shop_category(df, shop_name):
    # Находим строку, где название магазина совпадает с переданным
    category = df.loc[df['shop_name'] == shop_name, 'category_type']

    if not category.empty:
        return category.values[0]  # Возвращаем первый найденный тип продукта
    else:
        return 'None'
    
# заменяет название магазина на общую категорию (clothes food electronics)
def shop_mask(df,col):
    df_shops = pd.read_csv('input_data/shop_locations.csv', sep=';',names=['category_type','shop_name', 'coordinates'])
    out = []
    for shop_name in df[col]:
        out.append(get_shop_category(df_shops,shop_name))
    df[col] = out
    return df

# заменяет точное количество купленного товара на обощение
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

# заменяет точную цену купленного товара на обощение
def price_mask(df,col):
    out = []
    for price,amount in df[[col,'Количество']].values:
        price /= amount
        if price < 5000:
            out.append('< 5000')
        elif price < 10000:
            out.append('< 10000')
        elif price >= 10000:
            out.append('>= 10000')
    df[col] = out
    return df

def add_k_anonymity_column(df, quasi_identifiers):
    """
    Функция для добавления k-anonymity к каждой строке датасета
    на основе квазиидентификаторов.
    
    :param df: DataFrame
    :param quasi_identifiers: Список квазиидентификаторов
    :return: DataFrame с добавленным столбцом 'k-anonymity'
    """
    # Группируем по квазиидентификаторам и считаем количество строк в каждой группе
    grouped = df.groupby(quasi_identifiers).size().reset_index(name='k-anonymity')
    
    # Объединяем исходный DataFrame с группированным, чтобы добавить столбец 'k-anonymity'
    df_with_k = df.merge(grouped, on=quasi_identifiers, how='left')
    
    return df_with_k

def remove_worst_k_anonymity_rows(df, max_percent=0.05):
    """
    Функция для удаления строк с самым низким показателем k-anonymity,
    но не более max_percent от общего количества строк.
    Возваращет отсортированный по возрастанию датасет
    
    :param df: DataFrame с добавленным столбцом 'k-anonymity'
    :param max_percent: Максимальный процент строк для удаления (по умолчанию 5%)
    :return: DataFrame с удалёнными строками
    """
    # Определяем количество строк, которые нужно удалить (максимум 5%)
    n_rows_to_remove = int(len(df) * max_percent)
    
    # Сортируем DataFrame по столбцу 'k-anonymity' в порядке возрастания
    df_sorted = df.sort_values(by='k-anonymity')
    
    # Удаляем первые n строк с самым низким k-anonymity
    df_trimmed = df_sorted.iloc[n_rows_to_remove:]
    
    return df_trimmed

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


def k_anonymity_statistics(df, k_threshold=7):
    """
    Функция для подсчета количества строк, k-anonymity которых меньше указанного порога,
    а также для вычисления среднего, медианного, максимального и минимального значений k-anonymity.

    :param df: DataFrame с добавленным столбцом 'k-anonymity'
    :param k_threshold: Пороговое значение для подсчета строк (по умолчанию 7)
    :return: Словарь с количеством строк с k-anonymity меньше порога и статистикой
    """
    # Подсчет количества строк с k-anonymity меньше порога
    count_below_threshold = (df['k-anonymity'] < k_threshold).sum()

    # Вычисление статистических значений
    mean_k = df['k-anonymity'].mean()
    median_k = df['k-anonymity'].median()
    max_k = df['k-anonymity'].max()
    min_k = df['k-anonymity'].min()

    # Возвращаем статистику и количество строк
    stats = {
        'count_below_threshold': count_below_threshold,
        'percent_below_threshold': (str( round(((count_below_threshold/len(df))*100),1) ) + '%'),
        'mean_k': mean_k,
        'median_k': median_k,
        'max_k': max_k,
        'min_k': min_k,
        'number of rows': len(df),
    }

    return stats


    
if __name__ == '__main__':
    # TODO : shop_name, item_name, brand_name, amount, price
    df = read_csv(file_name='input_data/all_types_10k.csv',delimiter=';')
    print(df.head())
    location_stores = get_store_coordinates('input_data/shop_locations.csv')
    coordinates_mask_alternative(df,'Координаты')
    date_mask(df,'Дата и время')
    shop_mask(df,'Магазин')
    card_mask(df,'Номер карты')
    price_mask(df,'Цена')
    amount_mask(df,'Количество') # always after price_mask
    item_mask(df,'Товар')
    brand_mask(df,'Производитель')
    


    quasi_identifiers = ['Магазин','Координаты','Номер карты','Количество', 'Цена','Товар','Производитель'] # 
    
    df = add_k_anonymity_column(df,quasi_identifiers)
    df = remove_worst_k_anonymity_rows(df, max_percent=0.05)
    stats2 = k_anonymity_statistics(df, k_threshold=7)
    print(df.head(),'\n\n')

    for k in stats2.keys():
        print(k,stats2[k])
    
    # worst_k, best_k = calculate_k_anonymity(df, quasi_identifiers,all='no')
    
    
    
    # print("Топ-3 худших строк по k-анонимности:")
    # print(worst_k)

    # print("\n Топ-3 лучших строк по k-анонимности:")
    # print(best_k,'\n\n')
    # print(df.head(n=1000))

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