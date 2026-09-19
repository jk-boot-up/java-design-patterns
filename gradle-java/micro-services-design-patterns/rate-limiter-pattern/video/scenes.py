"""Scene definitions for the Rate Limiter teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Rate Limiter',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Rate Limiter '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: a '
            'rate limiter refuses requests beyond an agreed rate, so that '
            'one caller cannot use up a service that everyone shares. It '
            'says no early, so the service does not fail late. [[slnc '
            '350]] This is another project in the microservices category, '
            'whose subject is how many small services stay reliable when '
            'they talk to each other. In our online store, the thing that '
            'can be overwhelmed is the product search. [[slnc 300]] By '
            'the end you will see a thousand requests reach a search that '
            'can serve a hundred, see a token bucket allow a burst and '
            'then a steady rate, see a bucket each protect a polite '
            'caller from a greedy one, hear a refusal say exactly when to '
            'come back, and see the bill.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The product search can serve 100', 'requests a second.', '', 'A script sends 1000 in a second.', '', 'Everyone else waits behind it.', '', 'What should the search do?'],
        narration=(
            'Here is the scenario. The product search can serve a hundred '
            'requests a second. One client, perhaps a script, sends a '
            'thousand in a single second, and every other customer waits '
            'behind them. [[slnc 300]] The question: what should the '
            'search do about the other nine hundred?'
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
            'First, no limit. The search can serve a hundred requests a '
            'second. One client sends a thousand. All are accepted. Nine '
            'hundred of them are beyond what the search can serve, and '
            'every other customer waits behind them.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A bucket holds tokens.', '', 'Each request takes one.', '', 'The bucket refills at a steady', 'rate, up to its size.', '', 'No token: refused, at once,', 'and told when to come back.'],
        narration=(
            'The pattern. A bucket holds tokens. Each request takes one. '
            'The bucket refills at a steady rate, up to its size, and no '
            'further. If there is no token, the request is refused at '
            'once, and told when to come back.'
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
            'Second, a bucket of tokens. Ten tokens, refilled at five a '
            'second. A burst of twenty at once: ten are allowed, ten are '
            'refused. One second later, another twenty: five are allowed, '
            'the five that refilled. After ten quiet seconds the bucket '
            'is full again, and no fuller. Ten.'
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
            'Third, a steady rate always gets through. Five requests a '
            'second, evenly spaced, for a whole minute: three hundred of '
            'three hundred are allowed. A well behaved client never '
            'notices the limiter. A burst is tolerated, up to the size of '
            'the bucket. A sustained rate above the refill is not.'
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
            'Fourth, one bucket for everyone, or one each. With a single '
            'shared bucket, a greedy client takes all ten tokens, and a '
            'polite client is refused. That is not protection, it is a '
            'different outage. With a bucket each, the greedy client is '
            'held to ten, and the polite client is allowed.'
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
            'Fifth, say when to come back. The bucket is empty, and the '
            'refusal says: retry after a thousand milliseconds. One '
            'millisecond early, and the request is refused. At the moment '
            'it said, it is allowed. The client does not have to guess, '
            'and does not hammer.'
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
            'Last, the bill. Three servers, each with its own bucket, '
            'allow thirty, not ten. The limit is three times looser than '
            'it says. Ten thousand callers mean ten thousand buckets in '
            'memory. And a real page that loads twelve things at once '
            'gets only ten. The limit cannot tell a person from a script.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A 429 Too Many Requests response,', 'with a Retry-After header.', '', 'A class named Bucket, Limiter or', 'Throttle.', '', "Resilience4j's RateLimiter,", "Guava's RateLimiter, or a gateway"],
        narration=(
            'How do you recognise this in code you did not write? A 429 '
            'Too Many Requests response, with a Retry-After header. A '
            "class named Bucket, Limiter or Throttle. Resilience4j's "
            "RateLimiter, Guava's RateLimiter, or a gateway plugin. A "
            'limit written in the API documentation, such as 100 requests '
            'a minute.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a rate limiter on any service', 'that shared callers can overwhelm,', 'and on any API you expose. Use a', 'token bucket to allow short', 'bursts, key it by caller, and tell', 'refused callers exactly when to', 'retry. Share the count across', 'servers if the limit must be', 'exact. Set the burst size from'],
        narration=(
            'Here is my verdict, plainly. Use a rate limiter on any '
            'service that shared callers can overwhelm, and on any API '
            'you expose. Use a token bucket to allow short bursts, key it '
            'by caller, and tell refused callers exactly when to retry. '
            'Share the count across servers if the limit must be exact. '
            'Set the burst size from real page loads, not from a guess.'
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
        body=['For an internal service with one', 'known caller, a limit is only a', 'way to fail. It earns its place', 'with many or unknown callers.'],
        narration=(
            'So when is it too much? For an internal service with one '
            'known caller, a limit is only a way to fail. It earns its '
            'place with many or unknown callers.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Rate Limiter. [[slnc 250]] If you take one sentence "
            'away, take this one: a rate limiter says no early and says '
            'when to come back, and the price is state, and a limit that '
            'cannot tell a person from a script. [[slnc 350]] The full '
            'source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository, running offline with '
            'nothing installed but a Java development kit. [[slnc 300]] '
            'If you try one exercise, make the bucket for a caller '
            'larger, and see which polite requests stop being refused. '
            '[[slnc 300]] If this helped, a like genuinely does help '
            'other people find it, and subscribe if you would like the '
            'rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
