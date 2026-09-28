"""Scene definitions for the Scatter-Gather teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Scatter-Gather',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Scatter-Gather pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] Scatter-gather sends one '
            'request to many parties, all at the same time. [[slnc 300]] '
            'Then it gathers their answers, up to a deadline. [[slnc '
            '300]] And it combines them into one. [[slnc 600]] Think of '
            'asking several taxi firms for a quote at once. [[slnc 300]] '
            'You give them two minutes, then take the best offer you '
            'have. [[slnc 700]] In our online store, the product page '
            'shows the best price from four suppliers. [[slnc 500]] By '
            'the end, you will hear four suppliers asked one after '
            'another, then all at once. [[slnc 300]] A deadline stop the '
            'slowest one from holding up the page. [[slnc 300]] The page '
            'say honestly what was left out. [[slnc 300]] One failure not '
            'break the page. [[slnc 300]] And the bill.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The product page shows the best', 'price for a mug.', '', 'Four suppliers each know their', 'price.', '', 'Each takes a different time.', '', 'How do we ask them?'],
        narration=(
            'Here is the scenario. [[slnc 400]] The product page shows '
            'the best price for a mug. [[slnc 300]] Four suppliers each '
            'know their own price. [[slnc 300]] And each takes a '
            'different amount of time to answer. [[slnc 500]] So here is '
            'the question. [[slnc 300]] How do we ask them?'
        ),
    ),
    dict(
        key='03-seq', kind='console', title='Ask Them One After Another',
        body="""ONE. In turn.
  suppliers answer in 80, 120,
  200 and 900 ms.
  asked in turn: 1300 ms.""",
        narration=(
            'First demo: ask them one after another. [[slnc 400]] The '
            'four suppliers answer in eighty, a hundred and twenty, two '
            'hundred, and nine hundred milliseconds. [[slnc 500]] Asked '
            'in turn, the page waits thirteen hundred milliseconds. '
            '[[slnc 300]] That is all four times, added together.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Ask everyone at once.', '', 'Gather the answers as they come,', 'up to a deadline.', '', 'Combine what arrived, and say', 'what did not.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Ask everyone at once. [[slnc '
            '300]] Gather the answers as they arrive, up to a deadline. '
            '[[slnc 300]] Combine what arrived. [[slnc 300]] And say what '
            'did not.'
        ),
    ),
    dict(
        key='05-par', kind='console', title='Ask Them All At Once',
        body="""TWO. All at once.
  the same four, together:
  the page waits for the
  slowest: 900 ms.""",
        narration=(
            'Second demo: ask them all at once. [[slnc 400]] The same '
            'four suppliers, asked together. [[slnc 500]] Now the page '
            'waits only for the slowest one: nine hundred milliseconds, '
            'not thirteen hundred. [[slnc 500]] But it is still held up '
            'by that slowest supplier.'
        ),
    ),
    dict(
        key='06-deadline', kind='console', title='Do Not Wait For The Slowest',
        body="""THREE. A deadline.
  4 suppliers asked at once.
  deadline 500 ms:
  3 quotes gathered.
  Delta: too slow.

  best shown: Beta at 1190.
  the page waits 500, not 900.""",
        narration=(
            'Third demo: do not wait for the slowest. [[slnc 400]] All '
            'four suppliers are asked at the same moment. [[slnc 300]] '
            'With a deadline of five hundred milliseconds. [[slnc 500]] '
            'Three quotes come back in time. [[slnc 300]] Delta is too '
            'slow, and is left out. [[slnc 500]] The best of the three is '
            'shown: Beta, at eleven pounds ninety. [[slnc 300]] The page '
            'waited five hundred milliseconds, not nine hundred.'
        ),
    ),
    dict(
        key='07-honest', kind='console', title='Say What Was Left Out',
        body="""FOUR. Partial.
  best of 2 of 3 suppliers:
  1190 from Beta.

  Delta did not answer, and
  would have been 990.

  say that it is partial.""",
        narration=(
            'Fourth demo: say what was left out. [[slnc 400]] The page '
            'shows the best of the suppliers that answered: eleven pounds '
            'ninety, from Beta. [[slnc 500]] But Delta, which did not '
            'answer in time, would have been cheaper, at nine pounds '
            'ninety. [[slnc 500]] A partial answer is only honest if it '
            'says that it is partial.'
        ),
    ),
    dict(
        key='08-fail', kind='console', title='A Supplier That Fails',
        body="""FIVE. A failure.
  Beta is down.
  2 quotes gathered.
  missing: Beta, and why.

  one failure did not fail the
  page.""",
        narration=(
            'Fifth demo: a supplier that fails. [[slnc 400]] Beta is '
            'down. [[slnc 500]] The page still gets the other quotes. '
            '[[slnc 300]] It names Beta as missing, and says why. [[slnc '
            '500]] One failure did not break the page.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  1 view = 4 supplier calls.
  1000 views = 4000 calls.

  each quick 99 times in 100:
  ask 1: 99 pages in 100 quick.
  ask 4: 96.
  ask 10: 90.

  a deadline stops it.""",
        narration=(
            'Finally, the bill. [[slnc 400]] One page view is now four '
            'supplier calls. [[slnc 300]] A thousand views make four '
            'thousand calls. [[slnc 600]] And the more suppliers you ask, '
            'the more often one of them is slow. [[slnc 500]] Suppose '
            'each supplier is quick ninety-nine times in a hundred. '
            '[[slnc 300]] Ask one, and ninety-nine pages in a hundred are '
            'quick. [[slnc 300]] Ask four, and wait for all of them, and '
            'it drops to ninety-six. [[slnc 300]] Ask ten, and it drops '
            'to ninety. [[slnc 500]] A deadline is what stops the slowest '
            'supplier setting the pace.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['CompletableFuture.allOf or', 'invokeAll with a timeout.', '', 'A price comparison, flight search,', 'or federated search.', '', 'A method that returns results and', 'a list of sources that did not'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for Java code that starts several calls '
            'together, and waits for all of them, with a timeout. [[slnc '
            '300]] Look for price comparison, flight search, or search '
            'across many sources. [[slnc 300]] Look for a method that '
            'returns results, plus a list of sources that did not '
            'respond. [[slnc 300]] Search engines like Elasticsearch do '
            'this too, across the pieces of their data.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use scatter-gather when several', 'independent sources can answer the', 'same question, and the best or a', 'combination of the answers is what', 'you want. Always give it a', 'deadline, treat a failure like a', 'late answer, and say when an', 'answer is partial. Watch the fan-', 'out: every request now costs as'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use scatter-gather '
            'when several independent sources can answer the same '
            'question. [[slnc 300]] And you want the best answer, or a '
            'combination of them. [[slnc 600]] Always set a deadline. '
            '[[slnc 300]] Treat a failure just like a late answer. [[slnc '
            '300]] And say clearly when an answer is partial. [[slnc '
            '500]] And watch the cost. [[slnc 300]] Every request now '
            'costs as many calls as there are sources.'
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
        body=['With one source, or when you need', 'every answer without exception,', 'scatter-gather has nothing to', 'gather. With a very large fan-out,', 'the deadline decides more than the', 'data.'],
        narration=(
            'So, when is this too much? [[slnc 400]] With only one '
            'source, there is nothing to gather. [[slnc 300]] And if you '
            'truly need every single answer, a deadline does not help. '
            '[[slnc 400]] And with a very large number of sources, the '
            'deadline decides more than the data does.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Scatter-Gather pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] '
            'Scatter-gather asks many sources at once, and waits only '
            'until a deadline, and the price is many more calls, and '
            'answers that may be partial. [[slnc 500]] The full source '
            'code, written notes, diagrams, and an animated walkthrough '
            'are all in the repository. [[slnc 300]] It runs offline, '
            'with nothing installed except a Java development kit. [[slnc '
            '500]] Here is one exercise to try. [[slnc 300]] Add a fifth '
            'supplier that is always slow. [[slnc 300]] Then see what the '
            'deadline does for the page. [[slnc 500]] If this helped, a '
            'like really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
