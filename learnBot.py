# import the libraries we need
import shrimpy
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# insert your public and secret keys here
public_key = '1930af65a9e42525a057c14cd816b0d582df36a3ac4e39c850294666185c5d91'
secret_key = 'b480b278b729cf73d203a2816fa1765cd26845d106181ba62f897e4547ca7ec5e2f90375a65f2f0596c0434e875ae0f0c02954e1bfde72401ed59e3822af0529'

# create the client
client = shrimpy.ShrimpyApiClient(public_key, secret_key)

trading_pairs = client.get_trading_pairs('binance')
wanted_pairs = []
for pair in trading_pairs:
    if pair['quoteTradingSymbol'] == 'USDT':
        if pair['baseTradingSymbol'] == 'ETH' or pair['baseTradingSymbol'] == 'LTC' or pair['baseTradingSymbol'] == 'BTC':
            wanted_pairs.append(pair)

all_coin_candles = {}
# for pair in wanted_pairs:
#     all_coin_candles[pair['baseTradingSymbol'] + "/" + pair['quoteTradingSymbol']] = client.get_candles('binance', pair['baseTradingSymbol'], pair['quoteTradingSymbol'], '1d')

percentages = {}
# for coin_candles in all_coin_candles:
#     coin_candle_percentages = []
#     for candle in all_coin_candles[coin_candles]:
#         percentage_change = float('{:.2f}'.format(((float(candle['close']) - float(candle['open'])) / float(candle['open'])) * 100))
#         coin_candle_percentages.append(percentage_change)
#     percentages[coin_candles] = coin_candle_percentages

precursors_to_growth = {}
for coin_percentages in percentages:
    temp = []
    for i in range(len(percentages[coin_percentages])):
        if i != 0:
            if percentages[coin_percentages][i] > 0:
                temp.append(percentages[coin_percentages][i-1])
    precursors_to_growth[coin_percentages] = temp



def get_candles(exchange, base_symbols, quote_symbol, api_client, time_period='1h'):
    # Input information, returns a dictionary of trading pairs. Each equaling a list of candles
    candles = {}
    for base_symbol in base_symbols:
        candles[base_symbol + "/" + quote_symbol] = api_client.get_candles(exchange, base_symbol, quote_symbol, time_period)
    return candles

def get_candle_percentages(candle_dictionary, dp=2):
    # Input list dictionary of candles, returns dictionary of % changes
    percentages = {}
    dp_string = '{' + ':.{}f'.format(str(dp)) + '}'
    for coin in candle_dictionary:
        candle_percentages = []
        for candle in candle_dictionary[coin]:
            percentage_change = float(dp_string.format(((float(candle['close']) - float(candle['open'])) / float(candle['open'])) * 100))
            candle_percentages.append(percentage_change)
        percentages[coin] = candle_percentages
    return percentages

def most_frequent(data):
    # Input list of data, returns most common item from data
    counter = 0
    num = data[0]
    for i in data:
        curr_frequency = data.count(i)
        if curr_frequency > counter:
            counter = curr_frequency
            num = i
    return num

def most_shared(smaller_list, larger_list):
    # Input 2 lists, returns the item which corresponds in each list most.
    # EXAMPLE:
    # smaller_list = [ 1,2,2,2,2,3,4,4,4] larger_list = [4,4,4,2,2,2,2,2,2]
    # return 4 . Although there are more 2's all of the 4's in the larger list are in the smaller list.
    # A greater amount of 4's where successful and got to the smaller list
    current = None
    current_rating = 100
    current_amount = 0
    for item in smaller_list:
        rating = larger_list.count(item) / smaller_list.count(item)
        if rating < current_rating:
            current = item
            current_rating = rating
            current_amount = larger_list.count(item)
        elif rating == current_rating:
            if larger_list.count(item) > current_amount:
                current = item
                current_amount = larger_list.count(item)
    return current

# def show_most_common_precursors():
#     for coin in precursors_to_growth:
#         most_common = most_shared(precursors_to_growth[coin], percentages[coin])
#         print(coin)
#         print('Most Frequent:', most_common)
#         print('Appears in precursor:', precursors_to_growth[coin].count(most_common))
#         print('Appears in percentages', percentages[coin].count(most_common))
#         print('\n')


def get_pos_neg(data):
    # Input a list of data value, returns a list simplifying to -1 ,1 or 0
    pos_neg = []
    for item in data:
        if item > 0:
            pos_neg.append(1)
        elif item < 0:
            pos_neg.append(-1)
        else:
            pos_neg.append(0)
    return pos_neg


def get_patterns(data, minimum_occurrence=2, minimum_sequence_len=3, max_sequence_len=None, progress_tracker=False):
    #Input list of data, returns dictionary of all sequences that occur the minimum amount of times
    if max_sequence_len is None:
        max_sequence_len = len(data) // 6
    max_calc = len(data) * (max_sequence_len-minimum_sequence_len)
    current_calc = 0
    current_time = int(datetime.now().strftime('%S'))
    sequences = {}

    for sequence_len in range(minimum_sequence_len, max_sequence_len+1):
        for i in range(len(data)):
            current_calc +=1
            if int(datetime.now().strftime('%S')) > current_time + 5:
                if progress_tracker:
                    print(str(current_calc) +'/'+ str(max_calc))
                current_time = int(datetime.now().strftime('%S'))

            if (i + sequence_len) <= len(data):
                substring = data[i:i + sequence_len]
                # print(i,i+sequence_len)
                if str(substring) not in sequences:
                    substring_count = sum(1 for x in range(len(data)) if data[x:x + len(substring)] == substring)
                    if substring_count > (minimum_occurrence-1):
                        #print('LENGTH:' + str(sequence_len) + ' SUBSTRING:' + str(substring) + ' COUNT:' + str(substring_count))
                        sequences[str(substring)] = {'count': substring_count, 'length': sequence_len}

    return sequences
