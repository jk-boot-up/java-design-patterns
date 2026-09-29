# Valet Key Pattern — Video Narration Script

## 1. Valet Key

Hello, and welcome. This video explains the Valet Key pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Instead of carrying every upload yourself, you give the client a signed key. The key lets it do one specific thing, directly with the storage service, for a few minutes. Think of the valet key some cars come with. It opens the door, and starts the engine. But it will not open the boot, or the glovebox. The attendant parks the car, and the key is only good for that job. In this video, the domain is an online shop. Customers add photos to their product reviews. By the end, you will hear what carrying uploads costs. How a valet key works. What it will not allow. And its one big risk.

## 2. The Scenario

Here is the scenario. Customers can add photos to their product reviews. Each photo was uploaded to the shop's app server. The app server then sent it on to the file storage service.

## 3. Act One — Carried by the app

First demo: review photos carried through the shop's app server. Ten customers each upload a two megabyte photo. Each photo goes to the app server. The app server sends it on to storage. The app server carried forty megabytes. Every byte came in, and went out again.

## 4. Act Two — A valet key

Second demo: a valet key. The shop signs a short permission. You may upload one photo, to this address, within five minutes, up to five megabytes. The customer's browser sends the photo straight to storage. Storage checks the signature, and stores it. The app server carried under two hundred bytes. Just the key.

## 5. Act Three — Only what it allows

Third demo: the key allows that, and nothing else. Use it to read the photo? Refused. Change the address, to overwrite someone else's review? Refused: the signature no longer matches. Upload a six megabyte file? Refused: too large. And with no key at all, storage says no.

## 6. Act Four — Expiry

Fourth demo: the key runs out. A key is signed for two tenths of a second. It is used after four tenths. Refused: key expired. Nobody had to switch it off.

## 7. Act Five — The bill

Fifth demo: the bill. Whoever holds the key can use it. A key is pasted into a public chat. A stranger uses it. Storage accepts: the key is valid. It cannot be taken back before it expires. So keep keys short-lived, narrow, and out of your logs.

## 8. The Pattern

Let's name the pattern. The app signs a key. It names one action, one file, a size limit, and an expiry time. The client uses the key to talk to storage directly. Storage checks every part of it, and refuses anything else.

## 9. Who Does What

Here is who does what. The shop's app server signs valet keys. The signer uses a secret that only the shop and the storage service know. Storage checks each key, and stores the file. And the customer's browser uploads directly.

## 10. Where You Have Seen It

You have probably met this pattern already. Amazon S3 has presigned URLs. Azure has shared access signatures. Google Cloud has signed URLs. And every download link that stops working after a day is a valet key.

## 11. When To Use It

So, when should you use it? For large, or many, files that the app does not need to look at. Sign the method, the path, the size, and the expiry. Keep lifetimes short. And keep signed addresses out of your logs.

## 12. Thanks for Watching

That's the Valet Key pattern. If you remember one sentence, make it this one. Hand out a key that opens one door, briefly, and let the bytes go direct. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Make a key that works only once. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
