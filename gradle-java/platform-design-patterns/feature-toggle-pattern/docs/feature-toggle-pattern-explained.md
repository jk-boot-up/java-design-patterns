# Feature Toggle, Explained

## The pattern in one sentence

A feature toggle puts a new feature in the deployed code behind a switch that is read at run time, so that turning it on or off is a change of setting, not a new release.

## The six acts

### Deploying Is Releasing

Gift wrap goes live by deploying it: one deploy. It has a bug, so taking it away is another: two deploys. Each deploy ships every other change waiting in the branch too. The wish to switch one thing carries everything else with it.

```
  gift wrap goes live by deploying it: 1 deploy. it has a bug, so taking it away is another: 2 deploys.
  each deploy ships every other change waiting in the branch too, so the wish to switch one thing carries everything else with it.
```

### Deploy Dark, Switch Later

Gift wrap is in the deployed code, switched off. An order of five thousand costs five thousand. The switch is turned on in the table, with no deploy. The same order costs fifty three hundred.

```
  gift wrap is in the deployed code, switched off. an order of 5000 costs: 5000.
  the switch is turned on in the table. no deploy. the same order costs: 5300.
```

### Switch On For Some

A ten percent rollout: of a hundred customers, ten got it. Then only two named testers: of a hundred customers, two got it.

```
  10 percent rollout. of 100 customers, got it: 10.
  only two named testers. of 100 customers, got it: 2.
```

### The Kill Switch

Gift wrap has a bug. With twenty percent on, of a hundred orders, twenty failed. One change in the table turned it off. Of a hundred orders, none failed. No deploy.

```
  gift wrap has a bug. with 20 percent on, of 100 orders, failed: 20.
  one change in the table turned it off. of 100 orders, failed: 0. no deploy.
```

### When The Table Cannot Be Read

The table is up, and an order of five thousand costs fifty three hundred. The table is down, and it costs five thousand. The order still works, and every feature falls back to off.

```
  the table is up. an order of 5000: 5300.
  the table is down. an order of 5000: 5000. the order still works, and every feature falls back to off.
```

### The Bill

Five toggles make thirty two possible combinations. The tests usually run one. And on day two hundred, three toggles have been settled for over ninety days and are still in the code: express shipping, gift wrap and new search. Every one is an if that nobody needs.

```
  5 toggles make 32 possible combinations. the tests usually run one.
  on day 200, settled for over 90 days and still in the code: [express-shipping, gift-wrap, new-search]. every one is an if that nobody needs.
```

## The verdict

Ship features switched off, and turn them on for a few, then more. Keep a kill switch for anything risky. Choose the safe answer for when the table cannot be read. And remove every toggle once it has settled, because each one costs a combination.

## How to recognise this in code you did not write

- `if (flags.isEnabled("name", user))` in application code.
- LaunchDarkly, Unleash, Flagsmith, Togglz, or a homemade table.
- A percentage rollout by user id.
- A toggle named after a ticket, still in the code a year later.

## Where you have already met this

Every large web company's releases, and the way trunk-based development keeps unfinished work out of sight.

## When this is too much

For a change that is small and safe, a plain release is simpler. A toggle is a branch in your code that must later be removed.
