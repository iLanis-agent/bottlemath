#!/usr/bin/env python3
# Bottle Math oracle - mirrors engine.js float-for-float.
import json, math

def _fixed2(x):
    c = math.floor(x * 100 + 0.5)
    w, r = c // 100, c % 100
    return f"{w}.{r:02d}"

def _cents_word(dep):
    return "cent" if dep == 1 else "cents"

def _check_cans(cans):
    if not math.isfinite(cans) or cans < 0:
        raise ValueError("the can count must be zero or more")

def _check_deposit(dep):
    if not math.isfinite(dep) or dep <= 0:
        raise ValueError("the deposit must be more than 0 cents")

def bag_truth(cans, dep):
    _check_cans(cans); _check_deposit(dep)
    if cans == 0:
        return "No cans, no refund - the bag is just a bag."
    refund = cans * dep / 100
    can_word = "can" if cans == 1 else "cans"
    return f"{cans} {can_word} at {dep} {_cents_word(dep)} each bring back ${_fixed2(refund)}."

def trip_truth(cans, dep, trip_cost):
    _check_cans(cans); _check_deposit(dep)
    if not math.isfinite(trip_cost) or trip_cost < 0:
        raise ValueError("the trip cost must be zero or more")
    refund = cans * dep / 100
    margin = refund - trip_cost
    head = f"The cans bring back ${_fixed2(refund)} against a ${_fixed2(trip_cost)} trip - "
    if abs(margin) < 0.005:
        return head + "a wash, the trip costs exactly what the cans bring back."
    if margin > 0:
        return head + f"${_fixed2(margin)} ahead."
    return head + f"${_fixed2(-margin)} behind, the detour costs more than the cans bring back."

def stash_truth(rate, weeks, dep):
    _check_cans(rate); _check_deposit(dep)
    if not math.isfinite(weeks) or weeks < 1:
        raise ValueError("weeks must be at least 1")
    if rate == 0:
        return "Zero cans a week builds nothing - the garage stays clear."
    total = rate * weeks
    refund = total * dep / 100
    rate_word = "can" if rate == 1 else "cans"
    week_word = "week" if weeks == 1 else "weeks"
    total_word = "can" if total == 1 else "cans"
    return (f"{rate} {rate_word} a week for {weeks} {week_word} is {total} {total_word} - "
            f"${_fixed2(refund)} at the deposit, or a growing corner of the garage.")

CASES = [
    ("bagTruth", (87, 5)),
    ("bagTruth", (0, 5)),
    ("bagTruth", (24, 10)),
    ("bagTruth", (-3, 5)),
    ("bagTruth", (87, 0)),
    ("tripTruth", (87, 5, 3.00)),
    ("tripTruth", (20, 5, 2.65)),
    ("tripTruth", (50, 5, 2.50)),
    ("tripTruth", (87, 5, -1)),
    ("stashTruth", (15, 52, 5)),
    ("stashTruth", (1, 1, 10)),
    ("stashTruth", (15, 0, 5)),
]

FNS = {"bagTruth": bag_truth, "tripTruth": trip_truth, "stashTruth": stash_truth}

out = []
for name, args in CASES:
    try:
        expected = FNS[name](*args)
    except ValueError as e:
        expected = "ERR:" + str(e)
    out.append({"fn": name, "args": list(args), "expected": expected})

with open("expected.json", "w") as f:
    f.write(json.dumps(out, indent=2) + "\n")
print(f"{len(out)} cases written")
