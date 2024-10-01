import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import time

columns = ['Магазин', 'Координаты', 'Дата и время', 'Товар', 'Производитель', 
           'Номер карты', 'Количество', 'Цена', 
            ]


def calculate_time(func, df, *args):
    start_time = time.time()  # Замеряем начальное время
    result = func(df, *args)  # Выполняем переданную функцию
    end_time = time.time()    # Замеряем конечное время
    execution_time = end_time - start_time  # Рассчитываем время выполнения
    
    print(f"Время выполнения функции {func.__name__}: {execution_time:.6f} секунд")
    return result

def read_csv(file_name, delimiter=';') -> pd.DataFrame: 
    df_csv = pd.read_csv(file_name, sep=delimiter)
    #print(df_csv.head())
    #print(df_csv.shape)
    #print('-----------------\n')
    return df_csv


def calculate_k_anonymity(df, quasi_identifiers, all='no'):
    if all == 'yes':
        quasi_identifiers = df.columns
    
    # Группируем по квазиидентификаторам и считаем количество строк в каждой группе
    grouped = df.groupby(quasi_identifiers).size().reset_index(name='k-anonymity')
    
    # df_with_k теперь содержит только уникальные строки с k-анонимностью
    df_with_k = grouped.copy()
    print(df_with_k.head())
    
    # Сортируем по 'k-anonymity', чтобы найти строки с наибольшей и наименьшей k-анонимностью
    worst_k_anonymity = df_with_k.sort_values('k-anonymity').head(3)
    best_k_anonymity = df_with_k.sort_values('k-anonymity', ascending=False).head(3)
    
    # Подсчитываем количество строк с k-анонимностью меньше 5
    count_k_less_than_5 = (df_with_k['k-anonymity'] < 7).sum()
    print(f"\nКоличество строк с k-анонимностью меньше 7: {count_k_less_than_5}")

    return worst_k_anonymity, best_k_anonymity



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
    
    # Проверяем, если найдено значение
    if not category.empty:
        return category.values[0]  # Возвращаем первый найденный тип продукта
    else:
        return 'None'
    
def shop_mask(df,col):
    df_shops = pd.read_csv('shop_locations.csv', sep=';',names=['category_type','shop_name', 'coordinates'])
    out = []
    for shop_name in df[col]:
        out.append(get_shop_category(df_shops,shop_name))
    df[col] = out
    return df
    
if __name__ == '__main__':
    # TODO : shop_name, item_name, brand_name, amount, price
    df = read_csv(file_name='input_data/all_types_55k.csv',delimiter=';')

    
    coordinates_mask(df,'Координаты')
    date_mask(df,'Дата и время')
    shop_mask(df,'Магазин')

    
    
    
    
    quasi_identifiers = ['Магазин','Дата и время','Координаты'] # 
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