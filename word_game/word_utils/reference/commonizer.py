import requests
from find_pangram import pangram_candidates

_wait = 0.5

def write_pangrams(pangrams, filename):
    with open(filename, "w+") as f:
        for p in pangrams:
            f.write(p + "\n")
            print(f"writing {p}")

def get_freq(term):
    response = None
    while True:
        try:
            response = requests.get('https://api.datamuse.com/words?sp='+term+'&md=f&max=1').json()
        except:
            print('Could not get response. Sleep and retry...')
            time.sleep(_wait)
            continue
        break;
    freq = 0.0 if len(response)==0 else float(response[0]['tags'][0][2:])
    return freq

def write_commons():
    write_pangrams(common_pangrams(), "common_pangrams.txt")

def common_pangrams():
    pangrams = []
    with open("all_pangrams.txt", "r") as f:
        pangrams = f.read().splitlines()
    for p in pangrams:
        if get_freq(p) > 0.05:
            yield p
            print(f"yielding {p}")
