"""Scene definitions for the Fork-Join teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Fork-Join',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Fork-Join pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] Fork-Join splits a big job '
            'into smaller pieces of the same kind. [[slnc 300]] It runs '
            'the pieces at the same time, on several workers. [[slnc '
            '300]] Then it joins their answers back into one. [[slnc '
            '600]] Think of counting votes after an election. [[slnc '
            '300]] Each district counts its own ballots at the same time. '
            '[[slnc 300]] Then the district totals are added together. '
            '[[slnc 700]] In our online store, the job is adding up one '
            "hundred thousand order totals, for the day's report. [[slnc "
            '500]] In this video, we split the job in halves until the '
            'pieces are small, and run them at the same time. [[slnc '
            '300]] We will learn how small is small enough, and why one '
            'big piece limits the speed. [[slnc 300]] And then the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=["The day's report adds up 100000", 'order totals.', '', 'The machine has several', 'processors.', '', 'One loop uses one of them.', '', 'How do we use the rest?'],
        narration=(
            "Here is the scenario. [[slnc 400]] The day's report adds up "
            'one hundred thousand order totals. [[slnc 400]] The machine '
            'has several processors. [[slnc 300]] But a simple loop uses '
            'only one of them. [[slnc 500]] So here is the question. '
            '[[slnc 300]] How do we use the rest?'
        ),
    ),
    dict(
        key='03-loop', kind='console', title='One Loop',
        body="""ONE. One loop.
  100000 order totals.
  a loop, on one thread.
  499838000 pence.""",
        narration=(
            'First, the simple way: one loop. [[slnc 400]] Adding up the '
            'hundred thousand order totals gives nearly five million '
            'pounds. [[slnc 300]] To be exact, four hundred and '
            'ninety-nine million, eight hundred and thirty-eight thousand '
            'pence. [[slnc 500]] It runs on one thread. [[slnc 300]] And '
            'the other processors sit idle.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Fork: split the job in two, and', 'hand one half to another worker.', '', 'Keep splitting until a piece is', 'small enough to do directly.', '', 'Join: wait for the halves, and', 'combine their answers.'],
        narration=(
            'Now, the pattern, in two steps. [[slnc 500]] Fork: split the '
            'job in two, and hand one half to another worker. [[slnc '
            '300]] Keep splitting, until a piece is small enough to do '
            'directly. [[slnc 500]] Join: wait for both halves, and '
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
            'Second demo: split until it is small. [[slnc 400]] The job '
            'is split in halves, again and again, until each piece has '
            'ten thousand totals or fewer. [[slnc 500]] That gives '
            'sixteen small pieces, each added up directly. [[slnc 300]] '
            'Thirty-one tasks in all. [[slnc 300]] Sixteen that add, and '
            'fifteen that only split and join. [[slnc 500]] And the final '
            'total is exactly the same as the loop.'
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
            'Third demo: the pieces really do run together. [[slnc 400]] '
            'There is a pool of four workers, and sixteen pieces. [[slnc '
            '300]] Each piece is held back until four pieces are running '
            'at once. [[slnc 500]] The most running at the same moment is '
            'four. [[slnc 300]] This is not just a claim. [[slnc 300]] '
            'The pieces waited for each other, so they had to be running '
            'together.'
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
            'Fourth demo: how small is small enough? [[slnc 400]] This '
            'size limit is called the threshold. [[slnc 500]] With a '
            'threshold of one hundred thousand, there is just one piece. '
            '[[slnc 300]] That is simply the loop again. [[slnc 300]] '
            'With ten thousand, sixteen pieces. [[slnc 300]] With one '
            'hundred, one thousand and twenty-four pieces. [[slnc 300]] '
            'And with one, a hundred thousand pieces, and nearly two '
            'hundred thousand tasks. [[slnc 300]] Most of that work is '
            'just the cost of making tasks. [[slnc 500]] Choosing the '
            'threshold is the main decision.'
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
            'Fifth demo: pieces that are not the same size. [[slnc 400]] '
            'Four equal pieces could make the job up to four times '
            'faster. [[slnc 500]] But suppose one piece costs '
            'eighty-five, and the other three cost five each. [[slnc '
            '300]] Then the best possible speed-up is only about one '
            'point two times. [[slnc 500]] The whole job waits for the '
            'big piece. [[slnc 300]] And three workers sit waiting too. '
            '[[slnc 300]] Splitting the work evenly is half the battle.'
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
            'Finally, the cost. [[slnc 400]] Imagine a pool of two '
            'workers, and eight pieces that each wait on something slow, '
            'like a database. [[slnc 300]] Only two run at once. [[slnc '
            '500]] Fork-Join is for work that keeps the processor busy. '
            '[[slnc 300]] A worker that is waiting is a worker that '
            'cannot help. [[slnc 500]] And splitting just twenty items '
            'into single items makes thirty-nine tasks, to add up twenty '
            'numbers. [[slnc 300]] Small jobs are faster in a plain loop.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A class that extends RecursiveTask', 'or RecursiveAction, with fork()', '', 'ForkJoinPool.commonPool(),', 'parallelStream(), and', '', 'A compute() method that starts', 'with an if (size <= THRESHOLD).'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for a class that extends Recursive Task, or '
            'Recursive Action, calling fork and join. [[slnc 300]] Look '
            "for the Fork Join Pool, parallel streams, or Java's parallel "
            'sort. [[slnc 300]] And look for a compute method that starts '
            'by checking whether the piece is small enough.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use fork-join for large,', 'processor-bound jobs that split', 'into independent pieces of about', 'the same cost, such as sums,', 'sorts, searches and image work.', 'Choose the threshold from', 'measurement, keep the pieces free', 'of shared mutable state, and', 'prefer a parallel stream when the'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use Fork-Join for '
            'large jobs that keep the processor busy. [[slnc 300]] Jobs '
            'that split into independent pieces, of about the same cost. '
            '[[slnc 300]] Such as sums, sorting, searching, and image '
            'processing. [[slnc 500]] Choose the threshold by measuring. '
            '[[slnc 300]] Keep the pieces free of shared, changing data. '
            '[[slnc 300]] And prefer a parallel stream when the job fits '
            'one. [[slnc 500]] Do not use it for work that waits, or for '
            'small jobs.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 300]] And "
            'nothing depends on the clock, so every run gives the same '
            'result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For small jobs, or work that waits', 'on I/O, fork-join is overhead or', 'starvation. A plain loop, or a', 'thread pool sized for waiting, is', 'better.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For small jobs, '
            'Fork-Join is mostly overhead. [[slnc 300]] For work that '
            'waits on files or networks, it leaves workers stuck. [[slnc '
            '400]] A plain loop, or a thread pool sized for waiting, is '
            'better.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Fork-Join pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] Fork-Join '
            'splits a job to use every processor, and the gain depends on '
            'the threshold, and on the pieces being even. [[slnc 500]] '
            'The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 500]] '
            'Here is one exercise to try. [[slnc 300]] Try a threshold of '
            'five hundred, and count the pieces. [[slnc 300]] Then change '
            'the costs so one piece is huge, and listen to the speed-up '
            'fall. [[slnc 500]] If this helped, a like really does help '
            "other people find it. [[slnc 300]] And subscribe, if you'd "
            'like the rest of the series. [[slnc 400]] Thanks for '
            'watching.'
        ),
    ),
]
