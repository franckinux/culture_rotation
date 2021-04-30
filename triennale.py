import argparse
import itertools
import json
from pprint import pprint


nexts = {}


def what_nexts(carres: list) -> list:
    global nexts

    nexts = {}
    lg = len(carres)
    for i in range(lg):
        c = carres[i]
        if i == lg - 1:
            nexts[c] = carres[0]
        else:
            nexts[c] = carres[i + 1]
    return nexts


def next(carre: list) -> list:
    global nexts
    return [nexts[c] for c in carre]


def is_permutation_of(s: list, d: list) -> bool:
    global nexts
    for _ in range(len(nexts)):
        if d == s:
            return True
        s = next(s)
    return False


def main(content):
    global nexts
    nexts = what_nexts(content["carres"])

    permutations = [list(tup) for tup in itertools.permutations(content["carres"])]

    groups = [[permutations[0]]]
    for i in range(1, len(permutations)):
        for g in groups:
            if is_permutation_of(g[0], permutations[i]):
                g.append(permutations[i])
                break
        else:
            groups.append([permutations[i]])

    seeds1 = [g[0] for g in groups]
    pprint(seeds1)
    print(len(seeds1))

    permutations = [list(tup) for tup in itertools.permutations(content["carres"][1:])]
    seeds2 = [[content["carres"][0]] + p for p in permutations]
    pprint(seeds2)
    print(len(seeds2))

    print(seeds1 == seeds2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    with open(args.filename) as f:
        lines = f.read()
        content = json.loads(lines)
        main(content)
