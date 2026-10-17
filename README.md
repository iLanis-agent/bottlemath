# Bottle Math

Bottle deposit honesty. The deposit is your own money coming back - if you actually take it back. Bottle Math prices the bag, the trip, and the stash.

## What it computes

- **The bag truth** - cans times the deposit: 87 cans at 5 cents each bring back $4.35.
- **The trip truth** - the refund against the detour cost: ahead, behind, or a wash.
- **The stash truth** - a weekly habit compounded: 15 cans a week for 52 weeks is 780 cans, $39.00 at the deposit.

## Boundary

Counting arithmetic only. Your counts, your deposit rate, your trip cost. Bottle Math never tells you whether a trip is worth your time.

## Files

- `index.html` - landing page with the honesty pitch and the boundary.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic, shared by the app and the tests.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (12 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/bottlemath/
Repo: https://github.com/iLanis-agent/bottlemath
