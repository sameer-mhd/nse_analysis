import mplfinance as mpf
import matplotlib.pyplot as plt


import datetime
mylist = [datetime.date.today()]
for date in mylist:
    dd = date

import requests
import pandas as pd
import json

for key,value in stk_id_dict.items():
    res = []
    ff = pd.DataFrame()
    url = "https://api.upstox.com/v2/historical-candle/"+value+"/day/2024-12-31/2024-01-01"
    payload={}
    headers = {
  'Accept': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    fn = data['data']
    gr = fn['candles']
    df = pd.DataFrame(gr)
    df.rename(columns={0: 'Date', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Close', 5:'Volume',6: 'Stock' }, inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Stock'] = key
    #df.set_index('Date', inplace=True)
    #ff = ff.append(df)
    ff = pd.concat([ff, df], ignore_index=True)

    ff['Date'] = pd.to_datetime(ff['Date'])
    ff['month'] = ff['Date'].dt.month

    for i in range(1,12):
        data = ff[ff['month'] == i]
        data = data.sort_values(by='Date')
        buy = int(data['Close'].head(1).iloc[0])
        
        # import pandas as pd
        # Convert data into a DataFrame
        df = pd.DataFrame(data)
        value = buy
    
        p_percentage = 10
        l_percentage = 5
        
        title_val =  str(data['Stock'].head(1).iloc[0])
        
        value_up = int(value * (1 + p_percentage / 100))  # Increase by percentage
        value_down = int(value * (1 - l_percentage / 100))
        
        up_value_open = df["Open"][1:] >=value_up
        up_value_high = df["High"] >= value_up
        up_value_low = df["Low"] >= value_up
        up_value_close = df["Close"] >= value_up

        down_value_open = df["Open"][1:] <=value_down
        down_value_high = df["High"] <= value_down
        down_value_low = df["Low"] <= value_down
        down_value_close = df["Close"] <= value_down

        first_date = data['Date']
        
        if up_value_open.any() == True:
            final = 'Margin'
        elif up_value_high.any() == True:
            final = 'Margin'
        elif up_value_low.any() == True:
            final = 'Margin'
        elif up_value_close.any() ==True:
            final = 'Margin'
        elif down_value_open.any() == True:
            final = 'Stop Loss'
        elif down_value_high.any() == True:
            final = 'Stop Loss'            
        elif down_value_low.any() == True:
            final = 'Stop Loss'
        elif up_value_close.any() ==True:
            final = 'Stop Loss'
        else:
            final = 'Hold'
       
    
        res.append(final)

        ################
        
        # Sort the DataFrame by 'Date'
        # df = df.sort_values(by='Date')
        
        # # Optional: Reset the index after sorting (if needed)
        # df = df.reset_index(drop=True)
        
        # # Ensure 'Date' is a datetime object
        # df['Date'] = pd.to_datetime(df['Date'])
        
        # # Set 'Date' as the index for mplfinance compatibility
        # df.set_index('Date', inplace=True)
        
        # # Select the required columns for candlestick plotting
        # ohlc_df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        
        # highlight_lines = [
        #     mpf.make_addplot([value_up] * len(ohlc_df), color='green', linestyle='--'),
        #     mpf.make_addplot([value] * len(ohlc_df), color='blue', linestyle='-'),
        #     mpf.make_addplot([value_down] * len(ohlc_df), color='red', linestyle='--')
        # ]
        
        # custom_style = mpf.make_mpf_style(
        #     base_mpf_style='yahoo',  # Use an existing style as a base
        #     facecolor='white',  # Background color
        #     gridstyle='-',         # Gridline style
        #     rc={'font.size': 8.5},   # Customize font size
        # )
    
        # investment = 10000
        
        # legend = ('Description:- ''BUY:',value,
        #           'Quantity:',int(investment/value),
        #           'Margin:',p_percentage,'%',int(value_up),
        #           'SL:',l_percentage,'%',int(value_down),
        #           'P&L:',int(value_up-value)*int(investment/value), final)
        
        # # Plot candlestick chart
        # fig, axes = mpf.plot(
        #     ohlc_df,
        #     title=title_val,
        #     type='candle',  # Candlestick chart
        #     ylabel="Price",
        #     volume=False,  # Enable volume plot
        #     style=custom_style,  # Use a predefined style
        #     addplot=highlight_lines,
        #     figsize=(10, 4),returnfig=True
        # )
    
        # if final == 'Margin':
        #     colour = 'Green'
        # elif final == 'Stop Loss':
        #     colour = 'Red'
        # else:
        #     colour = 'Blue'
        
        # ax = axes[0]  # Access the main axes (for price chart)
        # ax.text(
        #     0.5,  # x position (in normalized figure coordinates)
        #     1.0,  # y position (in normalized figure coordinates)
        #     legend,  # Text of the note
        #     transform=ax.transAxes,  # Positioning in axes coordinates
        #     ha='center',  # Horizontal alignment
        #     va='center',  # Vertical alignment
        #     fontsize=8.5,  # Font size
        #     color=colour,  # Text color
        #     weight='normal'  # Text weight
        # )
        # plt.show()
    

        
        ###############
    print('Margin:',res.count('Margin'),'|','Stop Loss:', res.count('Stop Loss'),'|','Hold:',res.count('Hold'), title_val)