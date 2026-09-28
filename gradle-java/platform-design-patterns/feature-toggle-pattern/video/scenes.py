"""Scene definitions for the Feature Toggle teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Feature Toggle',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Feature Toggle pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A feature toggle puts a new '
            'feature into the released code, behind a switch. [[slnc '
            '300]] The switch is read while the program runs. [[slnc '
            '300]] So turning the feature on or off is a change of '
            'setting, not a new release. [[slnc 600]] Think of the light '
            'switches in a new house. [[slnc 300]] The wiring is all '
            'installed. [[slnc 300]] But each light only comes on when '
            'you flip its switch. [[slnc 700]] In our online store, gift '
            'wrap is ready. [[slnc 300]] But we want to try it on a few '
            'customers first, and turn it off at once if it goes wrong. '
            '[[slnc 500]] By the end, you will hear a feature that can '
            'only be released by redeploying. [[slnc 300]] The same '
            'feature shipped switched off, and turned on later. [[slnc '
            '300]] Turned on for some customers only. [[slnc 300]] A kill '
            'switch that stops failures. [[slnc 300]] A safe answer when '
            'the switches cannot be read. [[slnc 300]] And the bill.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Gift wrap adds 3 pounds', 'to an order.', '', 'It is coded, and has a bug', 'nobody has found.', '', 'We would like to try it on a', 'few customers first.', '', 'How do we switch it on?'],
        narration=(
            'Here is the scenario. [[slnc 400]] Gift wrap adds three '
            'pounds to an order. [[slnc 300]] It has been built. [[slnc '
            '300]] And it has a bug that nobody has found yet. [[slnc '
            '500]] We would like to try it on a few customers first. '
            '[[slnc 500]] So here is the question. [[slnc 300]] How do we '
            'switch it on?'
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
            'First demo: deploying is releasing. [[slnc 400]] Gift wrap '
            'goes live by releasing new code. [[slnc 300]] That is one '
            'release. [[slnc 500]] It has a bug, so taking it away needs '
            'another release. [[slnc 300]] That is two. [[slnc 500]] And '
            'each release also ships every other change waiting to go '
            'out. [[slnc 300]] Switching one feature drags everything '
            'else along with it.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Ship the feature switched off.', '', 'A table of switches is read', 'while the program runs.', '', 'Turning it on, for some or all,', 'or off again, is a change of', 'setting.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Ship the feature switched '
            'off. [[slnc 300]] A table of switches is read while the '
            'program runs. [[slnc 500]] Turning the feature on, for some '
            'customers or for everyone, is a change in that table. [[slnc '
            '300]] And so is turning it off again.'
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
            'Second demo: ship it dark, and switch it on later. [[slnc '
            '400]] Gift wrap is in the released code, but switched off. '
            '[[slnc 300]] An order of fifty pounds costs fifty pounds. '
            '[[slnc 500]] Then the switch is turned on in the table. '
            '[[slnc 300]] No release. [[slnc 300]] The same order now '
            'costs fifty-three pounds.'
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
            'Third demo: switch it on for some customers. [[slnc 400]] A '
            'ten percent rollout. [[slnc 300]] Out of a hundred '
            'customers, ten get gift wrap. [[slnc 500]] Then, only two '
            'named testers. [[slnc 300]] Out of a hundred customers, just '
            'those two get it.'
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
            'Fourth demo: the kill switch. [[slnc 400]] Gift wrap has its '
            'bug. [[slnc 300]] With twenty percent of customers switched '
            'on, twenty orders out of a hundred fail. [[slnc 500]] One '
            'change in the table turns it off. [[slnc 300]] Out of the '
            'next hundred orders, none fail. [[slnc 300]] And there was '
            'no release.'
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
            'Fifth demo: when the switch table cannot be read. [[slnc '
            '400]] With the table working, a fifty-pound order costs '
            'fifty-three, with gift wrap. [[slnc 500]] With the table '
            'down, it costs fifty. [[slnc 300]] The order still works. '
            '[[slnc 300]] Every feature simply falls back to off.'
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
            'Finally, the bill. [[slnc 400]] Five toggles make thirty-two '
            'possible combinations. [[slnc 300]] And the tests usually '
            'run just one of them. [[slnc 600]] And on day two hundred, '
            'three toggles have been fully on for more than ninety days. '
            '[[slnc 300]] They are still in the code: express shipping, '
            'gift wrap, and new search. [[slnc 300]] Each one is a branch '
            'in the code that nobody needs any more.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['if (flags.isEnabled("name", user))', 'in application code.', '', 'LaunchDarkly, Unleash, Flagsmith,', 'Togglz, or a homemade table.', '', 'A percentage rollout by user id.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for code that asks whether a named feature '
            'is enabled, for this user. [[slnc 300]] Look for services '
            'like LaunchDarkly, Unleash, or Flagsmith, or a homemade '
            'table of switches. [[slnc 300]] Look for a rollout by '
            'percentage of users. [[slnc 300]] Or a toggle named after an '
            'old ticket, still in the code a year later.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Ship features switched off, and', 'turn them on for a few, then more.', 'Keep a kill switch for anything', 'risky. Choose the safe answer for', 'when the table cannot be read. And', 'remove every toggle once it has', 'settled, because each one costs a', 'combination.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Ship features switched '
            'off. [[slnc 300]] Then turn them on for a few customers, and '
            'then more. [[slnc 500]] Keep a kill switch for anything '
            'risky. [[slnc 300]] Choose a safe answer for when the table '
            'cannot be read. [[slnc 500]] And remove every toggle once '
            'the decision is settled. [[slnc 300]] Because each one '
            'doubles the combinations to test.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 300]] "
            'Nothing depends on a real clock, so every run gives the same '
            'result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a change that is small and', 'safe, a plain release is simpler.', 'A toggle is a branch in your code', 'that must later be removed.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a small, safe '
            'change, a normal release is simpler. [[slnc 400]] A toggle '
            'is a branch in your code, and it must be removed later.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Feature Toggle pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A '
            'feature toggle turns a release into a setting, and gives you '
            'a kill switch, and the price is combinations to test, and '
            'old toggles to remove. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 300]] It runs offline, with '
            'nothing installed except a Java development kit. [[slnc '
            '500]] Here is one exercise to try. [[slnc 300]] Add a rule '
            'that turns gift wrap on for customers whose number is even. '
            '[[slnc 300]] And check that it works. [[slnc 500]] If this '
            'helped, a like really does help other people find it. [[slnc '
            "300]] And subscribe, if you'd like the rest of the series. "
            '[[slnc 400]] Thanks for watching.'
        ),
    ),
]
