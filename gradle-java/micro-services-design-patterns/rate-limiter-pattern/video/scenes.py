"""Scene definitions for the Rate Limiter teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Rate Limiter',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Rate Limiter pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A rate limiter refuses '
            'requests beyond an agreed rate. [[slnc 300]] So one caller '
            'cannot use up a service that everyone shares. [[slnc 300]] '
            'It says no early, so the service does not fail later. [[slnc '
            '600]] Think of a nightclub with a door attendant. [[slnc '
            '300]] Only so many people are let in each minute. [[slnc '
            '300]] The rest are told to wait, before the room gets '
            'dangerously full. [[slnc 700]] In our online store, the '
            'thing that can be overwhelmed is the product search. [[slnc '
            '500]] By the end, you will hear a thousand requests reach a '
            'search that can serve a hundred. [[slnc 300]] A bucket of '
            'tokens allow a burst, and then a steady rate. [[slnc 300]] A '
            'separate bucket for each caller protect a polite caller from '
            'a greedy one. [[slnc 300]] A refusal that says exactly when '
            'to come back. [[slnc 300]] And the bill.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The product search can serve 100', 'requests a second.', '', 'A script sends 1000 in a second.', '', 'Everyone else waits behind it.', '', 'What should the search do?'],
        narration=(
            'Here is the scenario. [[slnc 400]] The product search can '
            'serve a hundred requests a second. [[slnc 300]] One client, '
            'perhaps a script, sends a thousand in a single second. '
            '[[slnc 300]] And every other customer waits behind it. '
            '[[slnc 500]] So here is the question. [[slnc 300]] What '
            'should the search do about the other nine hundred?'
        ),
    ),
    dict(
        key='03-none', kind='console', title='No Limit',
        body="""ONE. No limit.
  the search serves 100 a second.
  a client sends 1000.
  accepted: 1000.
  over capacity: 900.""",
        narration=(
            'First demo: no limit. [[slnc 400]] The search can serve a '
            'hundred requests a second. [[slnc 300]] One client sends a '
            'thousand. [[slnc 500]] All thousand are accepted. [[slnc '
            '300]] Nine hundred of them are more than the search can '
            'serve. [[slnc 300]] And every other customer waits behind '
            'them.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A bucket holds tokens.', '', 'Each request takes one.', '', 'The bucket refills at a steady', 'rate, up to its size.', '', 'No token: refused, at once,', 'and told when to come back.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Picture a bucket that holds '
            'tokens. [[slnc 300]] Each request takes one token. [[slnc '
            '500]] The bucket refills at a steady rate, up to its size, '
            'and no further. [[slnc 500]] If there is no token left, the '
            'request is refused, straight away. [[slnc 300]] And it is '
            'told when to come back.'
        ),
    ),
    dict(
        key='05-bucket', kind='console', title='A Bucket Of Tokens',
        body="""TWO. A bucket.
  10 tokens, 5 a second.
  burst of 20: 10 allowed.
  1 second later: 5.
  10 quiet seconds: full,
  and no more than full:
  10.""",
        narration=(
            'Second demo: a bucket of tokens. [[slnc 400]] The bucket '
            'holds ten tokens, and refills at five per second. [[slnc '
            '600]] A burst of twenty requests arrives at once. [[slnc '
            '300]] Ten are allowed, and ten are refused. [[slnc 500]] One '
            'second later, another twenty arrive. [[slnc 300]] Five are '
            'allowed: the five tokens that refilled. [[slnc 500]] After '
            'ten quiet seconds, the bucket is full again. [[slnc 300]] '
            'But no fuller than ten.'
        ),
    ),
    dict(
        key='06-steady', kind='console', title='A Steady Rate Always Gets Through',
        body="""THREE. Steady.
  5 a second for a minute:
  300 of 300 allowed.

  bursts up to the bucket size.
  sustained above the refill:
  refused.""",
        narration=(
            'Third demo: a steady rate always gets through. [[slnc 400]] '
            'Five requests a second, evenly spaced, for a whole minute. '
            '[[slnc 300]] All three hundred are allowed. [[slnc 500]] A '
            'well-behaved client never notices the limiter. [[slnc 300]] '
            'A short burst is allowed, up to the size of the bucket. '
            '[[slnc 300]] But a rate that stays above the refill rate is '
            'not.'
        ),
    ),
    dict(
        key='07-fair', kind='console', title='One Bucket For Everyone, Or One Each',
        body="""FOUR. Fairness.
  one shared bucket: greedy
  takes 10, polite refused.

  a bucket each: greedy held
  to 10 of 20, polite allowed.""",
        narration=(
            'Fourth demo: one bucket for everyone, or one each. [[slnc '
            '400]] With a single shared bucket, a greedy client takes all '
            'ten tokens. [[slnc 300]] And a polite client is refused. '
            '[[slnc 300]] That is not protection. [[slnc 300]] It is just '
            'a different outage. [[slnc 600]] With a bucket for each '
            'caller, the greedy client is held to ten. [[slnc 300]] And '
            'the polite client is allowed through.'
        ),
    ),
    dict(
        key='08-retry', kind='console', title='Say When To Come Back',
        body="""FIVE. When to return.
  empty: retry after 1000 ms.
  1 ms early: refused.
  at that moment: allowed.

  no guessing, no hammering.""",
        narration=(
            'Fifth demo: say when to come back. [[slnc 400]] The bucket '
            'is empty. [[slnc 300]] The refusal says: try again in one '
            'second. [[slnc 500]] One millisecond too early, and the '
            'request is refused. [[slnc 300]] At exactly the time it '
            'said, it is allowed. [[slnc 500]] The client does not have '
            'to guess. [[slnc 300]] And it does not keep hammering the '
            'service.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  3 servers, a bucket each:
  30 allowed, not 10.

  10000 callers: 10000 buckets.

  a page loading 12 things:
  gets 10.""",
        narration=(
            'Finally, the bill. [[slnc 400]] Three servers, each with its '
            'own bucket, allow thirty requests, not ten. [[slnc 300]] So '
            'the limit is three times looser than it says. [[slnc 500]] '
            'Ten thousand callers means ten thousand buckets in memory. '
            '[[slnc 500]] And a real web page that loads twelve things at '
            'once only gets ten. [[slnc 300]] The limit cannot tell a '
            'person from a script.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A 429 Too Many Requests response,', 'with a Retry-After header.', '', 'A class named Bucket, Limiter or', 'Throttle.', '', "Resilience4j's RateLimiter,", "Guava's RateLimiter, or a gateway"],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for an H T T P response with status four '
            'two nine, meaning too many requests. [[slnc 300]] Often with '
            'a header saying when to retry. [[slnc 300]] Look for a class '
            'named bucket, limiter, or throttle. [[slnc 300]] Look for '
            'rate limiter classes from libraries like Resilience four J '
            'or Guava. [[slnc 300]] Or a limit in the A P I '
            'documentation, such as a hundred requests a minute.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a rate limiter on any service', 'that shared callers can overwhelm,', 'and on any API you expose. Use a', 'token bucket to allow short', 'bursts, key it by caller, and tell', 'refused callers exactly when to', 'retry. Share the count across', 'servers if the limit must be', 'exact. Set the burst size from'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a rate limiter on '
            'any service that shared callers can overwhelm. [[slnc 300]] '
            'And on any A P I you offer to others. [[slnc 600]] Use a '
            'token bucket, so short bursts are allowed. [[slnc 300]] Give '
            'each caller its own bucket. [[slnc 300]] Tell refused '
            'callers exactly when to retry. [[slnc 300]] Share the count '
            'across servers, if the limit must be exact. [[slnc 300]] And '
            'set the bucket size from real page loads, not from a guess.'
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
        body=['For an internal service with one', 'known caller, a limit is only a', 'way to fail. It earns its place', 'with many or unknown callers.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For an internal '
            'service with one known caller, a limit is only another way '
            'to fail. [[slnc 400]] It earns its place when there are many '
            'callers, or callers you do not know.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Rate Limiter pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A rate '
            'limiter says no early, and says when to come back, and the '
            'price is extra state, and a limit that cannot tell a person '
            'from a script. [[slnc 500]] The full source code, written '
            'notes, diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 300]] It runs offline, with nothing '
            'installed except a Java development kit. [[slnc 500]] Here '
            "is one exercise to try. [[slnc 300]] Make each caller's "
            'bucket larger. [[slnc 300]] Then see which polite requests '
            'stop being refused. [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
