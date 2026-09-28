"""Scene definitions for the Event-Driven Architecture with Kafka teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Event-Driven Architecture with Kafka',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Event-Driven Architecture pattern, in Java, using Apache '
            'Kafka. [[slnc 300]] This video is presented by Jayasekhar '
            'Konduru. [[slnc 600]] First, a simple definition. [[slnc '
            '300]] In an event-driven system, services do not call each '
            'other. [[slnc 300]] They write facts, called events, to a '
            'shared log, and each service reads that log at its own pace. '
            '[[slnc 500]] With Kafka, that log is called a topic, and it '
            'lives on a server called a broker. [[slnc 300]] The broker '
            'also remembers how far each reading service has got. [[slnc '
            '600]] Think of a library that keeps a bookmark for every '
            'reader. [[slnc 300]] You can leave for a week, come back, '
            'and carry on from the right page. [[slnc 700]] This is the '
            'framework version of the Event-Driven Architecture video. '
            '[[slnc 300]] We keep the same online store, and watch a real '
            'Kafka broker do the work. [[slnc 400]] We will lose an order '
            'the old way, then send events to Kafka, catch up after an '
            'outage, replay history, and finally, look at the cost.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Event-Driven Architecture, the', 'hand-built video, writes facts to', 'a log.', '', 'It shows readers at their own', 'pace, and a reader that catches', 'up.', '', 'If you have not seen it, start', 'there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Event-Driven Architecture video. '
            '[[slnc 400]] That one builds the log itself, in plain Java. '
            '[[slnc 300]] It shows readers working at their own pace, a '
            'reader catching up, and a new reader replaying history. '
            '[[slnc 500]] If you are new to the pattern, watch that one '
            'first. [[slnc 400]] Here, we keep the same example. [[slnc '
            "300]] We won't teach the pattern again. [[slnc 300]] "
            'Instead, we ask what a real tool, Kafka, does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Two things are new: Kafka, and', 'Docker to run it.', '', 'You need Docker running. Without', 'it the demo says so and stops.', '', 'Skipping this video loses none of', 'the pattern.'],
        narration=(
            'So, what is Apache Kafka? [[slnc 400]] Kafka keeps a log of '
            'events on a server, called a broker. [[slnc 400]] Programs '
            'that write events are called producers. [[slnc 300]] They '
            'add events to a topic. [[slnc 400]] Programs that read '
            'events are called consumers. [[slnc 300]] Consumers work in '
            'named groups, and the broker remembers how far each group '
            'has read. [[slnc 500]] To run the demo, you need Docker '
            'running, because the broker runs in a container. [[slnc '
            '300]] Without Docker, the demo tells you so, and stops. '
            '[[slnc 500]] And one promise. [[slnc 300]] If you skip this '
            'video, you lose none of the pattern. [[slnc 300]] This one '
            'is about the tool.'
        ),
    ),
    dict(
        key='04-direct', kind='console', title='Calling And Waiting',
        body="""ONE. Calling each other.
  the order service calls
  shipping and waits.
  shipping is down.
  order accepted: false.

  a customer lost an order.""",
        narration=(
            'First, the old way: services calling each other. [[slnc '
            '400]] The order service calls shipping, and waits for an '
            'answer. [[slnc 300]] But shipping is down. [[slnc 400]] So '
            'the order is not accepted. [[slnc 500]] A customer just lost '
            'their order, because of a service they never even see.'
        ),
    ),
    dict(
        key='05-log', kind='console', title='Telling The Log',
        body="""TWO. Telling the log.
  the order service sends the
  event to Kafka: offset 0.
  it has no reference to inventory
  or shipping.

  both read the topic, and act.""",
        narration=(
            'Second demo: telling the log. [[slnc 400]] The order service '
            'sends its event to Kafka. [[slnc 300]] Kafka stores it at '
            'position zero, called offset zero. [[slnc 300]] And the '
            'order service is finished. [[slnc 400]] It knows nothing '
            'about inventory or shipping. [[slnc 400]] Inventory reads '
            'the topic, and sees the order. [[slnc 300]] Shipping reads '
            'the same topic, and sees it too.'
        ),
    ),
    dict(
        key='06-down', kind='console', title='A Service That Is Down',
        body="""THREE. A service is down.
  shipping read ORD-1, went down.
  3 more orders accepted.
  the broker counts lag 3.

  shipping is back, and catches up
  from where it stopped:
  4 planned, lag 0.""",
        narration=(
            'Third demo: a service that is down. [[slnc 400]] Shipping '
            'reads the first order, and then goes down. [[slnc 400]] '
            'Three more orders arrive, and all three are accepted. [[slnc '
            '400]] The broker reports that shipping is three events '
            'behind. [[slnc 300]] This gap is called lag. [[slnc 500]] '
            'Then shipping comes back. [[slnc 300]] The broker remembers '
            'exactly where it stopped. [[slnc 300]] So shipping carries '
            'on from there, and plans all four orders. [[slnc 300]] Now '
            'the lag is zero.'
        ),
    ),
    dict(
        key='07-new', kind='console', title='A New Reader',
        body="""FOUR. A new reader.
  analytics added after 2 orders.
  it reads the topic from the
  start: ORD-1, ORD-2.

  the order service is untouched.""",
        narration=(
            'Fourth demo: a new reader. [[slnc 400]] After two orders '
            'have been placed, we add a brand new service: analytics. '
            '[[slnc 400]] It reads the topic from the very beginning. '
            '[[slnc 300]] So it sees both earlier orders. [[slnc 400]] '
            'And the order service was not changed at all. [[slnc 400]] '
            'Kafka keeps the events, so a new service can be built from '
            'history.'
        ),
    ),
    dict(
        key='08-late', kind='console', title='Not The Same Instant',
        body="""FIVE. Not the same instant.
  order accepted; stock: 10.
  it should be 9.
  after inventory reads: 9.

  for a moment they disagree.
  eventually consistent.""",
        narration=(
            'Fifth demo: things do not happen at the same instant. [[slnc '
            '400]] An order is accepted. [[slnc 300]] But the stock count '
            'still says ten. [[slnc 300]] It should say nine. [[slnc '
            '400]] A moment later, inventory reads the event, and the '
            'count becomes nine. [[slnc 500]] For that short moment, the '
            'two services disagree. [[slnc 300]] This is called eventual '
            'consistency. [[slnc 300]] The system becomes correct, but '
            'not at every single instant.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  the same event, delivered twice.
  no duplicate check: stock 8.
  with one: 9. right.

  the flow is spread over services:
  read the topic to see it.

  and a broker is another system
  to run.""",
        narration=(
            'Finally, the cost. [[slnc 400]] Kafka can deliver the same '
            'event twice, for example when a reader crashes before saving '
            'its place. [[slnc 400]] Without a duplicate check, the stock '
            'drops twice, to eight. [[slnc 300]] That is wrong. [[slnc '
            '300]] With a duplicate check, it stays at nine, which is '
            'right. [[slnc 500]] Second, the journey of one order is now '
            'spread across several services. [[slnc 300]] To follow it, '
            'you read the topic, not one piece of code. [[slnc 500]] And '
            'third, the broker is one more system you have to run.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['A group for each service.', '', 'Expect readers to be behind.', '', 'Make readers safe to repeat.', '', 'Watch the lag.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a broker when '
            'services must not depend on each other being up, and when '
            'new services will join later. [[slnc 500]] Then follow four '
            'rules. [[slnc 300]] One. [[slnc 200]] Give each service its '
            'own consumer group. [[slnc 300]] Two. [[slnc 200]] Expect '
            'readers to be behind, and design for it. [[slnc 300]] Three. '
            '[[slnc 200]] Make every reader safe to run twice on the same '
            'event. [[slnc 300]] And four. [[slnc 200]] Watch the lag.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['`KafkaProducer` and', '`KafkaConsumer`, or', '`@KafkaListener`.', '', 'A `group.id` for each service.', '', 'Lag dashboards, and `kafka-', 'consumer-groups.sh`.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for the Kafka Producer and Kafka Consumer '
            'classes. [[slnc 300]] Or a method marked with the at Kafka '
            'Listener annotation. [[slnc 400]] Look for a group I D '
            'setting for each service. [[slnc 400]] And look for '
            'dashboards that show lag, or the Kafka consumer groups '
            'command line tool.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Most large event-driven systems:', 'order pipelines, activity feeds', 'and change data capture.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In most large '
            'event-driven systems. [[slnc 300]] Order pipelines, activity '
            'feeds, and systems that copy database changes to other '
            'services.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Apache Kafka 4.3.1.', '', 'Docker 24 or later.'],
        narration=(
            'For the record, here are the versions. [[slnc 300]] Apache '
            'Kafka, four point three point one. [[slnc 300]] And Docker, '
            'version twenty-four or later.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real broker', 'in a container, real offsets, and', 'real consumer groups.', '', 'Each act uses its own one-', 'partition topic, so the counts are', 'exact.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything in it is real. [[slnc 300]] A real broker, '
            'running in a container, with real offsets, and real consumer '
            'groups. [[slnc 400]] Each demo uses its own topic, with a '
            'single partition, so every count you heard is exact.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a small system where all parts', 'are always up together, a direct', 'call is simpler. A broker is a', 'system to run, and to understand.'],
        narration=(
            'So, when is this too much? [[slnc 400]] In a small system '
            'where every part is always up together, a direct call is '
            'simpler. [[slnc 400]] A broker is another system to run, and '
            'another system to understand.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a third reader for a loyalty service, and read the topic from the start..'],
        narration=(
            "That's Event-Driven Architecture with Kafka. [[slnc 400]] If "
            'you remember one sentence, make it this one. [[slnc 300]] '
            "Kafka keeps the log, and each service's place in it, and the "
            'price is a broker to run, and readers that may see an event '
            'twice. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Add a third reader, for a loyalty points service. '
            '[[slnc 300]] And have it read the topic from the very start. '
            '[[slnc 500]] If this helped, a like really does help other '
            "people find it. [[slnc 300]] And subscribe, if you'd like "
            'the rest of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
