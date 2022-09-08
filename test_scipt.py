import pandas as pd
import numpy as np
import re

female_names = open("ru_female_names.txt", encoding = 'utf-8').read().lower().split('\n')
male_names = open("ru_male_names.txt", encoding = 'utf-8').read().lower().split('\n')

# считываем данные
df = pd.read_csv('test_data.csv')

# создаем новую колонку для записи результатов
df['insight'] = np.nan

# подсчет количества диалогов
dialogues = df['dlg_id'].unique()

# для каждого диалога в датасете
for i in dialogues:

#     метки - соблюдались ли правила для приветствия и прощания
    hi = False
    bye = False
    print('Диалог', i)
#     выбираем только строки соответствующего диалога, которые произносил менеджер
    df_ = df[(df['dlg_id'] == i)&(df['role'] == 'manager')]

#     для каждой строки в выбранной совокупности
    for j in range(0, len(df_)):

#         извлекаем текст
        text = df_['text'].iloc[j]
#     шаблон для приветствия
        rs1 = re.findall(r"(?i)здравст*|добрый*\s\w+|привет*", text)
        if len(rs1) != 0:
            print('Приветствие:', text)
            df['insight'].iloc[df_[df_['text']==df_['text'].iloc[j]].index] = 'Greeting'
            hi = True

#         шаблон для представления
        rs2 = re.findall(r"(?i)меня\s|зовут*\s\w+", text)
        if len(rs2) != 0:
            print('Менеджер представил себя:', text)
            df['insight'].iloc[df_[df_['text']==df_['text'].iloc[j]].index] = 'Introduction'

#             поиск имен
            words = text.split(' ')
            for word in words:
                if word in female_names or word in male_names:
                    print('Имя менеджера:', word)
#             шаблон для названия компании
            rsc = re.findall(r"компания\s\w+\sбизнес|компания\s\w+", text)
            print('Название компании:', rsc[0][9:])

#         шаблон для прощания
        rs3 = re.findall(r"(?i)всего\sхор*|до*\sсвид*", text)
        if len(rs3) != 0:
            print('Прощание:', text)
            df['insight'].iloc[df_[df_['text']==df_['text'].iloc[j]].index] = 'Saying_bye'
            bye = True
#     проверка соблюдения требований
    print('Проверка требования к менеджеру: «В каждом диалоге обязательно необходимо поздороваться и попрощаться с клиентом»: ')
    if hi and bye:
        print('Выполнено')
    elif hi and bye==False:
        print('Не выполнено - Прощание')
    elif hi==False and bye:
        print('Не выполнено - Приветствие')
    else:
        print('Не выполнено')
    print()
    print('-----------')
    print()

df.to_csv('test_result.csv')
