"""Scene definitions for the Load Balancing with Spring Cloud LoadBalancer teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Load Balancing with Spring Cloud LoadBalancer',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains '
            'client-side Load Balancing in Java, using Spring Cloud '
            'LoadBalancer. [[slnc 300]] This video is presented by '
            'Jayasekhar Konduru. [[slnc 600]] First, a simple definition. '
            '[[slnc 300]] When a service runs as several copies, the '
            'caller chooses which copy gets each request. [[slnc 300]] '
            'With Spring Cloud LoadBalancer, the caller only writes a '
            'service name. [[slnc 300]] And a balancer picks one copy of '
            'that service, for every request. [[slnc 600]] Think of a '
            'supermarket with several tills, and a sign that simply says: '
            'pay here. [[slnc 300]] Someone behind the sign sends each '
            'shopper to a till. [[slnc 700]] In our online store, the '
            'catalogue service runs as three copies. [[slnc 500]] By the '
            'end, you will hear twelve real requests spread by a real '
            'balancer. [[slnc 300]] Fair turns turn out not to be fast. '
            '[[slnc 300]] A rule of our own. [[slnc 300]] A stopped copy. '
            '[[slnc 300]] And a trap with real addresses.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Client-Side Load Balancing, the', 'hand-built video, chooses among', 'three copies of the catalogue.', '', 'It shows fair is not always fast.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video builds on the plain Java Load Balancing video. '
            '[[slnc 300]] If you have not seen it, start there. [[slnc '
            '500]] That video chooses among three copies of the catalogue '
            'service, with four rules written by hand. [[slnc 300]] And '
            'it shows that a fair rule is not always a fast one. [[slnc '
            '500]] This video uses the same example. [[slnc 300]] It does '
            'not teach the pattern again. [[slnc 300]] It shows what '
            'Spring Cloud LoadBalancer does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Two things are new: Spring Boot, and', 'Spring Cloud LoadBalancer.', '', 'It sits inside the HTTP client.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before any code, what is Spring Cloud LoadBalancer? [[slnc '
            '400]] It is a client-side balancer for Spring. [[slnc 300]] '
            'It sits inside the H T T P client that makes web requests. '
            '[[slnc 500]] The caller uses a service name. [[slnc 300]] '
            'And the balancer picks a copy for every request. [[slnc '
            '300]] By default, it takes turns, which is called round '
            'robin. [[slnc 500]] And a promise. [[slnc 300]] Skipping '
            'this video loses none of the pattern. [[slnc 300]] The plain '
            'Java video teaches all of it.'
        ),
    ),
    dict(
        key='04-rr', kind='console', title='Twelve Requests, One Name',
        body="""ONE. One name.
  12 requests: 4, 4, 4.

  the caller never saw an
  address.""",
        narration=(
            'First demo: the default. [[slnc 400]] Twelve requests go to '
            'the name catalogue. [[slnc 300]] The balancer spreads them '
            'evenly: four, four, and four. [[slnc 500]] The caller only '
            'wrote a name. [[slnc 300]] It never saw a single address.'
        ),
    ),
    dict(
        key='05-fair', kind='console', title='Fair Is Not Fast',
        body="""TWO. Fair, not fast.
  work: 4, 4, 24.

  the slow copy did the most.""",
        narration=(
            'Second demo: fair is not fast. [[slnc 400]] Copy C is on '
            'older hardware. [[slnc 300]] Each request costs it six times '
            'as much work. [[slnc 500]] Round robin still gives it a '
            'third of the requests. [[slnc 300]] So the work comes out as '
            'four, four, and twenty-four. [[slnc 300]] The slowest copy '
            'did the most work.'
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
            'Third demo: a rule of our own. [[slnc 400]] This rule sends '
            'each request to the copy that has done the least work so '
            'far. [[slnc 500]] Now the slow copy gets only one request. '
            '[[slnc 300]] And the work comes out as six, five, and six. '
            '[[slnc 300]] Much more even. [[slnc 500]] This rule is set '
            'up for one service name only. [[slnc 300]] Every other name '
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
            'Fourth demo: a copy goes down. [[slnc 400]] Copy B is '
            'stopped. [[slnc 300]] But it is still in the list of copies. '
            '[[slnc 300]] So a third of the requests are still sent to '
            'it. [[slnc 500]] Four of the twelve fail. [[slnc 300]] '
            'Without health checks, the balancer does not know the copy '
            'is down.'
        ),
    ),
    dict(
        key='08-retry', kind='console', title='A Retry Lands Elsewhere',
        body="""FIVE. A retry.
  each request may retry once.
  12 answered.

  the retry is the caller's.""",
        narration=(
            'Fifth demo: a retry. [[slnc 400]] Now each request may try '
            'once more if it fails. [[slnc 300]] And all twelve are '
            'answered. [[slnc 300]] Because the second attempt goes to '
            "the next copy. [[slnc 500]] The retry is the caller's job. "
            '[[slnc 300]] A balancer on its own only spreads the failures '
            'around.'
        ),
    ),
    dict(
        key='09-names', kind='console', title='Only For Names',
        body="""SIX. Only for names.
  an unknown name: fails.
  a real address: fails.

  every host is a service name.""",
        narration=(
            'Last demo: a trap. [[slnc 400]] A balanced client treats '
            'every host as a service name. [[slnc 500]] A name with no '
            'copies behind it fails. [[slnc 300]] But so does a real web '
            'address. [[slnc 300]] Because it is looked up as if it were '
            'a service name. [[slnc 500]] So for a real address, use an '
            'ordinary client, not a balanced one.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Default first.', '', 'Add retries or health checks.', '', 'Names, never addresses.', '', 'Replace it when work is uneven.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use the default rule, '
            'until the work is uneven. [[slnc 300]] Add retries, or '
            'health checks, because a balancer on its own just spreads '
            'failures. [[slnc 300]] And on a balanced client, use service '
            'names, never real addresses.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['@LoadBalanced on a client builder.', '', 'A URL whose host is a service name.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for a load balanced annotation on a client '
            'builder. [[slnc 300]] And look for a web address whose host '
            'is a service name, not a real address.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Any Spring service that calls', 'another by name.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In any Spring '
            'service that calls another service by name.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'Spring Cloud 2025.1.3.', '', 'LoadBalancer 5.0.3.'],
        narration=(
            'For the record, here is what was used. [[slnc 300]] Spring '
            'Boot, version four point one point one. [[slnc 300]] Spring '
            'Cloud, release twenty twenty-five point one point three. '
            '[[slnc 300]] And Spring Cloud LoadBalancer, version five '
            'point zero point three.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: real sockets,', 'real HTTP, the real balancer.', '', 'Work is counted in cost units,', 'never timed.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is real: real network connections, real web '
            'requests, and the real balancer. [[slnc 300]] Work is '
            'counted in units of cost, not timed. [[slnc 300]] So every '
            'run gives the same result.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['With one copy of a service,', 'there is nothing to balance.'],
        narration=(
            'So, when is this too much? [[slnc 400]] With only one copy '
            'of a service, there is nothing to balance.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', "are in the repository. Change copy-c's cost to two", 'and rerun act three.'],
        narration=(
            "That's Load Balancing, with Spring Cloud LoadBalancer. "
            '[[slnc 400]] If you remember one sentence, make it this one. '
            '[[slnc 300]] Spring Cloud LoadBalancer picks a copy for '
            'every request, but checking health and speed is still your '
            'job. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Change the cost of the slow copy from six to two. '
            '[[slnc 300]] Then run the third demo again, and see how the '
            'work is shared. [[slnc 500]] If this helped, a like really '
            'does help other people find it. [[slnc 300]] And subscribe, '
            "if you'd like the rest of the series. [[slnc 400]] Thanks "
            'for watching.'
        ),
    ),
]
