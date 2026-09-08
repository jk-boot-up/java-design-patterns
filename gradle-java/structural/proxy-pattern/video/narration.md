# Proxy Pattern — Video Narration Script

## 1. The Proxy Pattern

Hello, and welcome. This video explains the Proxy pattern in Java, and it is written and presented by Jayasekhar Konduru. Let's start with the simple definition. The proxy pattern puts a stand-in in front of a real object, with the same interface as the real thing. The caller cannot tell the difference, but the stand-in is free to delay the expensive work, check who is asking, or count the calls, before it passes anything along. That's the idea in a sentence — controlling when an object gets built, and who is allowed to touch it. The rest of the video does it properly, by building a real working Java project: an online store's category page, where loading a product's full-resolution image is expensive and not every asset is one a shopper may see. By the end you'll know how to delay expensive work until it is actually needed, and how to put an access check in one place that no caller can forget.

## 2. The Scenario

So, imagine a product listing backed by full-resolution images. Loading a single one of those is expensive — decoding the file, allocating the memory, reading from disk. And there are two things the listing needs that the image itself really shouldn't have to know anything about. First, don't load an image until it is actually rendered. And second, don't let a non-admin render a restricted image at all.

## 3. Where Those Checks End Up

Without a stand-in, both of those concerns land in the caller. The listing builds every image up front in its constructor, because that's the simplest thing that works. And every screen that shows an image re-implements the same role check inline. Now add a thumbnail grid, a slideshow, a search results page — and each one of those has to remember to do both of those things, and to do them correctly.

## 4. The Naive Approach — Eager Loading and Inline Checks

So here's the naive approach. NaiveProductListing takes a list of SKUs and, in its constructor, builds a HighResolutionProductImage for every single one — before anything has been rendered at all. And NaiveAdminImageViewer has the role check written directly inside its view method. That check is correct. The problem is that it's correct in exactly one place, and the next screen has to copy it.

## 5. Why That Hurts

And that does real damage as the system grows. You pay the full loading cost for images that are never shown — build a listing of ten and render one, and nine loads were wasted. The access rule is duplicated in every screen that renders an image. And worse than duplication: a screen that simply forgets the check isn't a compile error, it's a silent security hole. None of this is a bug. Each naive class does exactly what it says. The waste is structural — access control and lifetime management pushed out into every caller.

## 6. The Proxy Pattern

The proxy pattern fixes exactly this. In Gang of Four terms, proxy provides a surrogate or placeholder for another object in order to control access to it. In plain language? Same interface, but it decides whether, and when, the call actually gets through.

## 7. Remember It With the Bouncer on the Door

Here's how to remember it forever. Think about the bouncer on the door of a club. The bouncer stands in front of the club, not inside it. You talk to the bouncer exactly the way you'd talk to the club itself — you ask to come in. And the bouncer decides whether that request gets through. Here's the part that matters. The club is the same club either way. Nothing was added to it, nothing was changed about it. Somebody just controls the door.

## 8. The Four Roles

Every proxy setup has four roles. The subject, ProductImage, the interface the real thing and every stand-in share. The real subject, HighResolutionProductImage, the expensive object we're protecting. The proxies — LazyProductImage, which delays construction until the first render call, and RestrictedProductImage, which checks the caller's role first. And the client, ProductImageDemo, which holds only a ProductImage and never learns which of those it actually has. Here's the single most important idea in this whole video. The proxy exposes exactly the same interface as the real subject, and returns exactly the same result. Nothing new is added. That is what makes it a proxy and not a decorator.

## 9. The Subject — The Shared Shape

This is the subject, ProductImage. It's the shared interface the real image and every proxy implement — just render, and S K U. And this is the real subject, HighResolutionProductImage. Its constructor bumps a static load count, which is our stand-in for expensive work. Notice it knows nothing about proxies, or roles, or laziness. It just is an image.

## 10. The Virtual Proxy — Build It Late, Build It Once

And this is the virtual proxy, LazyProductImage. It holds a S K U, and a realImage field that stays null until somebody actually calls render. First call, it builds the real image and caches it. Every call after that reuses the cached one. And look at the S K U method. It answers straight from the proxy's own field, without loading anything. That detail matters — a proxy that has to build the real subject just to answer a cheap question has defeated its own purpose.

## 11. The Protection Proxy — And Why It Takes a ProductImage

Here's the subtlety worth pausing on. RestrictedProductImage takes a ProductImage in its constructor. Not a HighResolutionProductImage — a ProductImage. That one detail is what lets it wrap a LazyProductImage, so you get the role check and the lazy loading together, from two small classes that were never written with each other in mind. And notice the order. If the role check fails, it throws before it ever calls render on the image it wraps — so a denied shopper never causes a load at all. The expensive work is skipped because the access decision came first.

## 12. Running It

When we run the project, the numbers tell the whole story. The naive listing has loaded three images before rendering anything. The virtual proxy has loaded zero — the real subject hasn't been touched. After the first render it's one. After the second render it's still one, because the instance was cached. Then the protection proxy lets an admin through and refuses a shopper. And in the composed section, S K U nine thousand one stays unloaded right up until an admin passes the role check — one proxy wrapped in the other, doing both jobs at once.

## 13. Wrap Up

So, to recap. Use proxy when a client shouldn't have to manage when an object gets created, or whether it's allowed to be used at all. Keep the proxy's interface identical to the subject, and keep the cheap questions cheap — never load the real thing just to answer one. And if you remember one sentence from today, make it this one. Proxy keeps the same interface and delegates in order to control access — when to create, whether to allow, where the real thing lives. Decorator keeps the same interface and delegates in order to add new behaviour on top. Same shape, different intent.

## 14. Thanks for Watching

And that's the proxy pattern. If you got something out of this, do give it a thumbs up, and subscribe. It genuinely helps the channel, and it's what makes more of these possible. And if there's a pattern you'd like me to cover next, drop it in the comments. I read every one. All the source code, the written notes and an interactive animation are in the repository. Thanks for watching, and I'll see you in the next one.
