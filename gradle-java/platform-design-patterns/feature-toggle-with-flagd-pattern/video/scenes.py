"""Scene definitions for the Feature Toggle with flagd teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Feature Toggle with flagd',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Feature Toggle pattern in Java, using two tools: flagd and '
            'OpenFeature. [[slnc 300]] This video is presented by '
            'Jayasekhar Konduru. [[slnc 600]] First, a simple definition. '
            '[[slnc 300]] A feature toggle puts a new feature into the '
            'released code, behind a switch that is read while the '
            'program runs. [[slnc 300]] So turning it on or off is a '
            'change of setting, not a new release. [[slnc 600]] With '
            'flagd, each switch, called a flag, is an entry in a file. '
            '[[slnc 300]] A small background program watches that file. '
            '[[slnc 300]] And the shop asks it whether a flag is on, for '
            'a given customer. [[slnc 700]] In our online store, the '
            'feature is gift wrap. [[slnc 500]] By the end, you will hear '
            'a real flag program serve a flag that is off. [[slnc 300]] '
            'The file edited, and the change noticed by itself. [[slnc '
            '300]] A rollout to some customers. [[slnc 300]] A kill '
            'switch. [[slnc 300]] The checkout falling back when the flag '
            'program stops. [[slnc 300]] And the bill.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Feature Toggle, the hand-built', 'video, puts gift wrap behind a', 'table of switches.', '', 'It shows a dark deploy, a rollout,', 'a kill switch and a safe default.', '', 'If you have not seen it, start', 'there.'],
        narration=(
            'This video builds on the plain Java Feature Toggle video. '
            '[[slnc 300]] If you have not seen it, start there. [[slnc '
            '500]] That video puts gift wrap behind a table of switches. '
            '[[slnc 300]] It shows the feature shipped switched off, a '
            'rollout, a kill switch, and a safe default. [[slnc 500]] '
            'This video uses the same example. [[slnc 300]] It does not '
            'teach the pattern again. [[slnc 300]] It shows what flagd '
            'and OpenFeature do with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Two things are new: flagd, and', 'Docker to run it.', '', 'You need Docker running. Without', 'it the demo says so and stops.', '', 'Skipping this video loses none of', 'the pattern.'],
        narration=(
            'Before any code, what are these two tools? [[slnc 400]] '
            'OpenFeature is a standard way for code to ask whether a '
            'feature is on. [[slnc 500]] flagd is a small background '
            'program that answers that question. [[slnc 300]] It reads '
            'its flags from a file. [[slnc 300]] It notices when the file '
            'changes. [[slnc 300]] And it needs no restart. [[slnc 500]] '
            'You need Docker running to try it. [[slnc 300]] Without '
            'Docker, the demo says so, and stops. [[slnc 500]] And a '
            'promise. [[slnc 300]] Skipping this video loses none of the '
            'pattern. [[slnc 300]] The plain Java video teaches all of '
            'it.'
        ),
    ),
    dict(
        key='04-deploy', kind='console', title='Deploying Is Releasing',
        body="""ONE. Deploying is releasing.
  gift wrap live: 1 deploy.
  a bug, taking it away: another.
  2 deploys.

  each deploy ships every other
  change too.""",
        narration=(
            'First demo: releasing by redeploying. [[slnc 400]] Gift wrap '
            'goes live by releasing new code. [[slnc 300]] That is one '
            'release. [[slnc 500]] It has a bug, so taking it away needs '
            'another release. [[slnc 300]] That is two. [[slnc 500]] And '
            'each release also ships every other change that is waiting.'
        ),
    ),
    dict(
        key='05-dark', kind='console', title='Deploy Dark, Switch Later',
        body="""TWO. Deploy dark.
  gift wrap is in the code, and
  flagd has it off: 5000.
  the file is edited; flagd
  notices. no deploy, no restart:
  5300.""",
        narration=(
            'Second demo: ship it switched off, and turn it on later. '
            '[[slnc 400]] Gift wrap is in the released code, and flagd '
            'has it switched off. [[slnc 300]] A fifty-pound order costs '
            'fifty pounds. [[slnc 500]] Then the flags file is edited. '
            '[[slnc 300]] And flagd notices by itself. [[slnc 300]] No '
            'release, and no restart. [[slnc 300]] The same order now '
            'costs fifty-three pounds, with gift wrap.'
        ),
    ),
    dict(
        key='06-some', kind='console', title='Switch On For Some',
        body="""THREE. On for some.
  a 10 percent rollout, by flagd's
  own hash: about a tenth of 100.
  two named testers:
  2 of 100.""",
        narration=(
            'Third demo: switch it on for some customers. [[slnc 400]] A '
            'ten percent rollout. [[slnc 300]] flagd decides who is in by '
            "scrambling each customer's number in a fixed way. [[slnc "
            '300]] Out of a hundred customers, about ten get it. [[slnc '
            '500]] Then, only two named testers. [[slnc 300]] Out of a '
            'hundred customers, just those two get it.'
        ),
    ),
    dict(
        key='07-kill', kind='console', title='The Kill Switch',
        body="""FOUR. The kill switch.
  gift wrap has a bug.
  20 percent on: about a fifth
  of 100 orders failed.
  one edit turned it off:
  0 failed. no deploy.""",
        narration=(
            'Fourth demo: the kill switch. [[slnc 400]] Gift wrap has a '
            'bug. [[slnc 300]] With twenty percent switched on, about a '
            'fifth of a hundred orders fail. [[slnc 500]] One edit to the '
            'file turns it off. [[slnc 300]] Out of the next hundred '
            'orders, none fail. [[slnc 300]] No release.'
        ),
    ),
    dict(
        key='08-down', kind='console', title='When flagd Cannot Be Reached',
        body="""FIVE. flagd is down.
  flagd up: 5300.
  flagd stopped: 5000.

  the order still works, and every
  feature falls back to off.""",
        narration=(
            'Fifth demo: when flagd cannot be reached. [[slnc 400]] With '
            'flagd running, a fifty-pound order costs fifty-three. [[slnc '
            '500]] With flagd stopped, it costs fifty. [[slnc 300]] The '
            'order still works. [[slnc 300]] Every feature simply falls '
            'back to off.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  5 flags: 32 combinations.
  the tests run one.

  flagd is a process to keep up;
  every check is a network call.

  a settled flag stays in the file,
  an if nobody needs.""",
        narration=(
            'Finally, the bill. [[slnc 400]] A shop with five flags has '
            'thirty-two possible combinations. [[slnc 300]] And the tests '
            'usually run just one. [[slnc 600]] flagd is one more program '
            'to run and keep up. [[slnc 300]] And every flag check is a '
            'network call. [[slnc 300]] This demo made hundreds of them. '
            '[[slnc 600]] And a flag that is settled, but still in the '
            'file, is a branch in the code nobody needs. [[slnc 300]] '
            'flagd will not remove it for you.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Flags live outside the code.', '', 'Rollouts by hash stay repeatable.', '', 'Down means off.', '', 'Remove settled flags.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Keep flags in a file '
            'or service, served by a program like flagd. [[slnc 300]] And '
            'change them there, not in the code. [[slnc 500]] Percentage '
            'rollouts by a fixed scramble are repeatable, so the same '
            'customers stay in. [[slnc 300]] Decide what happens when '
            'flagd is down: off is the safe answer. [[slnc 300]] And '
            'remove flags once they are settled.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['A `flags.json` with `variants`,', '`defaultVariant` and `targeting`.', '', 'An OpenFeature client,', '`client.getBooleanValue(...)`.', '', 'A `fractional` rule for a', 'percentage rollout.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            "400]] Look for a flags file listing each flag's options, its "
            'default, and its targeting rules. [[slnc 300]] Look for an '
            "OpenFeature client that asks for a flag's value. [[slnc "
            '300]] Or a fractional rule, used for a percentage rollout.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Companies that use OpenFeature', 'with LaunchDarkly, Flagsmith,', 'Unleash or their own service.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In companies '
            'that use OpenFeature with services like LaunchDarkly, '
            'Flagsmith, Unleash, or their own flag service.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['flagd latest, built September', 'tenth, twenty twenty six.', '', 'Docker 24 or later.'],
        narration=(
            'For the record, here is what was used. [[slnc 300]] The '
            'latest flagd release, built on the tenth of September, '
            'twenty twenty-six. [[slnc 300]] And Docker, version '
            'twenty-four or later.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real flagd', 'in a container, a real file it', 'watches, and real HTTP calls.', '', "The rollout is by flagd's own", 'hash, so the same customers are', 'picked every run.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is real: a real flagd in a container, a real file '
            'it watches, and real web requests. [[slnc 300]] The rollout '
            "uses flagd's own fixed scramble. [[slnc 300]] So the same "
            'customers are picked on every run.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a handful of switches that', 'change with each release, a', 'setting in the deployment is', 'enough. A daemon adds a process', 'and a network call to every check.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a handful of '
            'switches that change with each release, a setting in the '
            'release itself is enough. [[slnc 400]] A flag program adds a '
            'process to run, and a network call to every check.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a second flag for express shipping, and turn it on for the named testers..'],
        narration=(
            "That's Feature Toggle, with flagd. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A real '
            'flag program turns a file edit into a release, and the price '
            'is one more process to run, and a network call for every '
            'check. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Add a second flag, for express shipping. [[slnc 300]] '
            'And turn it on for the two named testers. [[slnc 500]] If '
            'this helped, a like really does help other people find it. '
            "[[slnc 300]] And subscribe, if you'd like the rest of the "
            'series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
