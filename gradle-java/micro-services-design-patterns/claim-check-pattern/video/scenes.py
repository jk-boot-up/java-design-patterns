"""Scene definitions for the Claim Check teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Claim Check',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Claim Check '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: a '
            'claim check stores a large payload somewhere cheap, and '
            'sends only a small ticket through the message broker. The '
            'receiver redeems the ticket for the payload, the way you '
            'collect a coat. [[slnc 350]] This is another project in the '
            'microservices category, whose subject is how many small '
            'services stay reliable when they talk to each other. In our '
            'online store, the big thing is an invoice PDF that has to be '
            'sent to another service. [[slnc 300]] By the end you will '
            'see a broker refuse a big message, see a ticket carry it '
            'instead, see how little the broker carries, see luggage '
            'nobody collected, see a changed payload caught by a '
            'checksum, and see the bill, which is extra steps and a '
            'ticket that must be hard to guess.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['When an order ships, the store', 'sends the invoice PDF to the', 'mailing service.', '', 'The invoice is 5000 bytes.', 'The broker takes 1000.', '', 'What do we send?'],
        narration=(
            'Here is the scenario. When an order ships, the online store '
            'sends the invoice, a PDF of five thousand bytes, to the '
            'mailing service through a message broker. The broker accepts '
            'messages of a thousand bytes. [[slnc 300]] The question: '
            'what do we send?'
        ),
    ),
    dict(
        key='03-big', kind='console', title='A Message That Is Too Big',
        body="""ONE. Too big.
  the invoice: 5000 bytes.
  the broker's limit: 1000.
  refused.

  the ones with no limit get
  slow.""",
        narration=(
            'First, a message that is too big. The invoice is five '
            'thousand bytes, and the broker refuses it: it is over its '
            'limit of a thousand. Most brokers cap the size of a message, '
            'and the ones that do not get slow when the messages are '
            'large.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Store the big thing somewhere', 'cheap.', '', 'Send a small ticket: where it is,', 'how big, and a checksum.', '', 'The receiver redeems the ticket,', 'checks it, and lets it go.'],
        narration=(
            'The pattern. Store the big thing somewhere cheap. Send a '
            'small ticket through the broker: where it is, how big it is, '
            'and a checksum. The receiver redeems the ticket, checks that '
            'it is the right thing, and then lets the storage go.'
        ),
    ),
    dict(
        key='05-ticket', kind='console', title='Send The Ticket, Not The Luggage',
        body="""TWO. The ticket.
  the invoice is stored.
  the message carries a claim:
  id, size 5000, checksum.

  the receiver redeems it and
  gets 5000 identical bytes.""",
        narration=(
            'Second, send the ticket, not the luggage. The invoice goes '
            'into storage. The message carries a claim: an identifier, '
            'the size, and a checksum. The receiver redeems the claim, '
            'and gets five thousand bytes, identical to what was sent.'
        ),
    ),
    dict(
        key='06-carried', kind='console', title='What The Broker Carries',
        body="""THREE. Carried.
  100 invoices, 5000 bytes each.
  no limit: 500000 bytes.
  by claim: 5900 bytes.

  the broker moves a ticket.""",
        narration=(
            'Third, what the broker carries. A hundred invoices of five '
            'thousand bytes. Through a broker with no size limit: five '
            'hundred thousand bytes. By claim: five thousand nine '
            'hundred. The broker moves a small ticket. The storage holds '
            'the luggage.'
        ),
    ),
    dict(
        key='07-orphans', kind='console', title='Luggage Nobody Collected',
        body="""FOUR. Uncollected.
  10 sent, 6 collected.
  blobs stored: 4.
  after the time limit: swept.

  a slow receiver arrives:
  the blob for this claim
  expired.""",
        narration=(
            'Fourth, luggage nobody collected. Ten are sent, and six are '
            'collected and deleted. Four blobs are still in storage. '
            'After the time limit, a sweep removes them. And a slow '
            'receiver, arriving later with its claim, finds its blob '
            'gone. The storage needs a life span, and the receiver has to '
            'cope with a claim that expired.'
        ),
    ),
    dict(
        key='08-same', kind='console', title='Is It The Same Luggage?',
        body="""FIVE. The same luggage?
  one byte changed in storage.
  the receiver: the checksum
  does not match.

  the claim's checksum is what
  makes the blob safe to trust.""",
        narration=(
            'Fifth, is it the same luggage? One byte is changed in '
            'storage. The receiver checks the checksum that came in the '
            'claim, and refuses the payload. The checksum in the claim is '
            'what makes a ticket for a blob safe to trust.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  3 storage operations and 2
  broker steps, not 1.

  counting claims: blob-1 reads
  blob-2's invoice.
  random claims: 0 found in
  100000 guesses.

  store-then-send can stop
  between the two.""",
        narration=(
            'Last, the bill. One invoice now takes three storage '
            'operations and two broker steps, where it took one. Claims '
            'that count up let anyone holding one read the next: blob one '
            "reads blob two's invoice. Random claims do not: a hundred "
            'thousand guesses found none. And storing then sending can '
            'stop between the two, leaving luggage nobody has a ticket '
            'for.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A message that holds a URL or an', 'id and a size instead of the data.', '', 'An S3 or blob storage path in an', 'SQS or Kafka message.', '', 'A ClaimCheck or Payload class in', 'an integration library.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'message that holds a URL or an id and a size instead of the '
            'data. An S3 or blob storage path in an SQS or Kafka message. '
            'A ClaimCheck or Payload class in an integration library. A '
            'lifecycle rule that deletes objects after a number of days.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a claim check when payloads', 'are larger than a broker should', 'carry, or when many consumers need', 'only part of the message. Make the', 'claim unguessable and carry a', 'checksum. Give stored payloads a', 'life span, sweep the ones nobody', 'collected, and handle a claim that', 'has expired. Store first, then'],
        narration=(
            'Here is my verdict, plainly. Use a claim check when payloads '
            'are larger than a broker should carry, or when many '
            'consumers need only part of the message. Make the claim '
            'unguessable and carry a checksum. Give stored payloads a '
            'life span, sweep the ones nobody collected, and handle a '
            'claim that has expired. Store first, then send, and expect '
            'the orphan.'
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
        body=['If payloads are small, a claim', 'check adds two steps for nothing.', 'If the receiver needs the data at', 'once and storage is slow, the', 'ticket costs more than it saves.'],
        narration=(
            'So when is it too much? If payloads are small, a claim check '
            'adds two steps for nothing. If the receiver needs the data '
            'at once and storage is slow, the ticket costs more than it '
            'saves.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Claim Check. [[slnc 250]] If you take one sentence "
            'away, take this one: a claim check keeps the broker light, '
            'and the price is extra steps, expiry, and a ticket that must '
            'be unguessable and verified. [[slnc 350]] The full source, '
            'the written notes, the diagrams and an animated walkthrough '
            'are all in the repository, running offline with nothing '
            'installed but a Java development kit. [[slnc 300]] If you '
            'try one exercise, make the sender delete the blob if '
            'publishing the claim fails, and prove it with a broker that '
            'refuses. [[slnc 300]] If this helped, a like genuinely does '
            'help other people find it, and subscribe if you would like '
            'the rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
