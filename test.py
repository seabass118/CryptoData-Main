import learnBot
import shrimpy


public_key = '1930af65a9e42525a057c14cd816b0d582df36a3ac4e39c850294666185c5d91'
secret_key = 'b480b278b729cf73d203a2816fa1765cd26845d106181ba62f897e4547ca7ec5e2f90375a65f2f0596c0434e875ae0f0c02954e1bfde72401ed59e3822af0529'
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
