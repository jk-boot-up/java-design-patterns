"""Scene definitions for the Bulkhead with Resilience4j teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Bulkhead with Resilience4j',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Bulkhead pattern '
            'with Resilience4j, in Java, and it is written and presented '
            'by Jayasekhar Konduru. [[slnc 300]] It is the framework '
            'version of the Bulkhead video. That one gave the nightly '
            'supplier feed and checkout their own pools of workers, so a '
            "slow partner api could fill the feed's pool without stopping "
            'the shop selling. This one shows the same idea inside '
            'Resilience4j. [[slnc 350]] The plain definition, in short: '
            'in Resilience4j, a bulkhead is an annotation that limits how '
            'many calls to one thing may run at once, or gives them their '
            'own threads. [[slnc 300]] By the end you will see one shared '
            'compartment let the feed starve checkout, then see a '
            'compartment each protect it, and see the costs: the wasted '
            'wall, the bypass, and the difference between a permit limit '
            'and a thread pool.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Bulkhead, the hand-built video,', 'gives the feed and checkout their', 'own pools of workers.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video assumes the Bulkhead video. If you have not seen '
            'it, start there. It gives the supplier feed and checkout '
            'their own pools of workers, so a slow feed cannot stop the '
            'shop selling. [[slnc 300]] This one uses the same example. '
            'It does not teach the pattern again. It shows what '
            'Resilience4j does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Resilience4j.', '', 'It contains two kinds of bulkhead.', '', 'It runs inside Spring Boot,', 'through an annotation.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first line of code, what Resilience4j is. '
            'Resilience4j is a library of resilience patterns for Java. '
            'It contains a bulkhead that limits concurrent calls, and one '
            'that runs the calls on their own threads. [[slnc 300]] And a '
            'promise: skipping this video loses none of the pattern. The '
            'hand-built one teaches all of it.'
        ),
    ),
    dict(
        key='04-shared', kind='console', title='One Compartment For Everything',
        body="""ONE. Shared.
  4 slow feed jobs hold all 4
  permits.

  checkout is refused.

  a background job stopped
  the shop selling.""",
        narration=(
            'First, the problem. One compartment of four permits serves '
            'everything. Four slow feed jobs take all four. Checkout, '
            'which is fast and fine, is refused. A background job has '
            'stopped the shop selling.'
        ),
    ),
    dict(
        key='05-own', kind='console', title='A Compartment Each',
        body="""TWO. A compartment each.
  2 feed jobs stuck.
  a third feed job: refused.

  checkout: sold.""",
        narration=(
            'Second, a compartment each. The feed has two permits, and '
            'two slow jobs fill them. A third is refused. Checkout, in '
            'its own compartment, sells as normal. [[slnc 300]] The hole '
            'floods one room. The ship stays up.'
        ),
    ),
    dict(
        key='06-fallback', kind='console', title='What A Full Compartment Does',
        body="""THREE. Full.
  refused at once, with no wait.

  with a fallback: the job gets
  feed batch skipped tonight.""",
        narration=(
            'Third, what a full compartment does to its callers. It '
            'refuses at once. The wait is set to zero, so no caller '
            'queues. With a fallback method, the refused job gets an '
            'answer: skipped tonight. Without one, it gets an exception.'
        ),
    ),
    dict(
        key='07-cost', kind='console', title='The Cost Of The Wall',
        body="""FOUR. The wall.
  feed: 0 permits free.
  checkout: 4 permits free.

  checkout's permits cannot
  help the feed.""",
        narration=(
            'Fourth, what the wall costs. The feed compartment has no '
            'permits free. Checkout has four, sitting idle. Nothing can '
            'lend them. That is the price of the protection, and the ship '
            'analogy predicts it.'
        ),
    ),
    dict(
        key='08-proxy', kind='console', title='The Annotation Is A Proxy',
        body="""FIVE. A proxy.
  10 feed jobs through this.
  all 10 inside at once.

  permits free: 2. the
  bulkhead never saw them.""",
        narration=(
            'Fifth, the proxy again. Ten feed jobs called through this '
            'are all inside at once, in a compartment that holds two. The '
            'bulkhead shows two permits free. It never saw a call. The '
            'same rule as every Spring proxy.'
        ),
    ),
    dict(
        key='09-pool', kind='console', title='A Compartment With Its Own Threads',
        body="""SIX. Own threads.
  four submissions, none
  blocked the caller.

  2 running, 1 queued.
  the fourth: refused.

  ran on bulkhead-feedpool.""",
        narration=(
            'Last, the other kind. A thread pool compartment runs each '
            'call on its own threads. Two are running, one waits in a '
            'queue of one, and the fourth is refused. The caller was '
            'never blocked, not even by the slow ones. [[slnc 300]] The '
            'permit kind protects the pool of the caller. The thread pool '
            'kind protects the caller itself.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['A compartment each.', '', 'Size them from real load.', '', 'Thread pool when the caller must', 'not block.', '', 'Never call on this.'],
        narration=(
            'My verdict, plainly. Give each kind of work its own '
            'compartment, and size them from real load. Choose the thread '
            'pool kind when a full compartment must not block the caller. '
            'And never call a bulkhead method on this.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['@Bulkhead with a name.', '', 'type equals THREADPOOL.', '', 'BulkheadFullException in a log.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'bulkhead annotation with a name. A type set to thread pool. '
            'Or a bulkhead full exception in a log.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Any Spring service that calls', 'several others, some of them slow.'],
        narration=(
            'You have met this in any Spring service that calls several '
            'others, some of them slow.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'Resilience4j 2.4.0.', '', 'No web server, no web starter.'],
        narration=(
            'For the record. Spring Boot four point one point one. '
            'Resilience four j two point four point zero. No web server, '
            'and no web starter.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: the real bulkheads', 'and real threads.', '', 'Slow calls are held at a gate,', 'so nothing depends on timing.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is real: the real bulkheads and real threads. The '
            'slow calls are held at a gate, so nothing depends on timing.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For one caller and one dependency,', "a limit is a rate limiter's job."],
        narration=(
            'So when is it too much? For one caller and one dependency, a '
            "limit is a rate limiter's job, not a compartment's."
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Size the checkout compartment', 'to two and predict act four.'],
        narration=(
            "That's Bulkhead with Resilience4j. [[slnc 250]] If you take "
            'one sentence away, take this one: Resilience4j gives you '
            'compartments as configuration, and the wall costs capacity. '
            '[[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough are all in the '
            'repository. [[slnc 300]] If you try one exercise, size the '
            'checkout compartment to two, and predict act four. [[slnc '
            '300]] If this helped, a like genuinely does help other '
            'people find it, and subscribe if you would like the rest of '
            'the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
