import learnBot
import shrimpy


public_key = 'THIS IS PUBLIC'
secret_key = 'THIS IS A SECRET
client = shrimpy.ShrimpyApiClient(public_key, secret_key)

all_candles = learnBot.get_candles('binance', ['LTC', 'ETH', 'BTC'], 'USDT', api_client=client)
all_percentages = learnBot.get_candle_percentages(all_candles)

all_percentages_pos_neg = {}
for coin in all_percentages:
    all_percentages_pos_neg[coin] = learnBot.get_pos_neg(all_percentages[coin])

all_pos_neg_patterns = {}
for coin in all_percentages_pos_neg:
    all_pos_neg_patterns[coin] = learnBot.get_patterns(all_percentages_pos_neg[coin], minimum_occurrence=4, max_sequence_len=8, minimum_sequence_len=4, progress_tracker=True)

for coin in all_pos_neg_patterns:
    sorted_sequences = sorted(all_pos_neg_patterns[coin], key=lambda x: all_pos_neg_patterns[coin][x]['count'], reverse=True)
    for sequence in sorted_sequences:
        print("COIN:" + str(coin) + " SEQUENCE:" + str(sequence) + str(all_pos_neg_patterns[coin][sequence]))
