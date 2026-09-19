"""Scene definitions for the Load Balancing with Spring Cloud LoadBalancer teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Load Balancing with Spring Cloud LoadBalancer',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Client-Side Load '
            'Balancing pattern with Spring Cloud LoadBalancer, in Java, '
            'and it is written and presented by Jayasekhar Konduru. '
            '[[slnc 300]] It is the framework version of the Client-Side '
            'Load Balancing video. That one chose among three copies of '
            'the catalogue service on the client side, with four '
            'hand-written strategies, and showed that a fair strategy is '
            'not always a fast one. This one shows the same idea inside '
            'Spring Cloud LoadBalancer. [[slnc 350]] The plain '
            'definition, in short: in Spring Cloud LoadBalancer, the '
            'caller uses a service name, and a balancer picks one copy of '
            'the service for each request. [[slnc 300]] By the end you '
            'will see twelve real requests spread by a real balancer, '
            'then see fair not being fast, a strategy of your own, a '
            'stopped copy, and the trap of real addresses.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Client-Side Load Balancing, the', 'hand-built video, chooses among', 'three copies of the catalogue.', '', 'It shows fair is not always fast.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video assumes the Client-Side Load Balancing video. If '
            'you have not seen it, start there. It chooses among three '
            'copies of the catalogue service on the client side, with '
            'four strategies written by hand, and shows that a fair '
            'strategy is not always a fast one. [[slnc 300]] This one '
            'uses the same example. It does not teach the pattern again. '
            'It shows what Spring Cloud LoadBalancer does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Two things are new: Spring Boot, and', 'Spring Cloud LoadBalancer.', '', 'It sits inside the HTTP client.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first line of code, what Spring Cloud '
            'LoadBalancer is. Spring Cloud LoadBalancer is a client-side '
            'balancer for Spring. The caller uses a service name, and the '
            'balancer picks a copy for every request. Round robin is the '
            'default. [[slnc 300]] And a promise: skipping this video '
            'loses none of the pattern. The hand-built one teaches all of '
            'it.'
        ),
    ),
    dict(
        key='04-rr', kind='console', title='Twelve Requests, One Name',
        body="""ONE. One name.
  12 requests: 4, 4, 4.

  the caller never saw an
  address.""",
        narration=(
            'First, the default. Twelve requests go to the name '
            'catalogue. The balancer spreads them four, four and four. '
            'The caller wrote only a name, and never saw an address.'
        ),
    ),
    dict(
        key='05-fair', kind='console', title='Fair Is Not Fast',
        body="""TWO. Fair, not fast.
  work: 4, 4, 24.

  the slow copy did the most.""",
        narration=(
            'Second, fair is not fast. Copy c is on older hardware, six '
            'times the cost per request. Round robin gives it a third of '
            'the requests. The work comes out four, four and twenty four.'
        ),
    ),
    dict(
        key='06-own', kind='console', title='A Strategy Of Our Own',
        body="""THREE. Our own.
  least work so far:
  requests 6, 5, 1.
  work 6, 5, 6.

  registered for one name.""",
        narration=(
            'Third, a strategy of our own. It sends each request to the '
            'copy with the least work so far. The slow copy gets one '
            'request. The work comes out six, five and six. It is '
            'registered for one service name only. The name catalogue '
            'still uses round robin.'
        ),
    ),
    dict(
        key='07-down', kind='console', title='A Copy Goes Down',
        body="""FOUR. A copy goes down.
  copy-b stopped.
  12 requests: 4 failed,
  8 answered.""",
        narration=(
            'Fourth, a copy goes down. It is still in the list, so a '
            'third of the requests are sent to it. Four of twelve fail. '
            'The balancer, without health checks, does not know.'
        ),
    ),
    dict(
        key='08-retry', kind='console', title='A Retry Lands Elsewhere',
        body="""FIVE. A retry.
  each request may retry once.
  12 answered.

  the retry is the caller's.""",
        narration=(
            'Fifth, a retry. Allow each request one more attempt, and all '
            'twelve are answered, because the second attempt goes to the '
            "next copy. The retry is the caller's job. The balancer alone "
            'only spreads the failures.'
        ),
    ),
    dict(
        key='09-names', kind='console', title='Only For Names',
        body="""SIX. Only for names.
  an unknown name: fails.
  a real address: fails.

  every host is a service name.""",
        narration=(
            'Last, a trap. A balanced client treats every host as a '
            'service name. A name with no instances fails. So does a real '
            'address, because it is looked up as a name. For a real '
            'address, use an ordinary client.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Default first.', '', 'Add retries or health checks.', '', 'Names, never addresses.', '', 'Replace it when work is uneven.'],
        narration=(
            'My verdict, plainly. Use the default until work is uneven. '
            'Add retries or health checks, because a balancer alone '
            'spreads failures. And use service names, never addresses, on '
            'a balanced client.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['@LoadBalanced on a client builder.', '', 'A URL whose host is a service name.'],
        narration=(
            'How do you recognise this in code you did not write? A load '
            'balanced annotation on a client builder. And a URL whose '
            'host is a service name, not an address.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Any Spring service that calls', 'another by name.'],
        narration=(
            'You have met this in any Spring service that calls another '
            'by name.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'Spring Cloud 2025.1.3.', '', 'LoadBalancer 5.0.3.'],
        narration=(
            'For the record. Spring Boot four point one point one. Spring '
            'Cloud twenty twenty five point one point three. LoadBalancer '
            'five point zero point three.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: real sockets,', 'real HTTP, the real balancer.', '', 'Work is counted in cost units,', 'never timed.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is real: real sockets, real HTTP and the real '
            'balancer. Work is counted in cost units, never timed.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['With one copy of a service,', 'there is nothing to balance.'],
        narration=(
            'So when is it too much? With one copy of a service, there is '
            'nothing to balance.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', "are in the repository. Change copy-c's cost to two", 'and rerun act three.'],
        narration=(
            "That's Load Balancing with Spring Cloud LoadBalancer. [[slnc "
            '250]] If you take one sentence away, take this one: Spring '
            'Cloud LoadBalancer picks per request, and health and speed '
            'are still yours to add. [[slnc 350]] The full source, the '
            'written notes, the diagrams and an animated walkthrough are '
            'all in the repository. [[slnc 300]] If you try one exercise, '
            'change the cost of the slow copy to two, and rerun act '
            'three. [[slnc 300]] If this helped, a like genuinely does '
            'help other people find it, and subscribe if you would like '
            'the rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
