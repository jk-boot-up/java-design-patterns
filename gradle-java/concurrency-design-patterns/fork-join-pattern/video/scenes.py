"""Scene definitions for the Fork-Join teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Fork-Join',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Fork-Join '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: fork '
            'join splits a big job into smaller pieces of the same kind, '
            'runs the pieces at the same time on several workers, and '
            'joins their answers back into one. [[slnc 350]] This is '
            'another project in the concurrency category, whose subject '
            'is how threads share work and state without corrupting '
            'either. In our online store, the job is adding up a hundred '
            "thousand order totals for the day's report. [[slnc 300]] By "
            'the end you will see one loop add a hundred thousand totals, '
            'see the job split in halves until the pieces are small, see '
            'four pieces run at the same moment, see how small is small '
            'enough, see one big piece cap the speedup, and see the bill, '
            'which is that it only helps work that uses the processor.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=["The day's report adds up 100000", 'order totals.', '', 'The machine has several', 'processors.', '', 'One loop uses one of them.', '', 'How do we use the rest?'],
        narration=(
            "Here is the scenario. The day's report adds up a hundred "
            'thousand order totals. The machine has several processors, '
            'and one loop uses just one of them. [[slnc 300]] The '
            'question: how do we use the rest?'
        ),
    ),
    dict(
        key='03-loop', kind='console', title='One Loop',
        body="""ONE. One loop.
  100000 order totals.
  a loop, on one thread.
  499838000 pence.""",
        narration=(
            'First, one loop. Adding up a hundred thousand order totals, '
            'in a loop, gives the answer: four hundred and ninety nine '
            'million, eight hundred and thirty eight thousand pence. It '
            'runs on one thread, while the other processors are idle.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Fork: split the job in two, and', 'hand one half to another worker.', '', 'Keep splitting until a piece is', 'small enough to do directly.', '', 'Join: wait for the halves, and', 'combine their answers.'],
        narration=(
            'The pattern. Fork: split the job in two, and hand one half '
            'to another worker. Keep splitting until a piece is small '
            'enough to do directly. Then join: wait for the halves, and '
            'combine their answers.'
        ),
    ),
    dict(
        key='05-split', kind='console', title='Split It Until It Is Small',
        body="""TWO. Split.
  halves until a piece is 10000
  or fewer.
  16 pieces added directly.
  31 tasks in all.

  the same total as the loop.""",
        narration=(
            'Second, split it until it is small. The job is split in '
            'halves, again and again, until a piece is ten thousand or '
            'fewer. That gives sixteen pieces, added directly, and thirty '
            'one tasks in all: sixteen leaves, and fifteen that only '
            'split and join. The total is the same as the loop.'
        ),
    ),
    dict(
        key='06-par', kind='console', title='The Pieces Really Run Together',
        body="""THREE. Together.
  a pool of 4 workers.
  16 pieces, each held until 4
  are running.
  most at the same moment: 4.""",
        narration=(
            'Third, the pieces really run together. A pool of four '
            'workers, and sixteen pieces. Each piece is held until four '
            'are running at once. The most running at the same moment is '
            'four. It is not a claim. The pieces waited for each other, '
            'so they had to be running together.'
        ),
    ),
    dict(
        key='07-size', kind='console', title='How Small Is Small Enough',
        body="""FOUR. How small.
  threshold 100000: 1 piece.
  10000: 16 pieces.
  100: 1024 pieces.
  1: 100000 pieces, 199999 tasks.

  one piece is the loop. one per
  item is the cost of tasks.""",
        narration=(
            'Fourth, how small is small enough. A threshold of a hundred '
            'thousand gives one piece, which is just the loop. Ten '
            'thousand gives sixteen pieces. A hundred gives a thousand '
            'and twenty four. One gives a hundred thousand pieces, and '
            'nearly two hundred thousand tasks, which is mostly the cost '
            'of making tasks. The threshold is the main decision.'
        ),
    ),
    dict(
        key='08-skew', kind='console', title='Pieces That Are Not The Same Size',
        body="""FIVE. Not equal.
  costs 25, 25, 25, 25:
  best speedup 4.0.

  costs 85, 5, 5, 5:
  best speedup 1.18.

  the job waits for the big one.""",
        narration=(
            'Fifth, pieces that are not the same size. Four equal pieces '
            'could give four times the speed. If one piece costs eighty '
            'five and the others five each, the best possible speedup is '
            'one point one eight. The job waits for the big piece, and '
            'three workers wait for it too. Splitting evenly is half the '
            'work.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  2 workers, 8 pieces that wait:
  2 running of 8.

  fork-join is for work that uses
  the processor.

  20 items split to singles:
  39 tasks. use a loop.""",
        narration=(
            'Last, the bill. A pool of two workers, and eight pieces that '
            'each wait on something slow, like a database: only two run '
            'at once. Fork join is for work that uses the processor. A '
            'worker that waits is a worker that cannot help. And '
            'splitting twenty items into single items makes thirty nine '
            'tasks, to add up twenty numbers. Small jobs are faster in a '
            'loop.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A class that extends RecursiveTask', 'or RecursiveAction, with fork()', '', 'ForkJoinPool.commonPool(),', 'parallelStream(), and', '', 'A compute() method that starts', 'with an if (size <= THRESHOLD).'],
        narration=(
            'How do you recognise this in code you did not write? A class '
            'that extends RecursiveTask or RecursiveAction, with fork() '
            'and join(). ForkJoinPool.commonPool(), parallelStream(), and '
            'Arrays.parallelSort. A compute() method that starts with an '
            'if (size <= THRESHOLD). CompletableFuture chains that run on '
            'the common pool.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use fork-join for large,', 'processor-bound jobs that split', 'into independent pieces of about', 'the same cost, such as sums,', 'sorts, searches and image work.', 'Choose the threshold from', 'measurement, keep the pieces free', 'of shared mutable state, and', 'prefer a parallel stream when the'],
        narration=(
            'Here is my verdict, plainly. Use fork-join for large, '
            'processor-bound jobs that split into independent pieces of '
            'about the same cost, such as sums, sorts, searches and image '
            'work. Choose the threshold from measurement, keep the pieces '
            'free of shared mutable state, and prefer a parallel stream '
            'when the job fits one. Do not use it for work that waits, or '
            'for small jobs.'
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
        body=['For small jobs, or work that waits', 'on I/O, fork-join is overhead or', 'starvation. A plain loop, or a', 'thread pool sized for waiting, is', 'better.'],
        narration=(
            'So when is it too much? For small jobs, or work that waits '
            'on I/O, fork-join is overhead or starvation. A plain loop, '
            'or a thread pool sized for waiting, is better.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Fork-Join. [[slnc 250]] If you take one sentence "
            'away, take this one: fork-join splits a job to use every '
            'processor, and the gain depends on the threshold, and on the '
            'pieces being even. [[slnc 350]] The full source, the written '
            'notes, the diagrams and an animated walkthrough are all in '
            'the repository, running offline with nothing installed but a '
            'Java development kit. [[slnc 300]] If you try one exercise, '
            'try a threshold of five hundred and count the pieces, then '
            'change the costs so one piece is huge. [[slnc 300]] If this '
            'helped, a like genuinely does help other people find it, and '
            'subscribe if you would like the rest of the series. [[slnc '
            '250]] Thanks for watching.'
        ),
    ),
]
