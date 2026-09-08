# Narration Script — Singleton Pattern

Generated from `scenes.py`. Do not hand-edit; edit the `narration` field of a scene instead and regenerate.

## 1. Singleton Pattern

Hello, and welcome. This video explains the Singleton pattern in Java, and it is written and presented by Jayasekhar Konduru. Let's start with the simple definition. The singleton pattern guarantees that a class has exactly one instance, and gives every caller one well-known way of reaching it. The class takes control of its own creation, so however you ask — and we'll see some determined ways of asking — you cannot get a second one. That's the idea in a sentence. It's the smallest pattern in the Gang of Four book, and the one Java developers reach for the most casually. The rest of the video does it properly, by building a real working Java project: an order-number sequencer for an online store, in Java twenty one. And along the way we'll watch a private constructor get called anyway — twice — by two attacks that Effective Java's favourite singleton shape is immune to.

## 2. The Job

So here's the job. Every checkout on our marketplace needs an order number — ORD-000001, ORD-000002, and so on — handed out in strict sequence, no gaps, no repeats. Checkout issues them. So does the admin console, when support staff raise a manual order. So does a background job replaying a failed payment. All three have to draw from the same counter, or two different customers can end up with the same order number.

## 3. An Instance Per Caller

Reasonable-looking class. The problem shows up the moment two different parts of the system each construct their own. Checkout builds one, admin console builds another, and each new OrderSequenceGenerator starts its own counter at zero. There's nothing wrong with the class itself — the bug is that the language lets anyone construct as many of it as they like, when the rule is exactly one, ever.

## 4. The Classic Fix

The textbook fix takes new away from callers and hands back one shared instance instead. Private constructor, static field, public getInstance. Every caller now goes through getInstance, and under normal use it really does return the same object every time. Private means private... or does it?

## 5. Breaking It: Reflection

Reflection can call a private constructor directly. Get declared constructor, set accessible true, new instance — and it just works. 'Private' is a compile-time convention the compiler checks, not an absolute the J V M enforces at runtime. Frameworks and testing tools use exactly this trick for legitimate reasons, and they never asked this class's permission first.

## 6. Breaking It: Serialization

Second attack, no reflection needed at all. Java's default serialization never calls a constructor — it rebuilds an object's fields straight from bytes. Serialize the shared instance, deserialize it, and what comes back is a brand-new object, counter reset to zero, silently. Two separate holes, in a class that was written specifically to prevent a second instance from ever existing.

## 7. The Singleton Pattern

The Gang of Four's definition is short. Ensure a class only has one instance, and provide a global point of access to it. In plain words? Make it impossible to construct more than one of this class, and give every caller in the program the same well-known way to reach the instance that does exist. The question this project actually answers is narrower, though: which Java shape makes that impossible, and which shapes only look like they do.

## 8. The Shape of It

So here's the shape of it. OrderSequenceGenerator is a single-element enum — instance is a constant the J V M creates exactly once, during class loading, before any caller's code can even reference it. Three guarantees come with that for free: the J V M's class-loading is thread-safe by the language specification, reflection is barred outright from calling an enum's constructor, and enum deserialization resolves by name against the existing constant instead of building a new object.

## 9. One Constant, Three Guarantees

That is the entire singleton. No private constructor to remember to write, no getInstance method, no null check, no lock. Constructor dot new instance on an enum throws IllegalArgumentException — the reflection A P I refuses outright, no defensive code required here. And serializing instance and reading it back hands you the exact same instance, because the language defines an enum's serialized form as its name, not its fields.

## 10. Why AtomicLong

One detail that only matters once you've actually solved the instance problem. Now that there truly is exactly one instance, it's reachable from every thread in the program at once, so the state it carries has to be safe to mutate concurrently. Counter plus plus on a plain int is a read, then a write — two threads can interleave and lose an increment. Increment and get on an atomic long is a single atomic operation. No two callers can ever collide on the same number.

## 11. Running It

Let's run it, and see the whole story on one screen. The enum issues order numbers, rejects the reflection attack with a clear exception, and comes back as the exact same instance after a serialization round trip. Then the legacy class — identical to callers under normal use — falls to both of the exact same attacks. Same two lines of attacking code, run against two classes that look identical from the outside, with opposite outcomes.

## 12. Where It Stops

Now the honest part. Every pattern has a ceiling, and this one's is real. A singleton is global mutable state dressed up in a pattern name — any code anywhere can reach INSTANCE, and there's no clean way to give one test its own counter. It hides a dependency, too: a method calling INSTANCE inside its body doesn't show that dependency in its signature the way a parameter would. And the moment the system needs a separate sequence per storefront or per warehouse, 'exactly one for the whole J V M' is precisely the wrong guarantee — no amount of tuning fixes that, the pattern itself has to go.

## 13. How It Relates to the Others

So where does singleton sit next to the other creational patterns? Prototype answers 'I have one, get me another.' Builder answers 'which pieces, assembled in what order.' Abstract factory answers 'which whole matching set.' Singleton is the odd one out — it says nothing about assembly at all, and controls how many instances exist, full stop. It's also the one most often reached for to solve a different problem — 'I don't want to pass this object around' — which dependency injection solves without the global-state cost.

## 14. One Sentence to Keep

If you keep one sentence from all of this, keep this one. A private constructor is a promise the compiler checks, not one the J V M enforces at runtime — reflection and serialization can both break it. A single-element enum is the one Java singleton shape that closes both holes, for free, with no extra code. There's a full set of notes in the project, an animated walkthrough you can step through at your own pace, and a session plan if you fancy teaching this to somebody else. Go add a readResolve method to the legacy class, and watch exactly one of the two attacks start failing.

## 15. Thanks for Watching

And that's the singleton pattern. If you got something out of this, do give it a thumbs up, and subscribe. It genuinely helps the channel, and it's what makes more of these possible. And if there's a pattern you'd like me to cover next, drop it in the comments. I read every one. All the source code, the written notes and the diagrams are in the repository. Thanks for watching, and I'll see you in the next one.
