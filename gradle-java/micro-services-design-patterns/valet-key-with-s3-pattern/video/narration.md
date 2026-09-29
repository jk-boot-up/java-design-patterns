# Valet Key with Amazon S3 Pattern — Video Narration Script

## 1. Valet Key with Amazon S3

Hello, and welcome. This video explains the Valet Key pattern, with Amazon S3 presigned addresses, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A valet key gives a client permission to do one thing, directly, for a short time. Without the client ever holding the real credentials. Amazon S3 is cloud object storage, and its presigned addresses are exactly such keys. Think of a hotel valet key. It starts the car, but does not open the boot. And the valet has it only for the evening. In this video, the domain is an online shop's review photos. By the end, you will hear how photos stop passing through the shop's server. What a signed address allows, and refuses. And what happens when one leaks.

## 2. The Scenario

Here is the scenario. Customers add photos to their reviews. Every photo went through the shop's app server, on its way to storage. Ten photos meant forty megabytes carried, by a server that only needed to say where each photo goes.

## 3. Act One — Through the app server

First demo: photos carried through the shop's app server. Ten customers each upload a two megabyte photo. Every byte comes in to the app server. And goes out again, to storage. Forty megabytes through a server that only needed to say where the photo goes.

## 4. Act Two — A presigned URL

Second demo: a valet key, as an S3 presigned address. The shop signs a web address. It allows one upload, of one photo, of exactly this size, for five minutes. The customer's browser uploads straight to S3. Accepted. Two million bytes stored. The app server carried only the address.

## 5. Act Three — That, and nothing else

Third demo: the key allows that, and nothing else. Use it to read the photo. Refused. Edit it to point at another review. Refused. Send a six megabyte file with it. Refused, because the size was signed. One honest note. An upload with no key at all gets through here, because this local stand-in for S3 does not check permissions. Real S3 refuses it.

## 6. Act Four — The key runs out

Fourth demo: the key runs out. A key valid for one second is used after two. Refused.

## 7. Act Five — The bill

Fifth demo: the bill. A valid address is pasted into a public chat. A stranger uses it. Accepted. Whoever holds the key can use it, until it expires. Keep keys short-lived and narrow. Keep them out of logs. And sign with credentials you can revoke.

## 8. The Pattern, in S3

Let's name the pattern, in S3's words. The shop signs an address. One method, one object, one size, for a few minutes. The client uses it directly. And S3 checks the signature against exactly what is asked.

## 9. Who Does What

Here is who does what. The storage class signs addresses with the AWS SDK's presigner. The browser uses only the address. And LocalStack plays Amazon S3, on your own machine.

## 10. Where You Have Seen It

You have probably met this already. S3 presigned addresses. Google Cloud's signed addresses. Azure's shared access signatures. And every download link in an email that stops working after a day.

## 11. When To Use It

So, when should you use it? For large uploads and downloads the app never needs to see. Sign the method, object and size. Keep lifetimes short. Keep addresses out of logs. And test permissions on the real service.

## 12. Thanks for Watching

That's the Valet Key, with Amazon S3. If you remember one sentence, make it this one. Sign exactly one permission, for a short time, and let the storage check it. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It needs Docker running, and starts LocalStack for you. Here is one exercise to try. Sign a download address for the photo, valid for one minute. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
