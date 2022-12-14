from datetime import datetime
import pandas as pd
import numpy as np

def limpiar_datos_quantity(df):
    columna = df['quantity']
    for i in range(len(columna)):
        if columna[i] == 'one' or columna[i] == 'One' or columna[i] == '-1'or columna[i] == 'NaN':
            columna[i] = '1'
        elif columna[i] == 'two' or columna[i] == '-2':
            columna[i] = '2'
    df_limpio = df.dropna()
    return df_limpio

def limpiar_datos_pizza(df_orig):
    df = limpiar_datos_quantity(df_orig)
    diccionario = {'@': 'a', '-': '_', '3': 'e', '0': 'o', ' ': '_'}
    columna = df['pizza_id']
    for key, value in columna.iteritems():
        for error in diccionario:
            value = value.replace(error, diccionario[error])
        columna[key] = value
    df_fin = df.sort_values('order_id')
    df_fin = df_fin.reset_index().drop(columns=['index'])
    return df_fin

def limpiar_fechas(df_orders):
    df_limpio = df_orders.dropna()
    columna = df_limpio['date']
    for indice, valor in columna.iteritems():
        try: 
            nuevo_valor = pd.to_datetime(float(valor)+3600, unit='s')
        except:
            nuevo_valor = pd.to_datetime(valor)
        columna[indice] = nuevo_valor  
    df_final = df_limpio.drop('time', axis = 1)
    df_final = df_final.sort_values('order_id')
    df_final = df_final.reset_index().drop(columns=['index'])
    return df_final

def extract():
    df_order_details_sucio = pd.read_csv('order_details.csv', sep = ';', encoding = 'latin1')
    df_pizza_types = pd.read_csv('pizza_types.csv', encoding = 'latin1')
    df_orders_sucio = pd.read_csv('orders.csv', sep = ';', encoding = 'latin1')
    df_order_details = limpiar_datos_pizza(df_order_details_sucio)
    df_orders = limpiar_fechas(df_orders_sucio)
    csv_order_details = df_order_details.to_csv('order_details_limpio.csv')
    csv_orders = df_orders.to_csv('orders_limpio.csv')
    return df_order_details, df_orders, df_pizza_types

def transform(df_order_details, df_orders, df_pizza_types):
    df_order_details['ingredientes'] = '' # creo una nueva columna vac??a a a que le voy a a??adir los ingredientes de cada pizza

    #creo una lista a la que a??adir?? todos los ingredientes de cada pizza
    lista_ingredientes = [] 
    for i in range(len(df_pizza_types)):
        ingredientes = df_pizza_types['ingredients'].iloc[i].split(',')
        for ing in ingredientes:
            ing = ing.strip()
            if ing not in lista_ingredientes:
                lista_ingredientes.append(ing)

    for i in range(len(df_order_details)):
        tipo_pizza = df_order_details['pizza_id'][i]
        #utilizo este bucle para que me busque los ingredientes que tiene cada pizza en el dataframe df_pizza_types
        for j in range(len(df_pizza_types)): 
            if tipo_pizza[:-2] == df_pizza_types['pizza_type_id'][j]:
                ingredientes = df_pizza_types['ingredients'][j]
                df_order_details['ingredientes'][i] = ingredientes
    #creo una columna por cada ingrediente no repetido usando lista_ingredientes previamente creada
    for ing in lista_ingredientes:
        df_order_details[ing] = df_order_details['ingredientes'].str.contains(ing)

    diccionario = {}
    for ing in lista_ingredientes:
        suma = df_order_details[ing].sum()
        diccionario[ing] = suma // 53
    
    df_final = pd.DataFrame()
    df_final['ingredientes'] = ''
    df_final['cantidad'] = ''
    claves = list()
    valores = list()
    for key in diccionario:
        claves.append(key)
        valores.append(diccionario[key])
    df_final['ingredientes'] = claves
    df_final['cantidad'] = valores
    return df_final
        
def load(df_final, df_order_details, df_orders):
    csv_final = df_final.to_csv('prediccion_final.csv')
    return csv_final

if __name__ == '__main__':
    df1, df2, df3 = extract()
    df_final = transform(df1, df2, df3)
    print(df_final)
    prediccion_final = load(df_final, df1, df2)