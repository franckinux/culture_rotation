import argparse
import itertools
import json
# from pprint import pprint


def score(ok, nok, t):
    s = 0
    for i in range(len(t) - 1):
        c = t[i:i + 2]
        if c in ok or (c[1], c[0]) in ok:
            s += 1
        if c in nok:
            return -1
    return s


def rotate(t: tuple) -> tuple:
    return (t[-1],) + t[0:-1]


def main(garden, groups, associations):
    # remove not cultivated vegetables from groups
    new_groups = {}
    for k, v in groups.items():
        new_groups[k] = set(v) & set(garden)

    # compute distinct root permutations of groups
    groups_keys = tuple(groups.keys())
    partial_permutations = itertools.permutations(groups_keys[1:])
    groups_key_permutations = ((groups_keys[0],) + p for p in partial_permutations)

    ok = tuple(tuple(sub) for sub in associations["ok"])
    nok = tuple(tuple(sub) for sub in associations["nok"])

    for group_key_permutation in tuple(groups_key_permutations):
        max_sum = 0

        for _ in range(len(group_key_permutation)):

            groups_values_permutations = {}
            for gk in groups_keys:
                groups_values_permutations[gk] = itertools.permutations(new_groups[gk])

            max = 0
            gkps = (groups_values_permutations[gkp] for gkp in group_key_permutation)
            for l in itertools.product(*gkps):
                t = tuple(itertools.chain(*l))
                s = score(ok, nok, t)
                if s > max:
                    max = s
                    r = t
            print(f"{r} {max}")

            max_sum += max

            group_key_permutation = rotate(group_key_permutation)

        print(f"{max_sum}")
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("garden")
    parser.add_argument("groups")
    parser.add_argument("associations")
    args = parser.parse_args()

    with open(args.garden) as f:
        garden = json.loads(f.read())

    with open(args.groups) as f:
        groups = json.loads(f.read())

    with open(args.associations) as f:
        associations = json.loads(f.read())

        main(garden, groups, associations)
