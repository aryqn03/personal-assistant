# Long term goals
# How portfolio does as a whole
# Key individual stocks -> performance
# P/E ratio if applicable
# Indicators of potential investments


# profileData 
# gives ['url', 'account', 'start_date', 'market_value', 'equity',
# 'extended_hours_market_value', 'extended_hours_equity',
# 'extended_hours_portfolio_equity', 'last_core_market_value', '
# last_core_equity', 'last_core_portfolio_equity', 'excess_margin',
# 'excess_maintenance', 'excess_margin_with_uncleared_deposits',
# 'excess_maintenance_with_uncleared_deposits', 'equity_previous_close',
# 'portfolio_equity_previous_close', 'adjusted_equity_previous_close',
# 'adjusted_portfolio_equity_previous_close', 'withdrawable_amount',
# 'unwithdrawable_deposits', 'unwithdrawable_grants', 'is_primary_account']

# allTransactions
# gives ['id', 'ref_id', 'url', 'cancel', 'ach_relationship',
# 'account', 'amount', 'direction', 'state', 'fees',
# 'status_description', 'scheduled', 'expected_landing_date',
# 'early_access_amount', 'created_at', 'updated_at', 'rhs_state',
# 'expected_sweep_at', 'expected_landing_datetime', 'investment_schedule_id',
# 'managed_by_ph', 'instant_limit_to_grant']

from collections import defaultdict
import pandas as pd
import robin_stocks.robinhood as r
import matplotlib.pyplot as plt
import config as config
from datetime import datetime

def current_status():
    print('\n')

    days_return = float(profileData['equity']) - float(profileData['adjusted_equity_previous_close'])
    if days_return < 0:
        print(
            f'Unfortunately, you took an L of ${round(days_return,3)} today. ({datetime.now().strftime("%d/%m/%Y %H:%M:%S")})')
    else:
        print(f'Lets go! You made ${round(days_return,3)} today! ({datetime.now().strftime("%d/%m/%Y %H:%M:%S")})')
    
    deposits = 0
    for i in range(len(allTransactions)):
        deposits += float(allTransactions[i]['amount'])
    percent_change = round(((float(profileData["equity"]) - float(deposits)) * 100) / float(deposits), 2)
    print(f'The market value of your portfolio is ${profileData["equity"]}')
    print(f'Your all time % change is {percent_change}%')
    print(f'You have ${profileData["withdrawable_amount"]} to spend my G!')
    print('\n')
    
    # print('General Information:\n')
    # print(f'Market value: ${profileData["market_value"]}')
    # print(f'(Extended Hour) Equity: ${profileData["extended_hours_equity"]}')
    # print(f'Buying power: ${profileData["withdrawable_amount"]}')
    # print(f'Prev-close equity: ${profileData["adjusted_equity_previous_close"]}')
    # print(f'Day change: {days_return}')    

def deposits_analysis():
    # deposit_data = {}
    # for i in range(len(allTransactions)):
    #     deposit_data[allTransactions[i]["expected_landing_date"]
    #         ] = allTransactions[i]["amount"]

    # date = list(deposit_data.keys())
    # amount = [float(value) for value in deposit_data.values()]

    # # Create the bar chart
    # plt.bar(date[::-1], amount[::-1], width=0.6, align='center', color='blue')
    # plt.xlabel('Date')
    # plt.ylabel('$USD')
    # plt.title('Deposits History')
    # plt.xticks(rotation=15)  # Rotate x-axis labels for better visibility
    # plt.xticks(fontsize=7)
    # plt.show()
    deposit_data = defaultdict(float)

    for transaction in allTransactions:
        expected_landing_date = transaction["expected_landing_date"]
        amount = float(transaction["amount"])
        year, month, _ = expected_landing_date.split("-")
        key = f"{year}-{month}"
        deposit_data[key] += amount
    
    months = list(deposit_data.keys())[::-1]
    amounts  = list(deposit_data.values())[::-1]

    plt.bar(months, amounts, width=0.6, align='center', color='blue')
    plt.xlabel('Month')
    plt.ylabel('$USD')
    plt.title('Deposit History by Month')
    plt.xticks(rotation=45)
    plt.show()




def portfolio_perf():
    print('\n')
    holdings = r.build_holdings()
    perf_dict = {}
    for stock in holdings.keys():
        perf_dict[stock] = float(holdings[stock]['percent_change'])
    sorted_perf_dict = dict(sorted(perf_dict.items(), key=lambda item: (item[1]), reverse=True))

    print("------Top to Bottom Performers By % Change-----------\n")
    for num, stock in enumerate(sorted_perf_dict, start=1):
        print(f"{num}. {stock} : {sorted_perf_dict[stock]}")
    print('---------------------------------------------------------\n')

def moving_avg():
    # Get historical data for AAPL
    historical_data = r.get_stock_historicals('AAPL', span='3month')

    # Convert to DataFrame
    df = pd.DataFrame(historical_data)
    df['begins_at'] = pd.to_datetime(df['begins_at'])
    df.set_index('begins_at', inplace=True)
    df['close_price'] = df['close_price'].astype(float)

    # Calculate moving averages
    df['7_day_avg'] = df['close_price'].rolling(window=7).mean()
    df['14_day_avg'] = df['close_price'].rolling(window=14).mean()

    # Plot data
    plt.figure(figsize=(12,6))
    plt.plot(df['close_price'], label='Close Price')
    plt.plot(df['7_day_avg'], label='7 Day Moving Average')
    plt.plot(df['14_day_avg'], label='14 Day Moving Average')
    plt.legend(loc='best')
    plt.title('AAPL Close Price with 7 and 14 Day Moving Averages')
    plt.show()    


if __name__ == '__main__':
    login = r.login(config.rbh_user, config.rbh_pass)
    my_stocks = r.build_holdings()
    # for name,info in my_stocks.items():
    #     print(name,info['price'])
    profileData = r.load_portfolio_profile()
    allTransactions = r.get_bank_transfers()

    menu = {}
    menu['1'] = "Current Status"
    menu['2'] = "Deposit History"
    menu['3'] = "Portfolio Performance"
    menu['4'] = "Potential next moves"
    menu['5'] = "Exit"

    while True:
        options = menu.keys()
        for entry in options:
            print(entry, menu[entry])

        selection = input("Please Select: ")
        if selection == '1':
            current_status()
        elif selection == '2':
            deposits_analysis()
        elif selection == '3':
            portfolio_perf()
        elif selection == '4':
            sub_menu = {}
            sub_menu['1'] = "Moving Avg Analysis"
            sub_menu['2'] = "Back to Main Menu"
            while True:
                options = sub_menu.keys()
                for entry in options:
                    print(entry, sub_menu[entry])
                
                selection = input("Please Select: ")
                if selection == '1':
                    moving_avg()
                elif selection == '2':
                    print("maybe make the menu functionality another file and connect it, to navigate thru it better")
                    break
        elif selection == '5':
            break
        else:
            print('\n')
            print("Unknown option selected!")
            print('\n')

