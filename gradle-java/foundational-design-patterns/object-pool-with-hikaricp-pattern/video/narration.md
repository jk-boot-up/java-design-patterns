# Object Pool with HikariCP Pattern — Video Narration Script

## 1. Object Pool with HikariCP

Hello, and welcome. This video explains the Object Pool pattern with HikariCP, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Object Pool video. That one built a pool by hand, and found four costs. HikariCP is the connection pool inside most Java applications, and the mature answer to several of them. The plain definition, in short: keep a few expensive objects, lend them out, and take them back. By the end you will see which costs a real library solves, and which it cannot.

## 2. The Partner Project

This video assumes the Object Pool video. If you have not seen it, start there. It builds a pool by hand, and finds four costs. A small pooled object is slower than allocating it. A returned object carries its old state. A leak hangs the application. And sizing is a guess. This one is about connections, the one thing worth pooling. It does not teach the pattern again.

## 3. Before The First Line

Before the first line, two new things. HikariCP is a database connection pool. You ask it for a connection, use it, and close it. Closing does not close it. It gives it back. H two is a database that runs in memory, so nothing needs installing. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it.

## 4. It Opens What Demand Needs

Ten payments, one after another, through a pool that is allowed to hold two connections. How many did it open? One. The payments ran one at a time, so one was enough. It opens what demand needs, up to the maximum. Closing the connection each time did not close it. It returned it.

## 5. The Dirty Return

The dirty return, from the hand-built video. One borrower sets auto commit to false, and read only to true, and returns the connection. The next borrower gets the very same connection. Auto commit is true. Read only is false. The pool reset the settings it knows about, on the way back. That is the reset the partner project had to write by hand.

## 6. What It Cannot Reset

But not everything. Ada sets a session variable, inside the database, and returns the connection. Grace borrows it, and reads the variable. Ada Lovelace. The security bug from the hand-built video is still possible. The pool can only reset what it can see. State that lives inside the database session is invisible to it.

## 7. Exhaustion, With A Timeout

Exhaustion. Two borrowers take both connections and never return them. A third caller waits, and after about three hundred milliseconds, it gets an exception with a message worth reading: connection is not available, request timed out. Total two, active two, idle zero. The timeout was already a setting. The hand-built pool needed one you had to remember. Its default here is thirty seconds, so set it. A leak detection setting can also log who never returned a connection.

## 8. Sizing Is Still A Guess

Sizing is still a guess. Four payments at once, each needing fifty milliseconds. A pool of one: they queue. Two hundred and twenty-three. A pool of four: fifty-three. A pool of fifty opens fifty connections, and keeps them idle, for four payments. HikariCP's own documentation argues for small pools. More is not faster.

## 9. What Pooling Buys

What does pooling buy, on real database connections? Opening a new one each time: about thirty-eight microseconds. Borrowing from the pool: about one and a half. And this is in-memory H two, whose connections are cheap. A real database over a network costs far more. That is why this is the one place the pattern is right. The timings vary by machine.

## 10. The Verdict

My verdict, plainly. Pool connections, threads and native handles. Use a library that has already fixed the hard parts. Never pool ordinary objects. And never write your own connection pool. You have just seen how many parts there are to get right.

## 11. Where You Have Met This

You have met this. Every Spring Boot application with a database uses HikariCP. Every data source is a pool. Now you know what it is doing when you close a connection.

## 12. What Was Used

For the record. HikariCP and H two, at the versions from Spring Boot four point one point one's bill of materials. Spring Boot itself is not used in this video.

## 13. What Is Real Here

The same honest admission as everywhere in this course, and short. Everything is real: the pool, the exception message, and the statistics. The only stand-in is the database, H two in memory. The timings vary by machine, and no test asserts one.

## 14. Thanks for Watching

That's the Object Pool with HikariCP. If you take one sentence away, take this one: use a library that has fixed the hard parts, and still reset what it cannot see. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, set the leak detection threshold, and see what it logs. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
