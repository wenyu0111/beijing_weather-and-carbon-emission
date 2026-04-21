import pandas as pd
import numpy as np
from prophet import Prophet
import warnings
warnings.filterwarnings('ignore')

import os
os.chdir('/Users/zhangwenyu/Desktop/2630代码及原始数据/')

df_weather = pd.read_csv('beijing_weather_2021_2025.csv')
df_weather['date'] = pd.to_datetime(df_weather['date'])
df_weather['avg_temp'] = (df_weather['highest_temp'] + df_weather['lowest_temp']) / 2

df_temp = df_weather[['date', 'avg_temp']].rename(columns={'date': 'ds', 'avg_temp': 'y'})

df_co2_1 = pd.read_excel('carbon-monitor-CITIES-maingraphdatas2021-2022.xlsx')
df_co2_2 = pd.read_excel('carbon-monitor-CITIES-maingraphdatas2023-2025.xlsx')
df_co2 = pd.concat([df_co2_1, df_co2_2], ignore_index=True)

df_co2['date'] = pd.to_datetime(df_co2['date'], format='%d/%m/%Y')
df_co2_daily = df_co2.groupby('date')['ktCO2 per day'].sum().reset_index()

df_co2 = df_co2_daily.rename(columns={'date': 'ds', 'ktCO2 per day': 'y'})

model_temp = Prophet(seasonality_mode='additive', yearly_seasonality=True, daily_seasonality=False)
model_temp.fit(df_temp)

model_co2 = Prophet(seasonality_mode='additive', yearly_seasonality=True, daily_seasonality=False)
model_co2.fit(df_co2)

def predict_by_date(target_date_str):
    future = pd.DataFrame({'ds': [pd.to_datetime(target_date_str)]})
    
    temp_forecast = model_temp.predict(future)
    temp_pred = temp_forecast['yhat'].values[0]
    high_pred = temp_pred + 6
    low_pred = temp_pred - 6
    
    co2_forecast = model_co2.predict(future)
    co2_pred = co2_forecast['yhat'].values[0]
    
    return {
        'Date': target_date_str,
        'Predicted Daily Temperature (°C)': round(float(temp_pred), 1),
        'Predicted Highest Temperature (°C)': round(float(high_pred), 1),
        'Predicted Lowest Temperature (°C)': round(float(low_pred), 1),
        'Predicted Total Carbon Emission (ktCO₂/day)': round(float(co2_pred), 2)
    }

if __name__ == '__main__':
    result = predict_by_date('2026-01-01')
    print("✅ Result：")
    print(result)