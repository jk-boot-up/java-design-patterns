# Claim Check with S3, Explained

## The pattern in one sentence

When a payload is too big to send in a message, store it somewhere built for big things and send a small ticket instead; whoever receives the ticket uses it to fetch the payload.

## The analogy, before any of the services' words

Think of the left-luggage office at a railway station. You leave your heavy suitcase at the counter and carry away a small paper ticket. Later, you, or anyone you give the ticket to, hands it back and gets the suitcase.

Now four questions the office has to answer, and a simulation never has to. What if the suitcase is too big for the door? The door here is the queue, and its size is not yours to choose. What if two suitcases are given the same ticket number? Somebody collects the wrong one. What if nobody ever comes back? The office has to clear its shelves, and the ticket in your pocket does not know. And what does the office charge, now that you pay a porter and a shelf instead of just carrying the bag? Those four questions are the six acts of this project.

## What S3 and SQS call these things

**S3**, Amazon's Simple Storage Service, is the office. A **bucket** is one of its storage rooms. An **object** is one stored file, here an invoice PDF. A **key** is the name the object is stored under, the number on the suitcase's tag.

**SQS**, Amazon's Simple Queue Service, is the queue between checkout and the email service. A **message** is one piece of text on it. SQS limits a message's length, and keeps a message nobody has taken for a while, its **retention period**.

**Versioning** is S3 keeping every object stored under a key, rather than replacing the old one. Each version has its own **version id**. In a versioned bucket, deleting by key only adds a **delete marker**: a note that says the key is deleted, while every version stays stored.

A **lifecycle rule** is S3 removing objects by itself, a number of whole days after they were stored.

**LocalStack** plays both services on your own machine, in one container the demo starts and stops.

## The six acts

### An Invoice Too Big For The Queue

SQS reports its longest message as 1048576 bytes. The monthly invoice is 1500000 bytes, and because a message is text, the PDF is written out as base64 first: 2000000 characters. SQS refuses it, in its own words. The edge is the surprise: base64 spells every 3 bytes with 4 letters, so a PDF of 786432 bytes becomes exactly 1048576 characters and is accepted, and one of 786433 becomes 1048580 and is refused.

```
  the email service's queue is on Amazon SQS, played by LocalStack. it reports its longest message as 1048576 bytes.
  a business customer's monthly invoice is a PDF of 1500000 bytes. a message is text, so it goes as base64: 2000000 characters.
  SQS refuses it: Message must be shorter than 1048576 bytes.
  a PDF of 786432 bytes becomes 1048576 characters and is accepted. one byte more, 786433, becomes 1048580 and is refused.
  base64 spells 3 bytes with 4 letters, so the largest PDF that fits is three quarters of the limit.
```

The refusal says "shorter than", but a message of exactly 1048576 characters is accepted. The limit includes its own number.

### Send The Ticket, Not The Luggage

Checkout stores the PDF under a random key, then sends a ticket: the bucket, the key, the size and the start of a SHA-256 checksum, a fingerprint of every byte. The email service takes the ticket, fetches the object, checks size and checksum, then deletes the object and after that the message.

```
  checkout stores the PDF in an S3 bucket under a random key of 36 characters, then sends a ticket.
  the ticket is 113 bytes of text: bucket, key, size 1500000, checksum bb8711d26a6daf29.
  the email service takes the ticket and fetches 1500000 bytes, identical to what was sent: true.
  it deletes the object, then the message. objects left in the bucket: 0. messages waiting: 0.
```

### Luggage Nobody Collected

Ten invoices by ticket, six collected. The other four are fine: their tickets are waiting. Then the eleventh is stored and its send fails, and that one is lost to everyone.

```
  checkout sends 10 invoices by ticket. the email service collects 6, then stops.
  S3 still holds 4 invoices, and SQS still holds 4 tickets for them.
  an 11th invoice is stored, and then its send fails: The specified queue does not exist.
  S3 now holds 5 invoices and SQS holds 4 tickets. 1 invoice has no ticket, and nobody will ever ask for it.
```

### The Same Key, Twice

A bucket that names each file after its order. A corrected invoice is stored under the same key before the first ticket is collected, and S3 simply replaces the object. The first ticket's checksum catches it. Versioning keeps both, and a ticket that carries the version id gets exactly the file it was written for. But the receiver's ordinary delete by key now removes nothing.

```
  a bucket keyed by order: ORD-1042's invoice is stored under invoices/ORD-1042.pdf and its ticket sent.
  a corrected invoice is stored under the same key before the first ticket is collected. S3 keeps 1 object.
  the email service redeems the first ticket: the payload is not the one that was sent: the checksum does not match.
  with versioning on, each store keeps its own version and the ticket names one. first ticket, identical to the first invoice: true.
  the email service deletes the key as before. keys listed: 0. versions still stored: 2. delete markers: 1.
  in a versioned bucket, delete hides the luggage and keeps paying for it. deleting each version by its id: 0 stored.
```

### How Long Each One Waits

The bucket's lifecycle rule counts in whole days, and S3 stamps each object with the midnight UTC at which it will go. The queue keeps a ticket for 345600 seconds by default. The demo cannot wait a day, so it deletes the invoice the way the rule would, and the waiting ticket finds nothing.

```
  the bucket gets a rule: remove every invoice 1 day after it was stored. a day is the smallest unit S3 takes.
  the invoice comes back stamped to expire at a midnight UTC, between 24 and 48 hours away: true.
  the queue keeps a ticket nobody has taken for 345600 seconds, which is 4 days.
  the demo cannot wait a day, so it removes the invoice as the rule would. tickets still waiting: 1.
  a slow email service redeems it: The specified key does not exist.
  the ticket and the luggage each have their own clock, and nothing keeps the two in step.
```

The exact expiry date depends on the day you run it, so the demo prints whether it has the right shape, not the date.

### The Bill

Every request both clients send is counted by the SDK itself, so these are requests the services really received.

```
  a 600000-byte invoice sent whole: 3 requests (SendMessage, ReceiveMessage, DeleteMessage). the queue carried 800000 bytes.
  the same invoice by ticket: 6 requests (PutObject, SendMessage, ReceiveMessage, GetObject, DeleteObject, DeleteMessage). the queue carried 117 bytes.
  twice the requests, two services to run and pay for, and a gap between storing and sending.
  this demo needed 1 container for 1 queue service and 1 storage service.
```

The ticket here is 117 bytes rather than 113 because this act's bucket has a longer name and the invoice's size has one digit fewer.

## The verdict

Use a claim check when a payload will not fit in a message, or should not travel through one. Then store under random keys and never reuse one; put a checksum on every ticket and check it; store first, send second, and have a lifecycle rule sweep what nobody claims; and make the queue forget a ticket before storage forgets its file.
