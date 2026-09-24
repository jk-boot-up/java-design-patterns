# Problem Statement

## The scenario

Checkout makes an invoice for every order, as a PDF file, and the email service sends it to the customer. They are two separate programs, and a queue sits between them so that checkout can hand the work over and carry on selling. Most invoices are small. A business customer's monthly invoice is not: it lists every order of the month, carries a scanned signature, and runs to one and a half million bytes.

## The naive version

Checkout puts the whole PDF in the message. A message on Amazon SQS is text, so the PDF is first written out as base64, and the queue refuses it.

```
  a business customer's monthly invoice is a PDF of 1500000 bytes. a message is text, so it goes as base64: 2000000 characters.
  SQS refuses it: Message must be shorter than 1048576 bytes.
```

## What the partner project already did

The plain-Java Claim Check project in this course taught the whole pattern with nothing installed: store the payload, send a ticket with an id, a size and a checksum, redeem it at the other end, sweep what nobody collects. It is a complete teaching of the idea and nothing here replaces it.

It had one comfort, though. Its broker's limit was a number the program chose for itself, and it counted raw bytes. Its storage handed out ids that could never collide, and its delete really deleted. None of those is true of the real services.

## What this project must deliver

The same invoice and the same two programs, with the queue on Amazon SQS and the storage on Amazon S3, both played by LocalStack in one container the demo starts and stops. A PDF genuinely refused by the service, in the service's own words, and the exact edge where a PDF stops fitting. A ticket that brings back the same 1500000 bytes. Luggage that nobody collected, and an invoice stored whose ticket never went. A key stored twice, caught by the checksum, fixed by versioning, and a delete in a versioned bucket that leaves every byte stored. The ticket's clock and the luggage's clock set side by side. And the bill, counted as requests the services actually received.

Every figure printed is the services' own, and two runs back to back print the same thing.
