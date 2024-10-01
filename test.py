import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

columns = ['ФИО', 'Паспортные данные', 'СНИЛС', 'Симптомы', 'Выбор врача', 
           'Дата посещения врача', 'Анализы', 'Дата получения анализов', 
           'Стоимость анализов', 'Карта оплаты']


def delete_attribute(df, col):
    mask = []
    for data in df[col]:
        mask.append(' ')
    df[col] = mask
    return df


def loc_gen_passport(df, col):
    passports = []
    for num in df[col]:
        if str(num)[0] == 'N':
            passports.append('Казахстан')
        elif str(num)[0].isdigit():
            passports.append('Россия')
        else:
            passports.append('Беларусь')
    df[col] = passports
    return df


def SNILS(df, col):
    sn = []
    for s in df[col]:
        new = "*" * 11 + str(s)[-2:]
        sn.append(new)
    df[col] = sn
    return df


def num_of_attributes(df, col):
    atributes = []
    for s in df[col]:
        atributes.append((s.count(',')+1))
    df[col] = atributes
    return df


def psevdonim(df, col):
    names = []
    department = {
    'Приемное отделение': ['Психиатр', 'Невролог', 'Офтальмолог', 'Физиотерапевт', 'Пульмонолог', 'Аллерголог', 'Кардиолог', 'Гериатр', 'Гепатолог', 'Иммунолог', 'Педиатр', 'Неонатолог'],
    'Палатные отделения': ['Гастроэнтеролог', 'Дерматолог', 'Уролог', 'Лор', 'Травматолог', 'Стоматолог', 'Эндокринолог', 'Гематолог', 'Неонатолог', 'Ревматолог', 'Гинеколог', 'Онкодерматолог', 'Невропатолог', 'Кардиоревматолог', 'Косметолог', 'Диетолог', 'Ортодонт', 'Фтизиатр', 'Ортопед', 'Оториноларинголог', 'УЗИ-специалист'],
    'Лечебно-диагностические отделения': ['Онколог', 'Эндоскопист', 'Онкоуролог', 'Генетик']
}
    for name in df[col]:
        for depart, doctors in department.items():
            if name in doctors:
                names.append(depart)
                break
            else:
                names.append('Лаборатория')
                break
    df[col] = names      
    return df


def date_mask(df, col):
    mask = []
    for data in df[col]:
        date = data[:5] + "XX" + "-" + "X" * 5 + ":" + "XX" + "+" + "XX" + ":" + "XX"
        mask.append(date) 
    df[col] = mask
    return df


def ma_cost(df, col, num_intervals=5):
    anon_col = []
    max_val = df[col].max()
    min_val = df[col].min()
    interval_size = (max_val - min_val) / num_intervals
    intervals = [(min_val + i * interval_size, min_val + (i+1) * interval_size) for i in range(num_intervals)]
    for val in df[col]:
        anon_value = np.mean([interval[0] for interval in intervals if interval[0] <= val <= interval[1]])
        anon_col.append(anon_value)
    df[col] = anon_col
    return df


def card_mask(df, col):
    cards = []
    for card in df[col]:
        mask = str(card)[:4] + "X" * 12
        cards.append(mask)
    df[col] = cards
    return df


def anonymization(path):
    df = pd.read_excel(path)
    delete_attribute(df, 'ФИО')
    loc_gen_passport(df, 'Паспортные данные')
    SNILS(df, 'СНИЛС')
    num_of_attributes(df, 'Симптомы')
    psevdonim(df, 'Выбор врача')
    date_mask(df, 'Дата посещения врача')
    num_of_attributes(df, 'Анализы')
    date_mask(df, 'Дата получения анализов')
    ma_cost(df, 'Стоимость анализов')
    card_mask(df, 'Карта оплаты')
    return df

def k_anonymity(df, selected):
    k_anon = True
    k = 1
    while k_anon:
        k_anon = calculate_k_anonymity(df, selected, k)
        k += 1
        if k > 19:
            break
    return (k-2)

def calculate_k_anonymity(df, columns, k):
    group_counts = df.groupby(columns).size().reset_index(name='count')
    return all(group_counts['count'] >= k)


loaded_file_path = None 
def load_file():
    global loaded_file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        loaded_file_path = file_path
        file_label.config(text="Файл загружен")

def handle_attributes():
    selected_attributes = []
    for attribute, var in attribute_vars.items():
        if var.get() == 1:
            selected_attributes.append(attribute)
    if loaded_file_path == None:
        messagebox.showinfo("Внимание!", "Файл не был загружен.")
    else:   
        df = anonymization(loaded_file_path)
        k = k_anonymity(df, selected_attributes)
        messagebox.showinfo("Датасет обезличен", f"K-anonymity = {k}")
        group_counts = df.groupby(selected_attributes).size().reset_index(name='count')
        bad_k_values = group_counts[group_counts['count'] < k].head(5)

        percentage_bad_k = (len(bad_k_values) / len(group_counts)) * 100

        #print(f"\nПлохие значения K-анонимности (первые 5):")
        #print(bad_k_values)
        #print(f"\nПроцент 'плохих' значений K-анонимности: {percentage_bad_k:.2f}%")


def k_anon():
    selected_attributes = []
    for attribute, var in attribute_vars.items():
        if var.get() == 1:
            selected_attributes.append(attribute)
    if loaded_file_path == None:
        messagebox.showinfo("Внимание!", "Файл не был загружен.")
    else:
        df = pd.read_excel(loaded_file_path)
        k = k_anonymity(df, selected_attributes)
        messagebox.showinfo("Вычисленное значение", f"k-anonymity = {k}")
        
root = tk.Tk()
root.title("Обезличиватель датасета")
root.geometry("500x600")

greeting_label = tk.Label(root, text="Добро пожаловать! Выберите квази-идентификаторы:", font=("Arial", 14))
greeting_label.pack(pady=20)
load_button = tk.Button(root, text="Загрузить файл", command=load_file, font=("Arial", 12), bg="lightblue")
load_button.pack(pady=10)
file_label = tk.Label(root, text="", font=("Arial", 12))
file_label.pack(pady=10)

attribute_vars = {}

for attribute in columns:
    var = tk.IntVar(value=0)
    attribute_vars[attribute] = var
    checkbox = tk.Checkbutton(root, text=attribute, variable=var, font=("Arial", 12))
    checkbox.pack(anchor=tk.W)

process_button = tk.Button(root, text="Обезличить и вычислить", command=handle_attributes, font=("Arial", 12), bg="green", fg="white")
process_button.pack(pady=20)
load_button2 = tk.Button(root, text="Вычислить k-anonymity", command=k_anon, font=("Arial", 12), bg="green", fg="white")
load_button2.pack(pady=25)

root.mainloop()