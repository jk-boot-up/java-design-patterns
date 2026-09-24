# Claim Check with S3 Pattern — Video Narration Script

## 1. Claim Check with S3

Hello, and welcome. This video explains the Claim Check pattern in Java, using real Amazon storage and a real Amazon queue, running on your own machine. It is written and presented by Jayasekhar Konduru. Here is the plain definition, in general words. When something is too big to send in a message, you put it in storage, and send a small ticket instead. Whoever receives the ticket uses it to fetch the real thing. It works like the left-luggage office at a railway station. You leave your heavy suitcase at the counter, you carry a small paper ticket, and later the ticket gets your suitcase back. Now the same thing in our online store. Checkout has an invoice to hand to the email service, and the invoice is a big PDF file. So checkout puts the PDF in storage, and sends the email service a ticket saying where to find it. By the end you will have seen a real queue refuse an invoice, a ticket bring it back byte for byte, luggage that nobody collects, a delete that deletes nothing, and the bill for all of it.

## 2. The Scenario

Here is the scenario. Checkout makes an invoice, as a PDF file, and the email service sends it to the customer. They are two separate programs, and a queue sits between them, so checkout can hand the work over and carry on. A queue is a waiting line for messages. One program puts a message in, another takes it out later. The hand-built partner project in this course had a queue with a size limit it made up for itself. This time the queue is Amazon's queue service, and the storage is Amazon's storage service. The limit is Amazon's limit, and the refusals are Amazon's own words.

## 3. An Invoice Too Big For The Queue

First, the version without a ticket. The queue service is called S Q S, short for Simple Queue Service. The demo asks it how long a message may be, and it answers: one million, forty eight thousand, five hundred and seventy six bytes. A business customer's monthly invoice is a PDF of one and a half million bytes. A message must be text, so the PDF is first written out as letters, in a format called base 64. That makes two million characters. S Q S refuses it, with its own words: message must be shorter than one million, forty eight thousand, five hundred and seventy six bytes. That is not a rule this program made up. It is the service saying no.

## 4. The Services' Words

The real services bring a few words with them, and each one is simpler than it sounds. Think of the left-luggage office again. The office is the storage service, called S 3, short for Simple Storage Service. A storage room in it is what S 3 calls a bucket. One suitcase on the shelf is what S 3 calls an object: just a stored file. And the number on the suitcase's tag, the name you fetch it by, is what S 3 calls a key. The queue is S Q S, and one piece of text in it is a message. Neither service is on Amazon here. A program called LocalStack answers exactly as they would, in one small sealed box on this machine, called a container. The demo switches it on at the start and off at the end.

## 5. Why A Smaller PDF Fails Too

Here is the surprise in the first act. A PDF is raw bytes, and a message must be text. So the bytes are spelled out with letters, and that spelling uses four letters for every three bytes. The file grows by a third on the way in. So the demo tries the edge. A PDF of seven hundred and eighty six thousand, four hundred and thirty two bytes becomes exactly the limit, and is accepted. One byte more, and the text grows past the limit, and it is refused. So a file does not fit because it is under the limit. It fits only if it is under three quarters of it.

## 6. Send The Ticket, Not The Luggage

Second, the claim check. Checkout puts the PDF in an S 3 bucket, under a random key thirty six characters long, a name nobody could guess. Only then does it send a ticket. The ticket is one hundred and thirteen bytes of text. It names the bucket, the key, the size, one and a half million bytes, and a checksum. A checksum is a short fingerprint worked out from every byte of the file. If one byte changes, the fingerprint changes. The email service takes the ticket, fetches one and a half million bytes, and checks the fingerprint. They are identical to what was sent. Then it deletes the stored file, and only after that the message. Nothing is left in either service.

## 7. Where The Invoice Lives

Here is the whole picture in words. There are four parts, in order. Checkout comes first: it stores the PDF, then sends the ticket. The S 3 bucket is second: it holds the PDF under its key, however big it is. The S Q S queue is third: it carries only the ticket, a hundred or so bytes. The email service is last: it takes the ticket, fetches the PDF, checks the fingerprint, and then clears up both. The one rule that holds it together is the order. Store before you send, and delete the message only after the file has been fetched and checked.

## 8. Luggage Nobody Collected

Third, luggage nobody collected. Checkout sends ten invoices by ticket. The email service collects six of them and then stops. S 3 still holds four invoices, and S Q S still holds four tickets for them. That part is fine. They will be collected later. Then an eleventh invoice is stored, and the send that should follow it fails. S Q S says the specified queue does not exist. Now storage holds five invoices, and the queue holds four tickets. One invoice has no ticket at all, and nobody will ever ask for it. Storing and sending are two steps, and a program can stop between them.

## 9. The Same Key, Twice

Fourth, the same key used twice. This bucket names each file after its order, so order ten forty two's invoice is stored under a key made from that order number, and its ticket is sent. Then a corrected invoice for the same order is stored under the same key, before the first ticket is collected. S 3 keeps one object. The new file has quietly replaced the old one. The email service redeems the first ticket. The fingerprint on the ticket does not match the file it gets back, so it refuses to send it. Without that checksum, a customer would have been sent an invoice nobody meant to send them.

## 10. A Delete That Deletes Nothing

S 3 has an answer to that, and it has a catch. A bucket can be told to keep every version of every file. Storing under a key that is already used then adds a new version, and the old one stays. S 3 calls this versioning. Each version has its own id, and the ticket carries it. Now the first ticket gets the first invoice, identical: true. Here is the catch. The email service deletes the key, as it did before. A listing of the bucket now shows no keys at all. But two versions are still stored, and still paid for. The delete only added a marker, a note saying the key is deleted. S 3 calls it a delete marker. Only deleting each version by its own id brings the bucket to zero.

## 11. How Long Each One Waits

Fifth, how long each one waits. Luggage nobody collects has to be cleared eventually. S 3 can do that itself, with a rule that removes every file a number of days after it was stored. S 3 calls it a lifecycle rule, and its smallest unit is one whole day. The invoice comes back stamped to expire at a midnight, between twenty four and forty eight hours away. The queue has its own clock. It keeps a ticket nobody has taken for three hundred and forty five thousand, six hundred seconds. That is four days. The demo cannot wait a day, so it removes the invoice the way the rule would. One ticket is still waiting. A slow email service redeems it, and S 3 says the specified key does not exist. The ticket outlived its luggage.

## 12. The Bill

Last, the bill. The demo counts every request the two services actually receive. An ordinary invoice of six hundred thousand bytes, small enough to go whole, takes three requests: send, receive, and delete the message. The queue carries eight hundred thousand bytes of text. The same invoice by ticket takes six requests: store the file, send the ticket, receive it, fetch the file, delete the file, delete the message. The queue carries only one hundred and seventeen bytes. So it is twice the requests, two services to run and pay for, and a gap between storing and sending. Here that was one container, for one queue service and one storage service.

## 13. What The Simulation Left Out

The hand-built partner project got the shape right. Store the luggage, send a ticket, redeem it, check the fingerprint, clear up, and expire what nobody collects. All of that holds on real S 3 and S Q S. It left out three things. Its limit was a number it chose, and it counted bytes. The real limit is the service's, and it counts text, so a file that looks small enough grows by a third and is refused. Its storage never let two files share a name. And its delete really deleted, where a versioned bucket keeps every byte and bills you for it.

## 14. The Verdict

Here is my verdict, plainly. Use a claim check when a payload will not fit in a message, or should not travel through one. Then say four things out loud, because neither service will assume them. One. Store every file under a random key, and never reuse one. Two. Put a checksum on every ticket, and check it before you trust the file. Three. Store first, then send, and have a rule that sweeps away what nobody claims. Four. Make the queue forget a ticket before storage forgets the file, so no ticket outlives its luggage.

## 15. What Is Real, And When Not

What is real here? Both services are played by LocalStack, version four point fourteen, in a container the demo starts and stops itself. That version is held back on purpose: the newer ones refuse to start without a LocalStack account. The code is plain Amazon code, using the newest Amazon library for Java, and would run unchanged against Amazon itself. The one thing you need is a container runtime, such as Docker Desktop, switched on before you start. Every number in this video is the program's own output, and two runs print the same thing. So when is this too much? If your payloads are small, a ticket adds steps for nothing. If the receiver needs the data at once and storage is slow, the ticket costs more than it saves. And it is always two services to run, not one.

## 16. Thanks for Watching

That's Claim Check with S 3. If you take one sentence away, take this one: the ticket goes through the queue, the luggage stays in storage, and a fingerprint on the ticket is what makes the luggage safe to trust. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, work out the largest PDF that would fit in the queue whole, then change the first act to try it, and see if you were right. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
