# The Proxy Pattern Pattern — Video Narration Script

## 1. The Proxy Pattern

Hello, and welcome. This video explains the Proxy pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A proxy is a stand-in, placed in front of a real object, with exactly the same shape. The caller cannot tell the difference. But the stand-in can delay expensive work, check who is asking, or count calls, before passing anything along. Think of a bouncer at the door of a club. You ask the bouncer to come in, and the bouncer decides. In our online store, a category page shows product images. Loading a full-size image is expensive. And some images only certain staff may see. By the end, you will know how to delay expensive work until it is needed. And how to put an access check in one place that no caller can forget.

## 2. The Scenario

Here is the scenario. A product listing uses full-size images. Loading just one is expensive: reading the file, decoding it, and holding it in memory. And the listing needs two things that the image itself should not have to care about. First: do not load an image until it is actually shown. Second: do not let an ordinary shopper see a restricted image at all.

## 3. Where Those Checks End Up

Without a stand-in, both jobs land on the caller. The listing loads every image up front, when it is created, because that is simplest. And every screen that shows an image repeats the same access check. Now add a thumbnail grid, a slideshow, and a search results page. Each one must remember to do both jobs, and do them correctly.

## 4. The Naive Approach — Eager Loading and Inline Checks

Here is the naive approach. The naive listing receives a list of product codes. And straight away, it loads a full-size image for every one, before anything is shown. And a separate admin viewer has the access check written directly inside it. That check is correct. But it is correct in only one place. The next screen has to copy it.

## 5. Why That Hurts

That does real damage as the system grows. You pay the full loading cost for images that are never shown. Load a listing of ten, show one, and nine loads were wasted. The access rule is copied into every screen that shows an image. And worse, a screen that forgets the check does not fail to build. It becomes a silent security hole. None of this is a bug. The waste is in the structure: access and timing pushed out into every caller.

## 6. The Proxy Pattern

The Proxy pattern fixes exactly this. The classic book on design patterns, by the authors known as the Gang of Four, describes it like this. Provide a stand-in, or placeholder, for another object, to control access to it. In plain words: the same shape, but it decides whether, and when, the call gets through.

## 7. Remember It With the Bouncer on the Door

Here is how to remember it. Think about the bouncer at the door of a club. The bouncer stands in front of the club, not inside it. You talk to the bouncer just as you would to the club. You ask to come in. And the bouncer decides whether you get through. Here is the part that matters. The club is the same club either way. Nothing was added to it. Someone just controls the door.

## 8. The Four Roles

Every proxy has four roles. The subject: the shared interface, here called product image. The real subject: the full-size image, the expensive object being protected. The proxies: a lazy image, which waits until the first time it is shown. And a restricted image, which checks the caller's role first. And the client: the demo code, which only ever holds a product image, and never learns which kind it has. Here is the most important idea in this video. A proxy has exactly the same shape as the real object, and gives exactly the same result. Nothing new is added. That is what makes it a proxy, and not a decorator.

## 9. The Subject — The Shared Shape

Here is the subject: the product image interface. It has just two questions. Show yourself. And what is your product code? And here is the real subject: the full-size image. Every time one is created, it adds one to a load counter. That counter stands for expensive work. It knows nothing about proxies, roles, or waiting. It just is an image.

## 10. The Virtual Proxy — Build It Late, Build It Once

Here is the lazy proxy. It holds a product code, and an empty space for the real image. The first time it is asked to show itself, it loads the real image, and keeps it. Every time after that, it reuses the one it kept. And when asked for its product code, it answers from its own record. Without loading anything. That matters. A proxy that loads the real thing just to answer a cheap question has defeated its own purpose.

## 11. The Protection Proxy — And Why It Takes a ProductImage

Here is a detail worth pausing on: the restricted proxy. It wraps any product image, not just a full-size one. That is what lets it wrap a lazy image. So you get the role check and the lazy loading together. From two small classes that were never written with each other in mind. And notice the order. If the role check fails, it refuses before touching the image it wraps. So a refused shopper never causes a load at all. The expensive work is skipped, because the access decision came first.

## 12. Running It

Let's run the project. The naive listing has loaded three images before showing anything. The lazy proxy has loaded none. The real image has not been touched. After the first time it is shown, one image is loaded. After the second time, still only one, because it was kept. Then the restricted proxy lets an admin through, and refuses a shopper. And in the combined example, the restricted image stays unloaded, right up until an admin passes the check. One proxy wrapped in the other, doing both jobs at once.

## 13. Wrap Up

So, to recap. Use a proxy when the caller should not have to manage when an object is created. Or whether it may be used at all. Keep the proxy's shape identical to the real object. And keep cheap questions cheap. Never load the real thing just to answer one. And one comparison worth knowing. A proxy and a decorator look the same: same shape, passing calls along. But a proxy controls access: when to create, and whether to allow. A decorator adds new behaviour on top. Same shape, different purpose.

## 14. Thanks for Watching

That's the Proxy pattern. If you remember one sentence, make it this one. A proxy is a stand-in with the same shape as the real thing, deciding when it is built, and who may use it. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a third proxy that counts how often each image is shown. And notice the caller does not change. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
