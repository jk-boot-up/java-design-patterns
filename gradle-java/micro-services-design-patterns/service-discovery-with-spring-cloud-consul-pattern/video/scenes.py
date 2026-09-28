"""Scene definitions for the Service Discovery with Spring Cloud Consul teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Service Discovery with Spring Cloud Consul',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Service Discovery pattern in Java, using Spring Cloud '
            'Consul. [[slnc 300]] This video is presented by Jayasekhar '
            'Konduru. [[slnc 600]] First, a simple definition. [[slnc '
            '300]] Services add themselves to a shared list, called a '
            'registry, when they start. [[slnc 300]] A caller asks the '
            'registry for a service by name, instead of holding a fixed '
            'address. [[slnc 600]] Think of a taxi rank. [[slnc 300]] '
            'Drivers join it when their shift starts, and you take '
            'whoever is at the front. [[slnc 600]] With Spring Cloud '
            'Consul, a service registers itself when it starts. [[slnc '
            '300]] And a client asks the registry for healthy copies, by '
            'name. [[slnc 700]] In our online store, the pricing service '
            'runs as three copies. [[slnc 500]] By the end, you will hear '
            'three real copies register with a real Consul. [[slnc 300]] '
            'Requests find them by name. [[slnc 300]] And the two ways '
            'the list can be wrong: a crash that is not noticed at once, '
            'and a registry that is gone.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Service Registry and Discovery, the', 'hand-built video, lets three copies', 'of Pricing announce themselves.', '', 'It shows a registry is only as good', 'as its last update.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video builds on the plain Java Service Discovery video. '
            '[[slnc 300]] If you have not seen it, start there. [[slnc '
            '500]] That video lets three copies of the pricing service '
            'announce themselves to a shared registry. [[slnc 300]] So a '
            'caller asks for an address each time. [[slnc 300]] And it '
            'shows that a registry is only as good as its last update. '
            '[[slnc 500]] This video uses the same example. [[slnc 300]] '
            'It does not teach the pattern again. [[slnc 300]] It shows '
            'what Spring Cloud Consul does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Three things are new: Spring Cloud', 'Consul, a real Consul agent, and', "Spring Boot's web server.", '', 'You need the consul program', 'installed. Without it the demo says', 'so and stops.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before any code, what is Spring Cloud Consul? [[slnc 400]] '
            'Consul is a registry, made by a company called HashiCorp. '
            '[[slnc 500]] Spring Cloud Consul registers a Spring '
            'application with Consul when it starts. [[slnc 300]] It adds '
            'a health check, which Consul calls regularly to see if the '
            'service is alive. [[slnc 300]] And it lets a client ask for '
            'healthy copies, by name. [[slnc 500]] To run this demo, you '
            'need the Consul program installed. [[slnc 300]] Without it, '
            'the demo says so, and stops. [[slnc 500]] And a promise. '
            '[[slnc 300]] Skipping this video loses none of the pattern. '
            '[[slnc 300]] The plain Java video teaches all of it.'
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
            'First demo: three copies announce themselves. [[slnc 400]] '
            'Three copies of pricing start. [[slnc 300]] And Consul lists '
            'all three. [[slnc 500]] Nobody told Consul about them. '
            '[[slnc 300]] Each copy registered itself when it started, '
            'with a health check. [[slnc 500]] The client only knows the '
            'name: pricing.'
        ),
    ),
    dict(
        key='05-find', kind='console', title='Requests Find Them',
        body="""TWO. Found.
  six requests to the name:
  2, 2, 2.""",
        narration=(
            'Second demo: requests find them. [[slnc 400]] The client '
            'asks by name. [[slnc 300]] Six requests are answered two, '
            'two, and two, by the three copies. [[slnc 500]] The list '
            'came from Consul. [[slnc 300]] And the choice of which copy '
            'came from a load balancer.'
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
            'Third demo: a new release moves a copy. [[slnc 400]] Pricing '
            'one restarts, on a new port. [[slnc 500]] An address someone '
            'wrote down now fails. [[slnc 300]] But asking by name still '
            'works. [[slnc 300]] Pricing one is back in the list, at its '
            'new port.'
        ),
    ),
    dict(
        key='07-stop', kind='console', title='A Graceful Stop Is Noticed At Once',
        body="""FOUR. A graceful stop.
  pricing-3 stopped.
  listed at once: 1 and 2.

  six requests: 3, 3.""",
        narration=(
            'Fourth demo: a polite shutdown is noticed at once. [[slnc '
            '400]] Pricing three shuts down properly, and removes itself '
            'from Consul. [[slnc 300]] The list shrinks straight away. '
            '[[slnc 300]] And six requests split three and three.'
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
            'Fifth demo: a crash is not noticed at once. [[slnc 400]] '
            'Pricing two stops answering, and says nothing. [[slnc 300]] '
            'Consul still lists it. [[slnc 300]] So three of the six '
            'requests fail. [[slnc 600]] Then its health check fails, and '
            'Consul removes it. [[slnc 300]] Now all six requests work. '
            '[[slnc 500]] The list is only as good as its last check. '
            "[[slnc 300]] That is the taxi rank's catch."
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
            'Last demo: the registry itself goes away. [[slnc 400]] '
            'Consul is stopped. [[slnc 300]] The client asks for pricing, '
            'and gets an error. [[slnc 500]] It kept no list of its own. '
            "[[slnc 300]] Remembering the last good list is the client's "
            'job.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Register at startup.', '', 'Choose the check interval.', '', 'Retry across copies.', '', 'Remember the last list.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Register when the '
            'service starts, and remove it when it shuts down. [[slnc '
            '300]] Choose how often the health check runs, on purpose. '
            '[[slnc 300]] Expect out-of-date entries after a crash, and '
            'retry on another copy. [[slnc 300]] And give the client a '
            'last known good list, for the day the registry is down.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['spring.cloud.consul in', 'configuration.', '', 'A URL whose host is a service name.', '', 'A health endpoint a registry calls.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for Spring Cloud Consul settings in the '
            'configuration file. [[slnc 300]] Look for a web address '
            'whose host is a service name. [[slnc 300]] And look for a '
            'health endpoint that a registry calls.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Platforms that run many small', 'services that must find each other.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In any platform '
            'that runs many small services that must find each other.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'Spring Cloud 2025.1.3.', '', 'Consul 1.16 or later.'],
        narration=(
            'For the record, here is what was used. [[slnc 300]] Spring '
            'Boot, version four point one point one. [[slnc 300]] Spring '
            'Cloud, release twenty twenty-five point one point three. '
            '[[slnc 300]] And Consul, version one point sixteen or later.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real Consul,', 'real registrations and real', 'health checks.', '', 'The demo waits for a check to fail,', 'so it takes about half a minute.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is real: a real Consul, real registrations, and '
            'real health checks. [[slnc 300]] The demo waits for a health '
            'check to fail. [[slnc 300]] So it takes about half a minute '
            'to run.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['With three services on fixed hosts,', 'a configuration file is simpler.'],
        narration=(
            'So, when is this too much? [[slnc 400]] With three services '
            'on fixed machines that rarely change, a settings file is '
            'simpler than a registry.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Change the check interval and', 'rerun act five.'],
        narration=(
            "That's Service Discovery, with Spring Cloud Consul. [[slnc "
            '400]] If you remember one sentence, make it this one. [[slnc '
            '300]] A real registry lists what passed its last health '
            'check, and the client must plan for everything else. [[slnc '
            '500]] The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 500]] '
            'Here is one exercise to try. [[slnc 300]] Change how often '
            'the health check runs. [[slnc 300]] Then run the fifth demo '
            'again, and see how long the crashed copy stays listed. '
            '[[slnc 500]] If this helped, a like really does help other '
            "people find it. [[slnc 300]] And subscribe, if you'd like "
            'the rest of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
