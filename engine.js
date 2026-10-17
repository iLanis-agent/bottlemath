// Bottle Math engine - bottle deposit honesty.
// Mirrored float-for-float by oracle.py; keep the op order identical.

function _fixed2(x) {
  var c = Math.floor(x * 100 + 0.5);
  var w = Math.floor(c / 100), r = c - w * 100;
  return w + "." + (r < 10 ? "0" + r : "" + r);
}

function _centsWord(dep) { return dep === 1 ? "cent" : "cents"; }

function _checkCans(cans) {
  if (!isFinite(cans) || cans < 0) throw new Error("the can count must be zero or more");
}
function _checkDeposit(dep) {
  if (!isFinite(dep) || dep <= 0) throw new Error("the deposit must be more than 0 cents");
}

// The bag truth: what the cans actually bring back.
function bagTruth(cans, depositCents) {
  _checkCans(cans); _checkDeposit(depositCents);
  if (cans === 0) return "No cans, no refund - the bag is just a bag.";
  var refund = cans * depositCents / 100;
  var canWord = cans === 1 ? "can" : "cans";
  return cans + " " + canWord + " at " + depositCents + " " + _centsWord(depositCents) +
    " each bring back $" + _fixed2(refund) + ".";
}

// The trip truth: the refund against what the detour costs you.
function tripTruth(cans, depositCents, tripCostDollars) {
  _checkCans(cans); _checkDeposit(depositCents);
  if (!isFinite(tripCostDollars) || tripCostDollars < 0) throw new Error("the trip cost must be zero or more");
  var refund = cans * depositCents / 100;
  var margin = refund - tripCostDollars;
  var head = "The cans bring back $" + _fixed2(refund) + " against a $" + _fixed2(tripCostDollars) + " trip - ";
  if (Math.abs(margin) < 0.005) {
    return head + "a wash, the trip costs exactly what the cans bring back.";
  }
  if (margin > 0) {
    return head + "$" + _fixed2(margin) + " ahead.";
  }
  return head + "$" + _fixed2(-margin) + " behind, the detour costs more than the cans bring back.";
}

// The stash truth: what a habit builds into.
function stashTruth(cansPerWeek, weeks, depositCents) {
  _checkCans(cansPerWeek); _checkDeposit(depositCents);
  if (!isFinite(weeks) || weeks < 1) throw new Error("weeks must be at least 1");
  if (cansPerWeek === 0) return "Zero cans a week builds nothing - the garage stays clear.";
  var total = cansPerWeek * weeks;
  var refund = total * depositCents / 100;
  var rateWord = cansPerWeek === 1 ? "can" : "cans";
  var weekWord = weeks === 1 ? "week" : "weeks";
  var totalWord = total === 1 ? "can" : "cans";
  return cansPerWeek + " " + rateWord + " a week for " + weeks + " " + weekWord + " is " +
    total + " " + totalWord + " - $" + _fixed2(refund) + " at the deposit, or a growing corner of the garage.";
}
