"""Scene definitions for the Service Discovery with Spring Cloud Consul teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Service Discovery with Spring Cloud Consul',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Service Registry '
            'and Discovery pattern with Spring Cloud Consul, in Java, and '
            'it is written and presented by Jayasekhar Konduru. [[slnc '
            '300]] It is the framework version of the Service Registry '
            'and Discovery video. That one let three copies of the '
            'Pricing service announce themselves to a shared registry, so '
            'a caller asked for an address each time instead of holding '
            'one, and showed that a registry is only as good as its last '
            'update. This one shows the same idea inside Spring Cloud '
            'Consul. [[slnc 350]] The plain definition, in short: with '
            'Spring Cloud Consul, a service registers itself when it '
            'starts, and a client asks the registry for healthy copies by '
            'name. [[slnc 300]] By the end you will see three real copies '
            'register themselves with a real Consul, see requests find '
            'them by name, and then see the two ways the list can be '
            'wrong: a crash that is not noticed at once, and a registry '
            'that is gone.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Service Registry and Discovery, the', 'hand-built video, lets three copies', 'of Pricing announce themselves.', '', 'It shows a registry is only as good', 'as its last update.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video assumes the Service Registry and Discovery video. '
            'If you have not seen it, start there. It lets three copies '
            'of the Pricing service announce themselves to a shared '
            'registry, so a caller asks for an address each time, and '
            'shows that a registry is only as good as its last update. '
            '[[slnc 300]] This one uses the same example. It does not '
            'teach the pattern again. It shows what Spring Cloud Consul '
            'does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Three things are new: Spring Cloud', 'Consul, a real Consul agent, and', "Spring Boot's web server.", '', 'You need the consul program', 'installed. Without it the demo says', 'so and stops.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first line of code, what Spring Cloud Consul is. '
            'Consul is a registry from HashiCorp. Spring Cloud Consul '
            'registers a Spring application with it when it starts, adds '
            'a health check, and lets a client ask for healthy copies by '
            'name. [[slnc 300]] And a promise: skipping this video loses '
            'none of the pattern. The hand-built one teaches all of it.'
        ),
    ),
    dict(
        key='04-register', kind='console', title='Three Copies Announce Themselves',
        body="""ONE. Announced.
  the client has a name, no
  address.

  Consul lists three copies.

  each registered itself.""",
        narration=(
            'First, three copies of Pricing start. Consul lists all '
            'three. Nobody told it. Each copy registered itself when it '
            'started, with a health check. The client has only the name, '
            'pricing.'
        ),
    ),
    dict(
        key='05-find', kind='console', title='Requests Find Them',
        body="""TWO. Found.
  six requests to the name:
  2, 2, 2.""",
        narration=(
            'Second, the client asks by name. Six requests, answered two, '
            'two and two by the three copies. The list came from Consul, '
            'and the choice came from the balancer.'
        ),
    ),
    dict(
        key='06-deploy', kind='console', title='A Deployment Moves A Copy',
        body="""THREE. A deployment.
  pricing-1 restarted on a
  new port.

  hardcoded: fails.
  by name: 2, 2, 2.""",
        narration=(
            'Third, a deployment. Pricing one restarts on a new port. The '
            'address someone wrote down now fails. Asking by name still '
            'works, and pricing one is back in the list, at its new port.'
        ),
    ),
    dict(
        key='07-stop', kind='console', title='A Graceful Stop Is Noticed At Once',
        body="""FOUR. A graceful stop.
  pricing-3 stopped.
  listed at once: 1 and 2.

  six requests: 3, 3.""",
        narration=(
            'Fourth, a graceful stop. Pricing three shuts down properly '
            'and removes itself. The list shrinks at once. The six '
            'requests split three and three.'
        ),
    ),
    dict(
        key='08-crash', kind='console', title='A Crash Is Not',
        body="""FIVE. A crash.
  pricing-2 crashed, silently.
  still listed.
  3 of 6 requests fail.

  after its check fails:
  removed, and 6 of 6 work.""",
        narration=(
            'Fifth, a crash. Pricing two stops answering, and says '
            'nothing. Consul still lists it. Three of six requests fail. '
            '[[slnc 300]] Then its health check fails, and Consul removes '
            'it. Now all six work. The list is only as good as its last '
            "check. That is the taxi rank's catch."
        ),
    ),
    dict(
        key='09-gone', kind='console', title='The Registry Itself Goes Away',
        body="""SIX. No registry.
  Consul stopped.
  asking for pricing:
  an error.

  the client kept nothing.""",
        narration=(
            'Last, the registry goes away. The client asks for pricing '
            'and gets an error. It kept no list of its own. Remembering '
            "the last good list is the client's job."
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Register at startup.', '', 'Choose the check interval.', '', 'Retry across copies.', '', 'Remember the last list.'],
        narration=(
            'My verdict, plainly. Register at startup, and deregister on '
            'shutdown. Choose the health check interval on purpose. '
            'Expect stale entries after a crash, and retry across copies. '
            'And give the client a last known good list for the day the '
            'registry is down.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['spring.cloud.consul in', 'configuration.', '', 'A URL whose host is a service name.', '', 'A health endpoint a registry calls.'],
        narration=(
            'How do you recognise this in code you did not write? '
            'Settings under spring cloud consul. A URL whose host is a '
            'service name. And a health endpoint that a registry calls.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Platforms that run many small', 'services that must find each other.'],
        narration=(
            'You have met this in platforms that run many small services '
            'that must find each other.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'Spring Cloud 2025.1.3.', '', 'Consul 1.16 or later.'],
        narration=(
            'For the record. Spring Boot four point one point one. Spring '
            'Cloud twenty twenty five point one point three. And Consul '
            'one point sixteen or later.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real Consul,', 'real registrations and real', 'health checks.', '', 'The demo waits for a check to fail,', 'so it takes about half a minute.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is real: a real Consul, real registrations and '
            'real health checks. The demo waits for a check to fail, so '
            'it takes about half a minute.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['With three services on fixed hosts,', 'a configuration file is simpler.'],
        narration=(
            'So when is it too much? With three services on fixed hosts '
            'that rarely change, a configuration file is simpler than a '
            'registry.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Change the check interval and', 'rerun act five.'],
        narration=(
            "That's Service Discovery with Spring Cloud Consul. [[slnc "
            '250]] If you take one sentence away, take this one: a real '
            'registry lists what passed its last check, and the client '
            'must plan for the rest. [[slnc 350]] The full source, the '
            'written notes, the diagrams and an animated walkthrough are '
            'all in the repository. [[slnc 300]] If you try one exercise, '
            'change the check interval, and rerun act five. [[slnc 300]] '
            'If this helped, a like genuinely does help other people find '
            'it, and subscribe if you would like the rest of the series. '
            '[[slnc 250]] Thanks for watching.'
        ),
    ),
]
