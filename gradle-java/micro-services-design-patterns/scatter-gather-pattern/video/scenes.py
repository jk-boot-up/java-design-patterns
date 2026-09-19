"""Scene definitions for the Scatter-Gather teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Scatter-Gather',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Scatter-Gather '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: '
            'scatter gather sends one request to many parties at the same '
            'time, and then gathers their answers, up to a deadline, and '
            'combines them into one. [[slnc 350]] This is another project '
            'in the microservices category, whose subject is how many '
            'small services stay reliable when they talk to each other. '
            'In our online store, the product page shows the best price '
            'from four suppliers. [[slnc 300]] By the end you will see '
            'four suppliers asked one after another, then all at once, '
            'see a deadline stop the slowest one setting the pace, see '
            'the page say honestly what was left out, see one failure not '
            'fail the page, and see the bill, which is that one view '
            'becomes many calls.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The product page shows the best', 'price for a mug.', '', 'Four suppliers each know their', 'price.', '', 'Each takes a different time.', '', 'How do we ask them?'],
        narration=(
            'Here is the scenario. The product page shows the best price '
            'for a mug. Four suppliers each know their price, and each '
            'takes a different time to answer. [[slnc 300]] The question: '
            'how do we ask them?'
        ),
    ),
    dict(
        key='03-seq', kind='console', title='Ask Them One After Another',
        body="""ONE. In turn.
  suppliers answer in 80, 120,
  200 and 900 ms.
  asked in turn: 1300 ms.""",
        narration=(
            'First, ask them one after another. The four suppliers answer '
            'in eighty, a hundred and twenty, two hundred and nine '
            'hundred milliseconds. Asked in turn, the page waits thirteen '
            'hundred milliseconds, the sum of all four.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Ask everyone at once.', '', 'Gather the answers as they come,', 'up to a deadline.', '', 'Combine what arrived, and say', 'what did not.'],
        narration=(
            'The pattern. Ask everyone at once. Gather the answers as '
            'they come, up to a deadline. Combine what arrived, and say '
            'what did not.'
        ),
    ),
    dict(
        key='05-par', kind='console', title='Ask Them All At Once',
        body="""TWO. All at once.
  the same four, together:
  the page waits for the
  slowest: 900 ms.""",
        narration=(
            'Second, ask them all at once. The same four suppliers, asked '
            'together. The page now waits for the slowest: nine hundred '
            'milliseconds, not thirteen hundred. But it is still held up '
            'by the slowest one.'
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
            'Third, do not wait for the slowest. Four suppliers are being '
            'asked at the same moment. With a deadline of five hundred '
            'milliseconds, three quotes come back. Delta is too slow, and '
            'is left out. The best of the three is shown: Beta, at eleven '
            'ninety. The page waited five hundred milliseconds, not nine '
            'hundred.'
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
            'Fourth, say what was left out. The page shows: the best of '
            'two of three suppliers, eleven ninety from Beta. The one '
            'that did not answer, Delta, would have been cheaper, at nine '
            'ninety. A partial answer is honest only if it says that it '
            'is partial.'
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
            'Fifth, a supplier that fails. Beta is down. The page gets '
            'the other two quotes, and names Beta as missing, and says '
            'why. One failure did not fail the page.'
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
            'Last, the bill. One page view is now four supplier calls. A '
            'thousand views make four thousand. And the more you ask, the '
            'more often the slowest sets the pace. If each supplier is '
            'quick ninety nine times in a hundred, asking one gives '
            'ninety nine quick pages in a hundred. Asking four and '
            'waiting for all gives ninety six. Asking ten gives ninety. A '
            'deadline is what stops the slowest setting the pace.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['CompletableFuture.allOf or', 'invokeAll with a timeout.', '', 'A price comparison, flight search,', 'or federated search.', '', 'A method that returns results and', 'a list of sources that did not'],
        narration=(
            'How do you recognise this in code you did not write? '
            'CompletableFuture.allOf or invokeAll with a timeout. A price '
            'comparison, flight search, or federated search. A method '
            'that returns results and a list of sources that did not '
            "respond. Elasticsearch's search across shards, which "
            'scatters and gathers.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use scatter-gather when several', 'independent sources can answer the', 'same question, and the best or a', 'combination of the answers is what', 'you want. Always give it a', 'deadline, treat a failure like a', 'late answer, and say when an', 'answer is partial. Watch the fan-', 'out: every request now costs as'],
        narration=(
            'Here is my verdict, plainly. Use scatter-gather when several '
            'independent sources can answer the same question, and the '
            'best or a combination of the answers is what you want. '
            'Always give it a deadline, treat a failure like a late '
            'answer, and say when an answer is partial. Watch the '
            'fan-out: every request now costs as many calls as there are '
            'sources.'
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
        body=['With one source, or when you need', 'every answer without exception,', 'scatter-gather has nothing to', 'gather. With a very large fan-out,', 'the deadline decides more than the', 'data.'],
        narration=(
            'So when is it too much? With one source, or when you need '
            'every answer without exception, scatter-gather has nothing '
            'to gather. With a very large fan-out, the deadline decides '
            'more than the data.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Scatter-Gather. [[slnc 250]] If you take one sentence "
            'away, take this one: scatter-gather asks many at once and '
            'waits for a deadline, and the price is fan-out and partial '
            'answers. [[slnc 350]] The full source, the written notes, '
            'the diagrams and an animated walkthrough are all in the '
            'repository, running offline with nothing installed but a '
            'Java development kit. [[slnc 300]] If you try one exercise, '
            'add a fifth supplier that is always slow, and see what the '
            'deadline does for the page. [[slnc 300]] If this helped, a '
            'like genuinely does help other people find it, and subscribe '
            'if you would like the rest of the series. [[slnc 250]] '
            'Thanks for watching.'
        ),
    ),
]
