"""Scene definitions for the Claim Check teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Claim Check',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Claim Check pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A claim check stores a large '
            'item somewhere cheap. [[slnc 300]] Then it sends only a '
            'small ticket through the message system. [[slnc 300]] The '
            'receiver hands in the ticket, and collects the item. [[slnc '
            '600]] Think of a cloakroom at a theatre. [[slnc 300]] You '
            'leave your heavy coat at the counter, and get a small '
            'numbered ticket. [[slnc 300]] You carry the ticket, not the '
            'coat. [[slnc 300]] Later, you hand in the ticket, and get '
            'your coat back. [[slnc 700]] In our online store, the big '
            'item is an invoice P D F, which must go to another service. '
            '[[slnc 500]] By the end, you will hear the message system '
            'refuse a big message. [[slnc 300]] A ticket carry it '
            'instead. [[slnc 300]] Items that nobody collected. [[slnc '
            '300]] A changed item caught by a check. [[slnc 300]] And the '
            'bill.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['When an order ships, the store', 'sends the invoice PDF to the', 'mailing service.', '', 'The invoice is 5000 bytes.', 'The broker takes 1000.', '', 'What do we send?'],
        narration=(
            'Here is the scenario. [[slnc 400]] When an order ships, the '
            'store sends the invoice to the mailing service. [[slnc 300]] '
            'The invoice is a P D F of five thousand bytes. [[slnc 500]] '
            'It travels through a message broker. [[slnc 300]] A broker '
            'is a separate program that carries messages between '
            'services. [[slnc 300]] And this broker only accepts messages '
            'up to a thousand bytes. [[slnc 500]] So here is the '
            'question. [[slnc 300]] What do we send?'
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
            'First demo: a message that is too big. [[slnc 400]] The '
            "invoice is five thousand bytes. [[slnc 300]] The broker's "
            'limit is a thousand. [[slnc 300]] So the broker refuses it. '
            '[[slnc 500]] Most brokers limit the size of a message. '
            '[[slnc 300]] And the ones with no limit get slow when '
            'messages are large.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Store the big thing somewhere', 'cheap.', '', 'Send a small ticket: where it is,', 'how big, and a checksum.', '', 'The receiver redeems the ticket,', 'checks it, and lets it go.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Store the big item somewhere '
            'cheap. [[slnc 500]] Send a small ticket through the broker. '
            '[[slnc 300]] The ticket says where the item is, how big it '
            'is, and carries a checksum. [[slnc 300]] A checksum is a '
            'short fingerprint of the data, used to check it has not '
            'changed. [[slnc 500]] The receiver hands in the ticket, and '
            'gets the item. [[slnc 300]] It checks that the item matches '
            'the fingerprint. [[slnc 300]] And then the storage can let '
            'it go.'
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
            'Second demo: send the ticket, not the luggage. [[slnc 400]] '
            'The invoice goes into storage. [[slnc 500]] The message '
            'carries a claim. [[slnc 300]] It holds an identifier, the '
            'size, five thousand bytes, and a checksum. [[slnc 500]] The '
            'receiver hands in the claim. [[slnc 300]] And gets back five '
            'thousand bytes, identical to what was sent.'
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
            'Third demo: how much the broker carries. [[slnc 400]] A '
            'hundred invoices, of five thousand bytes each. [[slnc 500]] '
            'Through a broker with no size limit, that is five hundred '
            'thousand bytes. [[slnc 300]] With claim checks, it is five '
            'thousand nine hundred bytes. [[slnc 500]] The broker carries '
            'small tickets. [[slnc 300]] The storage holds the luggage.'
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
            'Fourth demo: luggage nobody collected. [[slnc 400]] Ten '
            'invoices are sent. [[slnc 300]] Six are collected, and '
            'deleted. [[slnc 300]] So four are still sitting in storage. '
            '[[slnc 500]] After a time limit, a clean-up removes them. '
            '[[slnc 500]] Then a slow receiver arrives, with its claim. '
            '[[slnc 300]] And it finds that its invoice has gone. [[slnc '
            '500]] So stored items need a life span. [[slnc 300]] And the '
            'receiver must cope with a claim that has expired.'
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
            'Fifth demo: is it the same luggage? [[slnc 400]] One byte of '
            'the invoice is changed, while it sits in storage. [[slnc '
            '500]] The receiver compares it with the checksum that came '
            'in the claim. [[slnc 300]] They do not match, so the '
            'receiver refuses it. [[slnc 500]] The checksum in the claim '
            'is what makes the stored item safe to trust.'
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
            'Finally, the bill. [[slnc 400]] One invoice now takes three '
            'storage steps and two broker steps. [[slnc 300]] Before, it '
            'took one. [[slnc 600]] Next, the ticket numbers. [[slnc '
            '300]] If claims simply count up, one, two, three, anyone '
            'holding one can guess the next. [[slnc 300]] In the demo, '
            'the holder of claim one reads the invoice for claim two. '
            '[[slnc 500]] With random claims, a hundred thousand guesses '
            'found nothing. [[slnc 600]] And last, storing and then '
            'sending are two separate steps. [[slnc 300]] If the program '
            'stops between them, the invoice sits in storage, and nobody '
            'has a ticket for it.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A message that holds a URL or an', 'id and a size instead of the data.', '', 'An S3 or blob storage path in an', 'SQS or Kafka message.', '', 'A ClaimCheck or Payload class in', 'an integration library.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a message that holds a link or an I D '
            'and a size, instead of the data itself. [[slnc 300]] Look '
            'for a storage path, such as an Amazon S3 location, inside a '
            'queue message. [[slnc 300]] Look for a class called claim '
            'check, or payload, in an integration library. [[slnc 300]] '
            'Or a storage rule that deletes files after a number of days.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a claim check when payloads', 'are larger than a broker should', 'carry, or when many consumers need', 'only part of the message. Make the', 'claim unguessable and carry a', 'checksum. Give stored payloads a', 'life span, sweep the ones nobody', 'collected, and handle a claim that', 'has expired. Store first, then'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a claim check when '
            'items are bigger than a broker should carry. [[slnc 300]] Or '
            'when many receivers need only part of the message. [[slnc '
            '500]] Make the claim impossible to guess, and include a '
            'checksum. [[slnc 300]] Give stored items a life span. [[slnc '
            '300]] Clean up the ones nobody collected. [[slnc 300]] And '
            'handle a claim that has expired. [[slnc 500]] Store first, '
            'then send. [[slnc 300]] And expect the occasional item with '
            'no ticket.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 300]] "
            'Nothing depends on a real clock, so every run gives the same '
            'result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['If payloads are small, a claim', 'check adds two steps for nothing.', 'If the receiver needs the data at', 'once and storage is slow, the', 'ticket costs more than it saves.'],
        narration=(
            'So, when is this too much? [[slnc 400]] If the messages are '
            'small, a claim check adds two steps for nothing. [[slnc '
            '400]] And if the receiver needs the data at once, and '
            'storage is slow, the ticket costs more than it saves.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Claim Check pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] A claim check '
            'keeps the broker light, and the price is extra steps, '
            'expiry, and a ticket that must be impossible to guess, and '
            'checked. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 300]] It runs offline, with nothing '
            'installed except a Java development kit. [[slnc 500]] Here '
            'is one exercise to try. [[slnc 300]] Make the sender delete '
            'the stored invoice if sending the claim fails. [[slnc 300]] '
            'Then prove it works, with a broker that refuses. [[slnc '
            '500]] If this helped, a like really does help other people '
            "find it. [[slnc 300]] And subscribe, if you'd like the rest "
            'of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
