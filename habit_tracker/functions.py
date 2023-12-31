import random, string
import time
from manage import logger

encoding_dict = dict()
decoding_dict = dict()

alphabet = list(string.ascii_lowercase)

for i in range(10):
    encoding_dict[str(i)] = ''
    for j in range(25):
        if j % 2 == 0:
            encoding_dict[str(i)] += (random.choice(alphabet))
        else:
            encoding_dict[str(i)] += str(random.randint(0, 9))
    decoding_dict[encoding_dict[str(i)]] = str(i)

logger.critical(encoding_dict, decoding_dict)


def encode(user_id):
    encoded_id = ''
    for n in str(user_id):
        encoded_id += encoding_dict[n]
    return encoded_id


def decode(encoded_id):
    decoded_id = ''
    t = 0
    while t + 25 <= len(encoded_id):
        encoded_number = encoded_id[t:t + 25]
        decoded_id += decoding_dict[encoded_number]
        t += 25

    return int(decoded_id)


def get_time(for_url=False):
    current_time = time.localtime()
    if not for_url:
        current_date = f'{current_time.tm_mday}/{current_time.tm_mon}/{str(current_time.tm_year)[2:]}'
    else:
        current_date = f'{current_time.tm_mday}_{current_time.tm_mon}_{str(current_time.tm_year)[2:]}'
    return current_date


logger.critical(encode(11))
