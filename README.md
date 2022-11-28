El programa pizza2.2.py recibe 3 csv: orders.csv, order_details.csv y pizza_types.csv. Los primeros csvs nombrados no están limpios, es decir, contienen caracteres que no se pueden leer adecuadamente como por ejemplo 'cl@assic' en lugar de 'classic'. Es por esto que se necesita filtrar estos dos data frames previamente, para poder trabajar con los datos. El programa devuelve estos dos csvs limpios: orders_limpio.csv y order_details_limpio.csv. 
El programa pizza2.2.py luego utiliza estos dataframes ya limpios para concluir una predicción de la compra en la pizzeria una semana normal, y devuelve estos resultados en un csv final llamado 'prediccion_final.csv'. Se incluye un informe de calidad que analiza los ficheros de datos una vez limpios.

Para ejecutar el programa es necesario tener instalado python3. 

Para instalar las librerías nombradas en el requirements.txt se deberán ejecutar los siguientes comandos:
```python
pip3 install -r requirements.txt
```
