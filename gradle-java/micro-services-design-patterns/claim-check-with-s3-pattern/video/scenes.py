"""Scene definitions for the Claim Check with S3 teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks every count out loud, says each of the services' words in plain
language before using Amazon's name for it, and never points at a picture the
listener cannot see. Every figure is the output of `./gradlew run`.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Claim Check with S3',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Claim Check pattern in Java, using real Amazon storage and a '
            'real Amazon queue, running on your own machine. [[slnc 300]] '
            'This video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] When something is '
            'too big to send in a message, you put it in storage, and '
            'send a small ticket instead. [[slnc 300]] Whoever receives '
            'the ticket uses it to fetch the real thing. [[slnc 600]] It '
            'works like the left-luggage office at a railway station. '
            '[[slnc 300]] You leave your heavy suitcase at the counter, '
            'and carry a small paper ticket. [[slnc 300]] Later, the '
            'ticket gets your suitcase back. [[slnc 700]] In our online '
            'store, checkout has an invoice to hand to the email service. '
            '[[slnc 300]] The invoice is a big P D F file. [[slnc 300]] '
            'So checkout puts the P D F in storage, and sends the email '
            'service a ticket saying where to find it. [[slnc 500]] By '
            'the end, you will hear a real queue refuse an invoice. '
            '[[slnc 300]] A ticket bring it back, byte for byte. [[slnc '
            '300]] Luggage that nobody collects. [[slnc 300]] A delete '
            'that deletes nothing. [[slnc 300]] And the bill.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Checkout makes an invoice PDF.', 'The email service sends it out.', '',
              'A queue sits between them.', 'A queue carries text, and it has', 'a size limit.', '',
              'The hand-built partner project', 'made up its own limit.', '',
              'This time the limit is Amazon\'s,', 'and so are the error messages.'],
        narration=(
            'Here is the scenario. [[slnc 400]] Checkout makes an '
            'invoice, as a P D F file. [[slnc 300]] The email service '
            'sends it to the customer. [[slnc 300]] They are two separate '
            'programs, with a queue between them. [[slnc 500]] A queue is '
            'a waiting line for messages. [[slnc 300]] One program puts a '
            'message in, and another takes it out later. [[slnc 300]] So '
            'checkout can hand the work over, and carry on. [[slnc 600]] '
            'The plain Java version of this project used a queue with a '
            'size limit it made up. [[slnc 300]] This time, the queue is '
            "Amazon's queue service, and the storage is Amazon's storage "
            "service. [[slnc 300]] The limits are Amazon's, and so are "
            'the error messages.'
        ),
    ),
    dict(
        key='03-one', kind='console', title='An Invoice Too Big For The Queue',
        body="""ONE. An invoice too big for the queue.
  longest message: 1048576 bytes.

  a PDF of 1500000 bytes.
  as base64: 2000000 characters.

  SQS refuses it:
  Message must be shorter than
  1048576 bytes.""",
        narration=(
            'First demo: an invoice that is too big for the queue. [[slnc '
            '400]] The queue service is called S Q S, short for Simple '
            'Queue Service. [[slnc 500]] The demo asks it how long a '
            'message may be. [[slnc 300]] The answer is just over one '
            "million bytes. [[slnc 500]] A business customer's monthly "
            'invoice is one and a half million bytes. [[slnc 300]] But a '
            'message must be text. [[slnc 300]] So the P D F is first '
            'written out as letters, in a format called base sixty-four. '
            '[[slnc 300]] That makes two million characters. [[slnc 500]] '
            'S Q S refuses it. [[slnc 300]] It says the message must be '
            'shorter than its limit. [[slnc 300]] That is not a rule this '
            'program made up. [[slnc 300]] It is the real service saying '
            'no.'
        ),
    ),
    dict(
        key='04-words', kind='bullets', title="The Services' Words",
        body=['Storage: Amazon S3.', 'A bucket is a named storage room.',
              'An object is one stored file.', 'A key is the name it is stored under.', '',
              'Queue: Amazon SQS.', 'A message is one piece of text.', '',
              'LocalStack plays both, on this', 'machine, in one container.'],
        narration=(
            'The real services bring a few words with them. [[slnc 300]] '
            'Each one is simpler than it sounds. [[slnc 300]] Think of '
            'the left-luggage office again. [[slnc 500]] The office is '
            'the storage service, called S three, short for Simple '
            'Storage Service. [[slnc 300]] A storage room in it is called '
            'a bucket. [[slnc 300]] One suitcase on the shelf is called '
            'an object. [[slnc 300]] That is just a stored file. [[slnc '
            "300]] And the name on the suitcase's tag, the name you fetch "
            'it by, is called a key. [[slnc 500]] The queue is S Q S, and '
            'one piece of text in it is called a message. [[slnc 600]] '
            'Neither service is really on Amazon here. [[slnc 300]] A '
            'program called LocalStack answers exactly as they would. '
            '[[slnc 300]] It runs in a container, a small sealed box on '
            'this machine. [[slnc 300]] The demo switches it on at the '
            'start, and off at the end.'
        ),
    ),
    dict(
        key='05-base64', kind='bullets', title='Why A Smaller PDF Fails Too',
        body=['A PDF is raw bytes.', 'A message must be text.', '',
              'Base64 spells every 3 bytes', 'with 4 letters.', '',
              '786432 bytes -> 1048576: accepted.', '786433 bytes -> 1048580: refused.', '',
              'The PDF must be three quarters', 'of the limit, not under it.'],
        narration=(
            'Here is the surprise in the first demo. [[slnc 400]] A P D F '
            'is raw bytes, and a message must be text. [[slnc 300]] So '
            'the bytes are spelled out with letters. [[slnc 300]] That '
            'spelling uses four letters for every three bytes. [[slnc '
            '300]] So the file grows by a third on the way in. [[slnc '
            '500]] The demo tests the edge. [[slnc 300]] A P D F of about '
            'seven hundred and eighty-six thousand bytes becomes exactly '
            'the limit, and is accepted. [[slnc 300]] One byte more, and '
            'it is refused. [[slnc 500]] So a file does not fit just '
            'because it is under the limit. [[slnc 300]] It only fits if '
            'it is under three quarters of the limit.'
        ),
    ),
    dict(
        key='06-two', kind='console', title='Send The Ticket, Not The Luggage',
        body="""TWO. Send the ticket, not the luggage.
  PDF stored in an S3 bucket under
  a random key of 36 characters.

  the ticket is 113 bytes of text:
  bucket, key, size 1500000,
  checksum bb8711d26a6daf29.

  fetched 1500000 bytes, identical: true.
  objects left: 0. messages waiting: 0.""",
        narration=(
            'Second demo: send the ticket, not the luggage. [[slnc 400]] '
            'Checkout puts the P D F in an S three bucket. [[slnc 300]] '
            'It is stored under a random key, thirty-six characters long, '
            'that nobody could guess. [[slnc 300]] Only then does '
            'checkout send a ticket. [[slnc 500]] The ticket is only a '
            'hundred and thirteen bytes of text. [[slnc 300]] It names '
            'the bucket, the key, the size, and a checksum. [[slnc 300]] '
            'A checksum is a short fingerprint worked out from every byte '
            'of the file. [[slnc 300]] If one byte changes, the '
            'fingerprint changes. [[slnc 500]] The email service takes '
            'the ticket, and fetches one and a half million bytes. [[slnc '
            '300]] It checks the fingerprint, and the file is identical '
            'to what was sent. [[slnc 300]] Then it deletes the stored '
            'file. [[slnc 300]] And only after that, it deletes the '
            'message. [[slnc 300]] Nothing is left in either service.'
        ),
    ),
    dict(
        key='07-diagram', kind='diagram', title='Where The Invoice Lives',
        body=None,
        narration=(
            'Here is the whole picture, in words. [[slnc 400]] There are '
            'four parts, in order. [[slnc 500]] First, checkout. [[slnc '
            '300]] It stores the P D F, and then sends the ticket. [[slnc '
            '400]] Second, the S three bucket. [[slnc 300]] It holds the '
            'P D F under its key, however big it is. [[slnc 400]] Third, '
            'the S Q S queue. [[slnc 300]] It carries only the ticket, '
            'about a hundred bytes. [[slnc 400]] Fourth, the email '
            'service. [[slnc 300]] It takes the ticket, fetches the P D '
            'F, checks the fingerprint, and then clears up both. [[slnc '
            '600]] The rule that holds it together is the order. [[slnc '
            '300]] Store before you send. [[slnc 300]] And delete the '
            'message only after the file has been fetched and checked.'
        ),
    ),
    dict(
        key='08-three', kind='console', title='Luggage Nobody Collected',
        body="""THREE. Luggage nobody collected.
  10 sent by ticket, 6 collected.
  S3 still holds 4 invoices,
  SQS still holds 4 tickets.

  an 11th invoice is stored, then
  its send fails: The specified
  queue does not exist.

  S3 holds 5, SQS holds 4 tickets.
  1 invoice has no ticket.""",
        narration=(
            'Third demo: luggage nobody collected. [[slnc 400]] Checkout '
            'sends ten invoices by ticket. [[slnc 300]] The email service '
            'collects six, and then stops. [[slnc 300]] So S three still '
            'holds four invoices, and S Q S still holds four tickets for '
            'them. [[slnc 300]] That is fine. [[slnc 300]] They will be '
            'collected later. [[slnc 600]] Then an eleventh invoice is '
            'stored. [[slnc 300]] But the send that should follow it '
            'fails. [[slnc 300]] The queue says it does not exist. [[slnc '
            '500]] Now storage holds five invoices, but the queue holds '
            'only four tickets. [[slnc 300]] One invoice has no ticket at '
            'all. [[slnc 300]] And nobody will ever ask for it. [[slnc '
            '500]] Storing and sending are two separate steps. [[slnc '
            '300]] And a program can stop between them.'
        ),
    ),
    dict(
        key='09-four', kind='console', title='The Same Key, Twice',
        body="""FOUR. The same key, twice.
  stored under invoices/ORD-1042.pdf,
  ticket sent.

  a corrected invoice, same key.
  S3 keeps 1 object.

  the first ticket is redeemed:
  the payload is not the one
  that was sent: the checksum
  does not match.""",
        narration=(
            'Fourth demo: the same key, used twice. [[slnc 400]] This '
            'bucket names each file after its order. [[slnc 300]] So the '
            'invoice for order ten forty-two is stored under a key made '
            'from that order number. [[slnc 300]] And its ticket is sent. '
            '[[slnc 500]] Then a corrected invoice for the same order is '
            'stored under the same key. [[slnc 300]] Before the first '
            'ticket has been collected. [[slnc 300]] S three keeps only '
            'one file. [[slnc 300]] The new file has quietly replaced the '
            'old one. [[slnc 500]] The email service redeems the first '
            'ticket. [[slnc 300]] The fingerprint on the ticket does not '
            'match the file it gets back. [[slnc 300]] So it refuses to '
            'send it. [[slnc 500]] Without that checksum, a customer '
            'would have received an invoice nobody meant to send.'
        ),
    ),
    dict(
        key='10-versions', kind='console', title='A Delete That Deletes Nothing',
        body="""  versioning on. first ticket,
  identical to the first invoice: true.

  the key is deleted as before.
  keys listed: 0.
  versions still stored: 2.
  delete markers: 1.

  deleting each version by its id:
  0 stored.""",
        narration=(
            'S three has an answer to that, and it has a catch. [[slnc '
            '400]] A bucket can be told to keep every version of every '
            'file. [[slnc 300]] This is called versioning. [[slnc 300]] '
            'Storing under a key that is already used then adds a new '
            'version, and the old one stays. [[slnc 300]] Each version '
            'has its own I D, and the ticket carries it. [[slnc 300]] So '
            'now, the first ticket gets the first invoice, exactly. '
            '[[slnc 600]] Here is the catch. [[slnc 300]] The email '
            'service deletes the key, just as before. [[slnc 300]] A '
            'listing of the bucket now shows no files at all. [[slnc '
            '300]] But two versions are still stored, and still paid for. '
            '[[slnc 500]] The delete only added a marker, a note saying '
            'the key is deleted. [[slnc 300]] This is called a delete '
            'marker. [[slnc 300]] Only deleting each version by its own I '
            'D really empties the bucket.'
        ),
    ),
    dict(
        key='11-five', kind='console', title='How Long Each One Waits',
        body="""FIVE. How long each one waits.
  S3 rule: remove after 1 day.
  expires at a midnight UTC, between
  24 and 48 hours away: true.

  SQS keeps a ticket 345600 seconds,
  which is 4 days.

  tickets still waiting: 1.
  redeem: The specified key
  does not exist.""",
        narration=(
            'Fifth demo: how long each one waits. [[slnc 400]] Luggage '
            'nobody collects has to be cleared away eventually. [[slnc '
            '300]] S three can do that by itself. [[slnc 300]] A rule '
            'removes every file a set number of days after it was stored. '
            '[[slnc 300]] This is called a lifecycle rule, and its '
            'smallest unit is one whole day. [[slnc 500]] So the invoice '
            'is marked to expire at a midnight, between one and two days '
            'away. [[slnc 600]] The queue has its own clock. [[slnc 300]] '
            'It keeps a ticket that nobody has taken for four days. '
            '[[slnc 600]] The demo cannot wait a day, so it removes the '
            'invoice just as the rule would. [[slnc 300]] One ticket is '
            'still waiting. [[slnc 300]] A slow email service redeems it. '
            '[[slnc 300]] And S three says the key does not exist. [[slnc '
            '500]] The ticket outlived its luggage.'
        ),
    ),
    dict(
        key='12-six', kind='console', title='The Bill',
        body="""SIX. The bill.
  a 600000-byte invoice sent whole:
  3 requests. queue carried 800000.

  by ticket: 6 requests.
  PutObject, SendMessage,
  ReceiveMessage, GetObject,
  DeleteObject, DeleteMessage.
  queue carried 117 bytes.

  1 container for 1 queue service
  and 1 storage service.""",
        narration=(
            'Finally, the bill. [[slnc 400]] The demo counts every '
            'request the two services receive. [[slnc 500]] An ordinary '
            'invoice of six hundred thousand bytes is small enough to '
            'send whole. [[slnc 300]] That takes three requests: send, '
            'receive, and delete the message. [[slnc 300]] And the queue '
            'carries eight hundred thousand bytes of text. [[slnc 600]] '
            'The same invoice sent by ticket takes six requests. [[slnc '
            '300]] Store the file. [[slnc 200]] Send the ticket. [[slnc '
            '200]] Receive it. [[slnc 200]] Fetch the file. [[slnc 200]] '
            'Delete the file. [[slnc 200]] Delete the message. [[slnc '
            '500]] But the queue carries only a hundred and seventeen '
            'bytes. [[slnc 600]] So the ticket costs twice the requests, '
            'and two services to run and pay for. [[slnc 300]] And there '
            'is a gap between storing and sending.'
        ),
    ),
    dict(
        key='13-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['It got the shape right: store,', 'send a ticket, redeem, check,', 'clear up, expire.', '',
              'It left out:', '',
              'A limit that is the service\'s,', 'measured in text, not bytes.',
              'A key that can be overwritten.', 'A delete that keeps the bytes.'],
        narration=(
            'The plain Java version got the shape right. [[slnc 400]] '
            'Store the luggage, send a ticket, redeem it, check the '
            'fingerprint, clear up, and expire what nobody collects. '
            '[[slnc 300]] All of that holds on real S three and S Q S. '
            '[[slnc 600]] But it left out three things. [[slnc 500]] '
            'First, its limit was a number it chose, and it counted '
            'bytes. [[slnc 300]] The real limit counts text. [[slnc 300]] '
            'So a file that looks small enough grows by a third, and is '
            'refused. [[slnc 500]] Second, its storage never let two '
            'files share a name. [[slnc 500]] And third, its delete '
            'really deleted. [[slnc 300]] A versioned bucket keeps every '
            'byte, and bills you for it.'
        ),
    ),
    dict(
        key='14-verdict', kind='bullets', title='The Verdict',
        body=['Use a claim check when a payload', 'will not fit, or should not travel.', '',
              'Then say four things out loud:', '',
              '1. Random keys, never reused.', '2. A checksum on every ticket.',
              '3. Store first, and sweep what', '   nobody claims.',
              '4. Keep the ticket\'s clock shorter', '   than the luggage\'s.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a claim check when '
            'a file will not fit in a message, or should not travel '
            'through one. [[slnc 500]] Then settle four things, because '
            'neither service will assume them. [[slnc 500]] One. [[slnc '
            '200]] Store every file under a random key, and never reuse '
            'one. [[slnc 400]] Two. [[slnc 200]] Put a checksum on every '
            'ticket, and check it before you trust the file. [[slnc 400]] '
            'Three. [[slnc 200]] Store first, then send. [[slnc 300]] And '
            'have a rule that clears away what nobody claims. [[slnc '
            '400]] Four. [[slnc 200]] Make the queue forget a ticket '
            'before storage forgets the file. [[slnc 300]] So no ticket '
            'outlives its luggage.'
        ),
    ),
    dict(
        key='15-real', kind='bullets', title='What Is Real, And When Not',
        body=['LocalStack 4.14.0, held back: later', 'images need an account.',
              'AWS SDK for Java 2.55.3,', 'Testcontainers 2.0.5.', '',
              'Too much if payloads are small,', 'or if the receiver needs the data',
              'at once and storage is slow.', '',
              'Two services, not one.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] Both '
            'services are played by LocalStack, version four point '
            'fourteen, in a container the demo starts and stops by '
            'itself. [[slnc 300]] That version is held back on purpose, '
            'because newer ones need a LocalStack account. [[slnc 500]] '
            'The code is ordinary Amazon code, using the newest Amazon '
            'library for Java. [[slnc 300]] It would run unchanged '
            'against Amazon itself. [[slnc 300]] You only need Docker, or '
            'a similar container tool, switched on first. [[slnc 300]] '
            "Every number you heard comes from the program's own output. "
            '[[slnc 600]] So, when is this too much? [[slnc 300]] If your '
            'files are small, a ticket adds steps for nothing. [[slnc '
            '300]] If the receiver needs the data at once, and storage is '
            'slow, the ticket costs more than it saves. [[slnc 300]] And '
            'it always means two services to run, not one.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Claim Check, with S three. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] The '
            'ticket goes through the queue, the luggage stays in storage, '
            'and a fingerprint on the ticket is what makes the luggage '
            'safe to trust. [[slnc 500]] The full source code, written '
            'notes, diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Work out the largest P D F that would fit in the queue '
            'whole. [[slnc 300]] Then change the first demo to try it, '
            'and see if you were right. [[slnc 500]] If this helped, a '
            'like really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
