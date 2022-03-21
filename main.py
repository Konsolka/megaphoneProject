import pandas as pd
import os.path
import generateFakeCSV


if __name__ == '__main__':
    if not os.path.isfile('actions.csv') or not os.path.isfile('users.csv'): # Проверка на наличие файлов для аггрегации в случае отсутсвия создаем
        generateFakeCSV.createFakeCSV()
    df = pd.read_csv('actions.csv')
    df['Метка времени'] = pd.to_datetime(df['Метка времени']).dt.date
    pv1 = pd.pivot_table(df, index=['id абонента', 'Метка времени'], columns=['Тип услуги'], values='Объем затраченных единиц', aggfunc=sum, fill_value=0)
    pv1.to_csv('outAggregation.csv')
