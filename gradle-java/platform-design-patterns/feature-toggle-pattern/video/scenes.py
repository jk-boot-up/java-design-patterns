"""Scene definitions for the Feature Toggle teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Feature Toggle',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Feature Toggle '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: a '
            'feature toggle puts a new feature in the deployed code, '
            'behind a switch that is read while the program runs. Turning '
            'it on or off is then a change of a setting, and not a new '
            'release. [[slnc 350]] This is another project in the '
            'platform category, whose subject is how software is shipped, '
            'run and operated. In our online store, gift wrap is ready, '
            'but we want to turn it on for a few customers first, and off '
            'again at once if it goes wrong. [[slnc 300]] By the end you '
            'will see a feature that can only be released by deploying, '
            'see a feature deployed dark and switched on later, see it '
            'switched on for some customers, see a kill switch stop '
            'failures, see the safe answer when the switch table is down, '
            'and see the bill, which is combinations and old switches.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Gift wrap adds 3 pounds', 'to an order.', '', 'It is coded, and has a bug', 'nobody has found.', '', 'We would like to try it on a', 'few customers first.', '', 'How do we switch it on?'],
        narration=(
            'Here is the scenario. Gift wrap adds three pounds to an '
            'order. It has been coded, and it has a bug that nobody has '
            'found yet. We would like to try it on a few customers first. '
            '[[slnc 300]] The question: how do we switch it on?'
        ),
    ),
    dict(
        key='03-deploy', kind='console', title='Deploying Is Releasing',
        body="""ONE. Deploying is releasing.
  gift wrap live: 1 deploy.
  a bug, taking it away:
  another. 2 deploys.

  each deploy ships every other
  change in the branch too.""",
        narration=(
            'First, deploying is releasing. Gift wrap goes live by '
            'deploying it: one deploy. It has a bug, so taking it away is '
            'another: two deploys. Each deploy ships every other change '
            'waiting in the branch too. The wish to switch one thing '
            'carries everything else with it.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Ship the feature switched off.', '', 'A table of switches is read', 'while the program runs.', '', 'Turning it on, for some or all,', 'or off again, is a change of', 'setting.'],
        narration=(
            'The pattern. Ship the feature switched off. A table of '
            'switches is read while the program runs. Turning the feature '
            'on, for some customers or all, or off again, is a change of '
            'setting.'
        ),
    ),
    dict(
        key='05-dark', kind='console', title='Deploy Dark, Switch Later',
        body="""TWO. Deploy dark.
  gift wrap is in the code,
  switched off: 5000.
  switch on in the table,
  no deploy: 5300.""",
        narration=(
            'Second, deploy dark, switch later. Gift wrap is in the '
            'deployed code, switched off. An order of five thousand costs '
            'five thousand. The switch is turned on in the table, with no '
            'deploy. The same order costs fifty three hundred.'
        ),
    ),
    dict(
        key='06-some', kind='console', title='Switch On For Some',
        body="""THREE. On for some.
  10 percent rollout:
  10 of 100 customers.
  two named testers:
  2 of 100.""",
        narration=(
            'Third, switch on for some. A ten percent rollout: of a '
            'hundred customers, ten got it. Then only two named testers: '
            'of a hundred customers, two got it.'
        ),
    ),
    dict(
        key='07-kill', kind='console', title='The Kill Switch',
        body="""FOUR. The kill switch.
  gift wrap has a bug.
  20 percent on: 20 orders fail.
  one change in the table:
  0 fail. no deploy.""",
        narration=(
            'Fourth, the kill switch. Gift wrap has a bug. With twenty '
            'percent on, of a hundred orders, twenty failed. One change '
            'in the table turned it off. Of a hundred orders, none '
            'failed. No deploy.'
        ),
    ),
    dict(
        key='08-down', kind='console', title='When The Table Cannot Be Read',
        body="""FIVE. Table down.
  table up: 5300.
  table down: 5000.

  the order still works, and
  every feature falls back to
  off.""",
        narration=(
            'Fifth, when the table cannot be read. The table is up, and '
            'an order of five thousand costs fifty three hundred. The '
            'table is down, and it costs five thousand. The order still '
            'works, and every feature falls back to off.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  5 toggles: 32 combinations.
  the tests run one.

  day 200: settled for 90 days,
  still in the code:
  express-shipping, gift-wrap,
  new-search.

  each is an if nobody needs.""",
        narration=(
            'Last, the bill. Five toggles make thirty two possible '
            'combinations. The tests usually run one. And on day two '
            'hundred, three toggles have been settled for over ninety '
            'days, and are still in the code: express shipping, gift '
            'wrap, and new search. Every one is an if that nobody needs.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['if (flags.isEnabled("name", user))', 'in application code.', '', 'LaunchDarkly, Unleash, Flagsmith,', 'Togglz, or a homemade table.', '', 'A percentage rollout by user id.'],
        narration=(
            'How do you recognise this in code you did not write? if '
            '(flags.isEnabled("name", user)) in application code. '
            'LaunchDarkly, Unleash, Flagsmith, Togglz, or a homemade '
            'table. A percentage rollout by user id. A toggle named after '
            'a ticket, still in the code a year later.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Ship features switched off, and', 'turn them on for a few, then more.', 'Keep a kill switch for anything', 'risky. Choose the safe answer for', 'when the table cannot be read. And', 'remove every toggle once it has', 'settled, because each one costs a', 'combination.'],
        narration=(
            'Here is my verdict, plainly. Ship features switched off, and '
            'turn them on for a few, then more. Keep a kill switch for '
            'anything risky. Choose the safe answer for when the table '
            'cannot be read. And remove every toggle once it has settled, '
            'because each one costs a combination.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is plain Java. Every number quoted comes from '
            "this program's own output. Nothing depends on a clock, so "
            'every run is the same.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a change that is small and', 'safe, a plain release is simpler.', 'A toggle is a branch in your code', 'that must later be removed.'],
        narration=(
            'So when is it too much? For a change that is small and safe, '
            'a plain release is simpler. A toggle is a branch in your '
            'code that must later be removed.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Feature Toggle. [[slnc 250]] If you take one sentence "
            'away, take this one: a feature toggle turns release into a '
            'setting and gives you a kill switch, and the price is '
            'combinations to test and old toggles to remove. [[slnc 350]] '
            'The full source, the written notes, the diagrams and an '
            'animated walkthrough are all in the repository, running '
            'offline with nothing installed but a Java development kit. '
            '[[slnc 300]] If you try one exercise, add a rule that '
            'switches gift wrap on for customers whose number is even, '
            'and check it. [[slnc 300]] If this helped, a like genuinely '
            'does help other people find it, and subscribe if you would '
            'like the rest of the series. [[slnc 250]] Thanks for '
            'watching.'
        ),
    ),
]
