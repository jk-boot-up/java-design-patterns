# Double-Checked Locking Pattern — Video Narration Script

## 1. Double-Checked Locking

Hello, and welcome. This video explains the Double-Checked Locking pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: double checked locking creates a shared object lazily. It checks for the object first without a lock, and only takes the lock, and checks again, when it looks missing. This is another project in the concurrency category, whose subject is how threads share work and state without corrupting either. In our online store, the shared thing that is expensive to build is the price list. By the end you will see two threads each build the price list, see the lock-every-time fix and its cost, see the double check take the lock once, see why the field must be volatile, see the simplest correct way, and see the bill, which is that it is ceremony with one way to be subtly wrong.

## 2. The Scenario

Here is the scenario. The price list is expensive to build, so the shop builds it the first time anyone asks. Many threads ask, and the first few may ask at the same moment. The question: how do we build it exactly once?

## 3. Check, Then Create

First, check, then create. Two threads ask for the shared price list at the same moment, before it exists. Both see that it is missing. Both build one. Two price lists were built, and each thread holds a different one. One of them is thrown away, and the expensive build was done twice.

## 4. The Pattern

The pattern. Look for the object, without a lock. If it is missing, take the lock. Then look again, in case someone else built it while you waited. Only then, build it. Once it is built, nobody takes the lock again.

## 5. Lock Every Time

Second, lock every time. The same two threads, with the lock taken on every call: one is built. That is correct. But a thousand calls, long after the price list was built, take the lock a thousand times. Every caller waits its turn, to be told something that never changes.

## 6. Check, Lock, Check Again

Third, check, lock, check again. The same race builds one. The second thread waited for the lock, looked again, and found it already built. And a thousand calls take the lock once. After that, no call waits for anyone.

## 7. Why It Must Be Volatile

Fourth, why the field must be volatile. It is. Without it, the Java memory model lets one thread see the reference before it sees the object fully built. That failure cannot be produced on demand. It depends on the processor and the compiler. So it is not demonstrated here. A test guards the rule instead.

## 8. The Simplest Correct Way

Fifth, the simplest correct way. Before anyone asks, nothing is built. After two calls, one is built, and both got the same one. The JVM builds a class's static state once, when the class is first used. There is no lock to write, and no volatile to forget.

## 9. The Bill

Last, the bill. The double checked version is twenty nine lines. The holder is ten. Double checked locking is ceremony with one way to be subtly wrong. It earns its place only where the holder idiom cannot be used, for example, when creation needs an argument. And an uncontended lock is cheap. Measure before deciding the lock on every call is a problem.

## 10. How To Recognise It

How do you recognise this in code you did not write? A volatile static field, an if (x == null), a synchronized block, and another if (x == null). A private static nested Holder class with one field. Lazy<T> and Suppliers.memoize in libraries. A comment that says why the field is volatile.

## 11. The Verdict

Here is my verdict, plainly. Prefer the class holder idiom, or an enum, for a lazy shared object. If creation needs an argument or can fail and be retried, use double-checked locking, with a volatile field, a local variable, and a test that guards the volatile. If you have not measured the lock as a problem, take the lock on every call.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? Nearly always. Most lazy initialisation can use a holder, an eager static, or a lock on every call, and the cost of a wrong double check is a bug you cannot reproduce.

## 14. Thanks for Watching

That's Double-Checked Locking. If you take one sentence away, take this one: double-checked locking saves the lock after the build, and costs a rule you can break without seeing it. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, remove the volatile keyword and explain why a test cannot fail, and what that means. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
