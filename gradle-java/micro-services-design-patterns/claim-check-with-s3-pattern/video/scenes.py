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
            'Hello, and welcome. This video explains the Claim Check '
            'pattern in Java, using real Amazon storage and a real Amazon '
            'queue, running on your own machine. [[slnc 250]] It is '
            'written and presented by Jayasekhar Konduru. [[slnc 300]] '
            'Here is the plain definition, in general words. When '
            'something is too big to send in a message, you put it in '
            'storage, and send a small ticket instead. Whoever receives '
            'the ticket uses it to fetch the real thing. It works like '
            'the left-luggage office at a railway station. You leave '
            'your heavy suitcase at the counter, you carry a small paper '
            'ticket, and later the ticket gets your suitcase back. '
            '[[slnc 350]] Now the same thing in our online store. '
            'Checkout has an invoice to hand to the email service, and '
            'the invoice is a big PDF file. So checkout puts the PDF in '
            'storage, and sends the email service a ticket saying where '
            'to find it. [[slnc 300]] By the end you will have seen a '
            'real queue refuse an invoice, a ticket bring it back byte '
            'for byte, luggage that nobody collects, a delete that '
            'deletes nothing, and the bill for all of it.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Checkout makes an invoice PDF.', 'The email service sends it out.', '',
              'A queue sits between them.', 'A queue carries text, and it has', 'a size limit.', '',
              'The hand-built partner project', 'made up its own limit.', '',
              'This time the limit is Amazon\'s,', 'and so are the error messages.'],
        narration=(
            'Here is the scenario. Checkout makes an invoice, as a PDF '
            'file, and the email service sends it to the customer. They '
            'are two separate programs, and a queue sits between them, '
            'so checkout can hand the work over and carry on. [[slnc 300]] '
            'A queue is a waiting line for messages. One program puts a '
            'message in, another takes it out later. The hand-built '
            'partner project in this course had a queue with a size '
            'limit it made up for itself. [[slnc 250]] This time the '
            'queue is Amazon\'s queue service, and the storage is '
            'Amazon\'s storage service. The limit is Amazon\'s limit, '
            'and the refusals are Amazon\'s own words.'
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
            'First, the version without a ticket. The queue service is '
            'called S Q S, short for Simple Queue Service. The demo asks '
            'it how long a message may be, and it answers: one million, '
            'forty eight thousand, five hundred and seventy six bytes. '
            '[[slnc 250]] A business '
            'customer\'s monthly invoice is a PDF of one and a half '
            'million bytes. A message must be text, so the PDF is first '
            'written out as letters, in a format called base 64. That '
            'makes two million characters. [[slnc 250]] S Q S refuses '
            'it, with its own words: message must be shorter than one '
            'million, forty eight thousand, five hundred and seventy six '
            'bytes. That is not a rule this program made up. It is the '
            'service saying no.'
        ),
    ),
    dict(
        key='04-words', kind='bullets', title="The Services' Words",
        body=['Storage: Amazon S3.', 'A bucket is a named storage room.',
              'An object is one stored file.', 'A key is the name it is stored under.', '',
              'Queue: Amazon SQS.', 'A message is one piece of text.', '',
              'LocalStack plays both, on this', 'machine, in one container.'],
        narration=(
            'The real services bring a few words with them, and each one '
            'is simpler than it sounds. Think of the left-luggage office '
            'again. [[slnc 250]] The office is the storage service, '
            'called S 3, short for Simple Storage Service. A storage '
            'room in it is what S 3 calls a bucket. One suitcase on the '
            'shelf is what S 3 calls an object: just a stored file. And '
            'the number on the suitcase\'s tag, the name you fetch it '
            'by, is what S 3 calls a key. [[slnc 250]] The queue is S Q '
            'S, and one piece of text in it is a message. [[slnc 250]] '
            'Neither service is on Amazon here. A program called '
            'LocalStack answers exactly as they would, in one small '
            'sealed box on this machine, called a container. The demo '
            'switches it on at the start and off at the end.'
        ),
    ),
    dict(
        key='05-base64', kind='bullets', title='Why A Smaller PDF Fails Too',
        body=['A PDF is raw bytes.', 'A message must be text.', '',
              'Base64 spells every 3 bytes', 'with 4 letters.', '',
              '786432 bytes -> 1048576: accepted.', '786433 bytes -> 1048580: refused.', '',
              'The PDF must be three quarters', 'of the limit, not under it.'],
        narration=(
            'Here is the surprise in the first act. A PDF is raw bytes, '
            'and a message must be text. So the bytes are spelled out '
            'with letters, and that spelling uses four letters for every '
            'three bytes. The file grows by a third on the way in. '
            '[[slnc 250]] So the demo tries the edge. A PDF of seven '
            'hundred and eighty six thousand, four hundred and thirty two '
            'bytes becomes exactly the limit, and is accepted. One byte '
            'more, and the text grows past the limit, and it is '
            'refused. [[slnc 250]] So a file does not '
            'fit because it is under the limit. It fits only if it is '
            'under three quarters of it.'
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
            'Second, the claim check. Checkout puts the PDF in an S 3 '
            'bucket, under a random key thirty six characters long, a '
            'name nobody could guess. Only then does it send a ticket. '
            '[[slnc 250]] The ticket is one hundred and thirteen bytes '
            'of text. It names the bucket, the key, the size, one and a '
            'half million bytes, and a checksum. A checksum is a short '
            'fingerprint worked out from every byte of the file. If one '
            'byte changes, the fingerprint changes. [[slnc 250]] The '
            'email service takes the ticket, fetches one and a half '
            'million bytes, and checks the fingerprint. They are '
            'identical to what was sent. Then it deletes the stored file, '
            'and only after that the message. Nothing is left in either '
            'service.'
        ),
    ),
    dict(
        key='07-diagram', kind='diagram', title='Where The Invoice Lives',
        body=None,
        narration=(
            'Here is the whole picture in words. There are four parts, '
            'in order. Checkout comes first: it stores the PDF, then '
            'sends the ticket. The S 3 bucket is second: it holds the '
            'PDF under its key, however big it is. The S Q S queue is '
            'third: it carries only the ticket, a hundred or so bytes. '
            'The email service is last: it takes the ticket, fetches the '
            'PDF, checks the fingerprint, and then clears up both. '
            '[[slnc 300]] The one rule that holds it together is the '
            'order. Store before you send, and delete the message only '
            'after the file has been fetched and checked.'
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
            'Third, luggage nobody collected. Checkout sends ten '
            'invoices by ticket. The email service collects six of them '
            'and then stops. S 3 still holds four invoices, and S Q S '
            'still holds four tickets for them. That part is fine. They '
            'will be collected later. [[slnc 300]] Then an eleventh '
            'invoice is stored, and the send that should follow it '
            'fails. S Q S says the specified queue does not exist. '
            '[[slnc 250]] Now storage holds five invoices, and the queue '
            'holds four tickets. One invoice has no ticket at all, and '
            'nobody will ever ask for it. Storing and sending are two '
            'steps, and a program can stop between them.'
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
            'Fourth, the same key used twice. This bucket names each '
            'file after its order, so order ten forty two\'s invoice is '
            'stored under a key made from that order number, and its '
            'ticket is sent. [[slnc 250]] Then a corrected invoice for '
            'the same order is stored under the same key, before the '
            'first ticket is collected. S 3 keeps one object. The new '
            'file has quietly replaced the old one. [[slnc 250]] The '
            'email service redeems the first ticket. The fingerprint on '
            'the ticket does not match the file it gets back, so it '
            'refuses to send it. Without that checksum, a customer would '
            'have been sent an invoice nobody meant to send them.'
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
            'S 3 has an answer to that, and it has a catch. A bucket can '
            'be told to keep every version of every file. Storing under a '
            'key that is already used then adds a new version, and the '
            'old one stays. S 3 calls this versioning. Each version has '
            'its own id, and the ticket carries it. Now the first ticket '
            'gets the first invoice, identical: true. [[slnc 300]] Here '
            'is the catch. The email service deletes the key, as it did '
            'before. A listing of the bucket now shows no keys at all. '
            'But two versions are still stored, and still paid for. The '
            'delete only added a marker, a note saying the key is '
            'deleted. S 3 calls it a delete marker. [[slnc 250]] Only '
            'deleting each version by its own id brings the bucket to '
            'zero.'
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
            'Fifth, how long each one waits. Luggage nobody collects has '
            'to be cleared eventually. S 3 can do that itself, with a '
            'rule that removes every file a number of days after it was '
            'stored. S 3 calls it a lifecycle rule, and its smallest unit '
            'is one whole day. The invoice comes back stamped to expire '
            'at a midnight, between twenty four and forty eight hours '
            'away. [[slnc 300]] The queue has its own clock. It keeps a '
            'ticket nobody has taken for three hundred and forty five '
            'thousand, six hundred seconds. That is four days. '
            '[[slnc 250]] The demo cannot wait a day, so it removes the '
            'invoice the way the rule would. One ticket is still '
            'waiting. A slow email service redeems it, and S 3 says the '
            'specified key does not exist. The ticket outlived its '
            'luggage.'
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
            'Last, the bill. The demo counts every request the two '
            'services actually receive. An ordinary invoice of six '
            'hundred thousand bytes, small enough to go whole, takes '
            'three requests: send, receive, and delete the message. The '
            'queue carries eight hundred thousand bytes of text. '
            '[[slnc 250]] The same invoice by ticket takes six requests: '
            'store the file, send the ticket, receive it, fetch the '
            'file, delete the file, delete the message. The queue '
            'carries only one hundred and seventeen bytes. [[slnc 250]] '
            'So it is twice the requests, two services to run and pay '
            'for, and a gap between storing and sending. Here that was '
            'one container, for one queue service and one storage '
            'service.'
        ),
    ),
    dict(
        key='13-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['It got the shape right: store,', 'send a ticket, redeem, check,', 'clear up, expire.', '',
              'It left out:', '',
              'A limit that is the service\'s,', 'measured in text, not bytes.',
              'A key that can be overwritten.', 'A delete that keeps the bytes.'],
        narration=(
            'The hand-built partner project got the shape right. Store '
            'the luggage, send a ticket, redeem it, check the '
            'fingerprint, clear up, and expire what nobody collects. All '
            'of that holds on real S 3 and S Q S. [[slnc 300]] It left '
            'out three things. Its limit was a number it chose, and it '
            'counted bytes. The real limit is the service\'s, and it '
            'counts text, so a file that looks small enough grows by a '
            'third and is refused. Its storage never let two files share '
            'a name. And its delete really deleted, where a versioned '
            'bucket keeps every byte and bills you for it.'
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
            'Here is my verdict, plainly. Use a claim check when a '
            'payload will not fit in a message, or should not travel '
            'through one. Then say four things out loud, because neither '
            'service will assume them. [[slnc 250]] One. Store every '
            'file under a random key, and never reuse one. [[slnc 200]] '
            'Two. Put a checksum on every ticket, and check it before '
            'you trust the file. [[slnc 200]] Three. Store first, then '
            'send, and have a rule that sweeps away what nobody claims. '
            '[[slnc 200]] Four. Make the queue forget a ticket before '
            'storage forgets the file, so no ticket outlives its luggage.'
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
            'What is real here? Both services are played by LocalStack, '
            'version four point fourteen, in a container the demo starts '
            'and stops itself. That version is held back on purpose: '
            'the newer ones refuse to start without a LocalStack '
            'account. The code is plain Amazon code, using the newest '
            'Amazon library for Java, and would run unchanged against '
            'Amazon itself. The one thing you need is a container '
            'runtime, such as Docker Desktop, switched on before you '
            'start. Every number in this video is the program\'s own '
            'output, and two runs print the same thing. [[slnc 300]] So '
            'when is this too much? If your payloads are small, a ticket '
            'adds steps for nothing. If the receiver needs the data at '
            'once and storage is slow, the ticket costs more than it '
            'saves. [[slnc 250]] And it is always two services to run, '
            'not one.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Claim Check with S 3. [[slnc 250]] If you take one "
            'sentence away, take this one: the ticket goes through the '
            'queue, the luggage stays in storage, and a fingerprint on '
            'the ticket is what makes the luggage safe to trust. '
            '[[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough are all in the '
            'repository. [[slnc 300]] If you try one exercise, work out '
            'the largest PDF that would fit in the queue whole, then '
            'change the first act to try it, and see if you were right. '
            '[[slnc 300]] If this helped, a like genuinely does help '
            'other people find it, and subscribe if you would like the '
            'rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
