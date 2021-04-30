import argparse
import itertools
import json
from pprint import pprint


def score(ok, nok, t):
    s = 0
    for i in range(len(t) - 1):
        c = t[i:i + 2]
        if c in ok:
            s += 1
        if c in nok:
            return -1
    return s


def main(content):
    permutations = itertools.permutations(content["carres"][1:])
    seeds = ((content["carres"][0],) + p for p in permutations)
    # pprint(tuple(seeds))

    cultures = {}
    for c in content["carres"]:
        cultures[c] = itertools.permutations(content["cultures"][c])

    ok = tuple(tuple(sub) for sub in content["ok"])
    nok = tuple(tuple(sub) for sub in content["nok"])
    max = 0
    for l in itertools.product(*cultures.values()):
        t = tuple(itertools.chain(*l))
        s = score(ok, nok, t)
        if s > max:
            max = s
            r = t
        # print(f"{t} {s}")
    # print("-----------")
    print(f"{r} {max}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    with open(args.filename) as f:
        lines = f.read()
        content = json.loads(lines)
        main(content)
