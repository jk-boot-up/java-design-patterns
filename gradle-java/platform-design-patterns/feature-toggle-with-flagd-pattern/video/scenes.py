"""Scene definitions for the Feature Toggle with flagd teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Feature Toggle with flagd',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Feature Toggle '
            'pattern with flagd and OpenFeature, in Java, and it is '
            'written and presented by Jayasekhar Konduru. [[slnc 300]] It '
            'is the framework version of the Feature Toggle video. That '
            'one put gift wrap behind a table of switches read at run '
            'time. It showed the feature deployed dark, switched on for '
            'some customers, turned off by a kill switch, and safe when '
            'the table cannot be read. This one shows the same idea '
            'inside flagd and OpenFeature. [[slnc 350]] The plain '
            'definition, in short: with flagd, a flag is an entry in a '
            'file that a daemon watches. The application asks the daemon '
            'whether a flag is on for a customer. [[slnc 300]] By the end '
            'you will see a real flag daemon serve a flag that is off, '
            'see the file edited and the daemon notice by itself, see a '
            'rollout to a share of customers and to named testers, see a '
            'kill switch, see the checkout fall back when the daemon is '
            'stopped, and see the bill.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Feature Toggle, the hand-built', 'video, puts gift wrap behind a', 'table of switches.', '', 'It shows a dark deploy, a rollout,', 'a kill switch and a safe default.', '', 'If you have not seen it, start', 'there.'],
        narration=(
            'This video assumes the Feature Toggle video. If you have not '
            'seen it, start there. It puts gift wrap behind a table of '
            'switches, and shows a dark deploy, a rollout, a kill switch, '
            'and a safe default. [[slnc 300]] This one uses the same '
            'example. It does not teach the pattern again. It shows what '
            'flagd and OpenFeature does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Two things are new: flagd, and', 'Docker to run it.', '', 'You need Docker running. Without', 'it the demo says so and stops.', '', 'Skipping this video loses none of', 'the pattern.'],
        narration=(
            'Before the first line of code, what flagd and OpenFeature '
            'is. Open Feature is a standard way to ask whether a feature '
            'is on. Flagd is a small daemon that answers that question. '
            'It reads its flags from a file, notices when the file '
            'changes, and needs no restart. [[slnc 300]] And a promise: '
            'skipping this video loses none of the pattern. The '
            'hand-built one teaches all of it.'
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
            'First, deploying is releasing. Gift wrap goes live by '
            'deploying it: one deploy. It has a bug, so taking it away is '
            'another: two deploys. Each deploy ships every other change '
            'waiting in the branch too.'
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
            'Second, deploy dark, switch later. Gift wrap is in the '
            'deployed code, and flagd has it off. An order of five '
            'thousand costs five thousand. The flags file is edited, and '
            'flagd notices by itself: no deploy, no restart. The same '
            'order costs fifty three hundred.'
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
            'Third, switch on for some. A ten percent rollout, decided by '
            "flagd's own hash of the customer. Of a hundred customers, "
            'about a tenth got it. Then only two named testers: of a '
            'hundred customers, two got it.'
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
            'Fourth, the kill switch. Gift wrap has a bug. With twenty '
            'percent on, about a fifth of a hundred orders failed. One '
            'edit to the file turned it off. Of a hundred orders, none '
            'failed. No deploy.'
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
            'Fifth, when flagd cannot be reached. Flagd is up, and an '
            'order of five thousand costs fifty three hundred. Flagd is '
            'stopped, and it costs five thousand. The order still works, '
            'and every feature falls back to off.'
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
            'Last, the bill. A shop with five flags would have thirty two '
            'possible combinations. The tests usually run one. Flagd is '
            'another process to run and keep up, and every flag check is '
            'a network call: this demo made hundreds. And a flag that is '
            'settled and still in the file is an if that nobody needs. '
            'Flagd does not remove it for you.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Flags live outside the code.', '', 'Rollouts by hash stay repeatable.', '', 'Down means off.', '', 'Remove settled flags.'],
        narration=(
            'My verdict, plainly. Keep flags in a file or service that a '
            'daemon serves, and change them there, not in code. Rollouts '
            'by hash are repeatable, so the same customers stay in. '
            'Decide what happens when the daemon is down: off is the safe '
            'answer. And remove settled flags.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['A `flags.json` with `variants`,', '`defaultVariant` and `targeting`.', '', 'An OpenFeature client,', '`client.getBooleanValue(...)`.', '', 'A `fractional` rule for a', 'percentage rollout.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'flags.json with variants, defaultVariant and targeting. An '
            'OpenFeature client, client.getBooleanValue(...). A '
            'fractional rule for a percentage rollout.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Companies that use OpenFeature', 'with LaunchDarkly, Flagsmith,', 'Unleash or their own service.'],
        narration=(
            'You have met this in companies that use openfeature with '
            'launchdarkly, flagsmith, unleash or their own service.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['flagd latest, built September', 'tenth, twenty twenty six.', '', 'Docker 24 or later.'],
        narration=(
            'For the record. flagd, latest, built September tenth, twenty '
            'twenty six. Docker, 24 or later.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real flagd', 'in a container, a real file it', 'watches, and real HTTP calls.', '', "The rollout is by flagd's own", 'hash, so the same customers are', 'picked every run.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is real: a real flagd in a container, a real file '
            "it watches, and real HTTP calls. The rollout is by flagd's "
            'own hash, so the same customers are picked on every run.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a handful of switches that', 'change with each release, a', 'setting in the deployment is', 'enough. A daemon adds a process', 'and a network call to every check.'],
        narration=(
            'So when is it too much? For a handful of switches that '
            'change with each release, a setting in the deployment is '
            'enough. A daemon adds a process and a network call to every '
            'check.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a second flag for express shipping, and turn it on for the named testers..'],
        narration=(
            "That's Feature Toggle with flagd. [[slnc 250]] If you take "
            'one sentence away, take this one: a real flag daemon turns a '
            'file edit into a release, and the price is a process to run '
            'and a call for every check. [[slnc 350]] The full source, '
            'the written notes, the diagrams and an animated walkthrough '
            'are all in the repository. [[slnc 300]] If you try one '
            'exercise, add a second flag for express shipping, and turn '
            'it on for the named testers. [[slnc 300]] If this helped, a '
            'like genuinely does help other people find it, and subscribe '
            'if you would like the rest of the series. [[slnc 250]] '
            'Thanks for watching.'
        ),
    ),
]
