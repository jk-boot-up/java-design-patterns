"""Scene definitions for the Bulkhead with Resilience4j teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Bulkhead with Resilience4j',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Bulkhead pattern in Java, using a library called Resilience '
            'four J. [[slnc 300]] This video is presented by Jayasekhar '
            'Konduru. [[slnc 600]] First, a simple definition. [[slnc '
            '300]] A bulkhead gives each kind of work its own '
            'compartment. [[slnc 300]] So a slow job can fill its own '
            'compartment, but cannot take the room that other work needs. '
            '[[slnc 500]] The name comes from ships. [[slnc 300]] Walls '
            'divide the hull into watertight rooms, so one hole floods '
            'one room, not the whole ship. [[slnc 600]] In Resilience '
            'four J, a bulkhead is an annotation. [[slnc 300]] It limits '
            'how many calls to one thing may run at the same time. [[slnc '
            '300]] Or it gives those calls threads of their own. [[slnc '
            '700]] In our online store, a slow nightly supplier feed must '
            'never stop checkout from selling. [[slnc 500]] By the end, '
            'you will hear one shared compartment let the feed starve '
            'checkout. [[slnc 300]] Then a compartment each, protecting '
            'it. [[slnc 300]] And the costs: the idle room behind the '
            'wall, a way to bypass it by accident, and the two kinds of '
            'bulkhead.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Bulkhead, the hand-built video,', 'gives the feed and checkout their', 'own pools of workers.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video builds on the plain Java Bulkhead video. [[slnc '
            '300]] If you have not seen it, start there. [[slnc 500]] '
            'That video gives the supplier feed and checkout their own '
            'pools of workers. [[slnc 300]] So a slow feed cannot stop '
            'the shop selling. [[slnc 500]] This video uses the same '
            'example. [[slnc 300]] It does not teach the pattern again. '
            '[[slnc 300]] It shows what Resilience four J does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Resilience4j.', '', 'It contains two kinds of bulkhead.', '', 'It runs inside Spring Boot,', 'through an annotation.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before any code, what is Resilience four J? [[slnc 400]] It '
            'is a library of resilience patterns for Java. [[slnc 300]] '
            'It has two kinds of bulkhead. [[slnc 300]] One limits how '
            'many calls run at once. [[slnc 300]] The other runs the '
            'calls on threads of their own. [[slnc 300]] Here, it runs '
            'inside Spring Boot, switched on by an annotation. [[slnc '
            '500]] And a promise. [[slnc 300]] Skipping this video loses '
            'none of the pattern. [[slnc 300]] The plain Java video '
            'teaches all of it.'
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
            'First, the problem. [[slnc 400]] One compartment serves '
            'everything, and it has four permits. [[slnc 300]] A permit '
            'is simply permission for one call to run. [[slnc 500]] Four '
            'slow feed jobs take all four permits. [[slnc 300]] Then '
            'checkout arrives. [[slnc 300]] It is fast, and nothing is '
            'wrong with it. [[slnc 300]] But it is refused. [[slnc 500]] '
            'A background job has stopped the shop selling.'
        ),
    ),
    dict(
        key='05-own', kind='console', title='A Compartment Each',
        body="""TWO. A compartment each.
  2 feed jobs stuck.
  a third feed job: refused.

  checkout: sold.""",
        narration=(
            'Second demo: a compartment each. [[slnc 400]] The feed gets '
            'two permits of its own. [[slnc 300]] Two slow feed jobs fill '
            'them. [[slnc 300]] A third feed job is refused. [[slnc 500]] '
            'Checkout has its own compartment. [[slnc 300]] So it sells '
            'as normal. [[slnc 500]] The hole floods one room. [[slnc '
            '300]] The ship stays up.'
        ),
    ),
    dict(
        key='06-fallback', kind='console', title='What A Full Compartment Does',
        body="""THREE. Full.
  refused at once, with no wait.

  with a fallback: the job gets
  feed batch skipped tonight.""",
        narration=(
            'Third demo: what a full compartment does to the callers. '
            '[[slnc 400]] It refuses them at once. [[slnc 300]] The '
            'waiting time is set to zero, so no caller queues up. [[slnc '
            '500]] You can add a fallback method, which is a backup '
            'answer. [[slnc 300]] With a fallback, the refused job hears: '
            'feed batch skipped tonight. [[slnc 300]] Without one, it '
            'gets an error.'
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
            "Fourth demo: what the wall costs. [[slnc 400]] The feed's "
            "compartment has no permits free. [[slnc 300]] Checkout's "
            'compartment has four permits free, sitting idle. [[slnc '
            '500]] And nothing can lend them to the feed. [[slnc 300]] '
            'That is the price of the protection. [[slnc 300]] Just like '
            'the ship, where an empty room cannot lend its space to a '
            'flooded one.'
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
            'Fifth demo: a trap. [[slnc 400]] Spring adds the bulkhead by '
            'wrapping the object in a proxy. [[slnc 300]] A proxy is a '
            'stand-in that sits in front of the real object, and checks '
            'each call on the way in. [[slnc 500]] But if a method calls '
            'another method on the same object, the call never goes '
            'through the proxy. [[slnc 300]] So here, ten feed jobs are '
            'called from inside the same object. [[slnc 300]] All ten run '
            'at once, in a compartment meant for two. [[slnc 500]] And '
            'the bulkhead still reports two permits free. [[slnc 300]] It '
            'never saw a single call. [[slnc 300]] The same rule applies '
            'to every Spring annotation that works through a proxy.'
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
            'Last demo: the other kind of bulkhead. [[slnc 400]] This one '
            'runs each call on threads of its own. [[slnc 500]] Four jobs '
            'are handed to it. [[slnc 300]] Two are running. [[slnc 300]] '
            'One waits in a queue that holds only one. [[slnc 300]] And '
            'the fourth is refused. [[slnc 500]] The caller was never '
            'blocked, not even by the slow jobs. [[slnc 500]] So here is '
            'the difference. [[slnc 300]] The permit kind protects the '
            "caller's shared threads. [[slnc 300]] The thread pool kind "
            'protects the caller itself, because the caller never waits.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['A compartment each.', '', 'Size them from real load.', '', 'Thread pool when the caller must', 'not block.', '', 'Never call on this.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Give each kind of work '
            'its own compartment. [[slnc 300]] And size each one from '
            'real load, not from a guess. [[slnc 500]] Choose the thread '
            'pool kind when the caller must never be blocked. [[slnc '
            '500]] And never call a bulkhead method from inside the same '
            'object, because the proxy is skipped.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['@Bulkhead with a name.', '', 'type equals THREADPOOL.', '', 'BulkheadFullException in a log.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for a bulkhead annotation, with a name. [[slnc '
            '300]] Look for a type set to thread pool. [[slnc 300]] Or '
            'look for a bulkhead full exception in a log.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Any Spring service that calls', 'several others, some of them slow.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In any Spring '
            'service that calls several other services, where some of '
            'them are slow.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'Resilience4j 2.4.0.', '', 'No web server, no web starter.'],
        narration=(
            'For the record, here is what was used. [[slnc 300]] Spring '
            'Boot, version four point one point one. [[slnc 300]] '
            'Resilience four J, version two point four point zero. [[slnc '
            '300]] There is no web server, and no web starter.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: the real bulkheads', 'and real threads.', '', 'Slow calls are held at a gate,', 'so nothing depends on timing.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is real: the real bulkheads, and real threads. '
            '[[slnc 300]] The slow calls are held at a gate, until the '
            'demo opens it. [[slnc 300]] So nothing depends on timing, '
            'and every run gives the same result.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For one caller and one dependency,', "a limit is a rate limiter's job."],
        narration=(
            'So, when is this too much? [[slnc 400]] If there is only one '
            'caller and one slow service, you do not need compartments. '
            '[[slnc 300]] A simple limit on how often you call it is '
            'enough. [[slnc 300]] That is the job of a rate limiter.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Size the checkout compartment', 'to two and predict act four.'],
        narration=(
            "That's Bulkhead, with Resilience four J. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] '
            'Resilience four J gives you compartments as configuration, '
            'and the wall always costs some idle capacity. [[slnc 500]] '
            'The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 500]] '
            'Here is one exercise to try. [[slnc 300]] Give the checkout '
            'compartment two permits instead of four. [[slnc 300]] Then '
            'guess what the fourth demo will report, before you run it. '
            '[[slnc 500]] If this helped, a like really does help other '
            "people find it. [[slnc 300]] And subscribe, if you'd like "
            'the rest of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
