# Session Guide — Sidecar, With the Proxy Written in Java

**One hour, for a group who have already done the Sidecar session.**

This session does not work on its own. It is the second of a pair, and its whole argument
depends on the group already believing that a sidecar is a good idea. If half the room has
not seen §41, run that one instead and come back to this next time.

The shape of the hour is unusual for this course, and it is deliberate: the group spends
the first twenty minutes discovering that the tool they were sold last time cannot do
something reasonable, the middle twenty fixing it, and the last twenty finding out that the
fix costs more than the problem did. People leave persuaded *not* to write their own proxy,
which is the correct outcome.

---

## Learning Objectives

By the end, participants should be able to:

1. **Explain why nginx retries immediately**, in terms of upstream groups, and say why that
   is correct for a pool of machines and wrong in front of a single supplier.
2. **Name the contract between a service and its sidecar** — an address — and say what that
   makes replaceable.
3. **Describe the difference between a claim and a demonstration** in this context: two
   proxies in two languages on one port, with a service whose source file did not change.
4. **List what you lose** when twenty-two lines of configuration become forty lines of Java,
   including the loss that is not on any invoice: the fence.
5. **State the narrow rule** and apply it to a case from their own system.
6. **Say why a swap is a rollout**, and what happens to a request that arrives in the gap.

---

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:05 | Setup, and one question from last time |
| 0:05–0:18 | The sentence that cannot be said |
| 0:18–0:28 | The swap |
| 0:28–0:36 | Code walkthrough |
| 0:36–0:48 | Exercises |
| 0:48–0:57 | The bill, and the fence |
| 0:57–1:00 | Wrap-up |

---

## 0:00–0:05 — Setup, And One Question From Last Time

```bash
cd gradle-java/platform-design-patterns/sidecar-java-proxy-pattern
./gradlew test    # 30 tests
./gradlew run     # seven acts
```

Open with the question the last session ended on, and take answers before showing anything:

> Last time we said a sidecar is language-independent — the proxy can be written in a
> language nobody here knows, and the service will not care. **How would you prove that?**

Let the room propose things. Most groups reach for behaviour: run it with the new proxy and
check the payments still work. Note that answer on the board, because you are going to come
back and reject it in the walkthrough. A service that merely *behaves* the same afterwards
is a service somebody may have carefully rebuilt.

---

## 0:05–0:18 — The Sentence That Cannot Be Said

Run Acts 2 and 3.

The move here is to keep the room angry at nginx for as long as possible and then take the
anger away. Show Act 2 first — three attempts at 1, 2 and 3 milliseconds against a provider
that recovers at 300 — and ask what went wrong. Almost everybody says the retry policy is
misconfigured. Someone will offer to fix it.

Let them try. Ask for the directive they would add. Give it a minute.

Then explain the upstream group: nginx has no retry counter, it has a list of servers and a
rule that says move to the next one, and §41's configuration lists the provider's address
three times because that is how you spell three attempts. Moving to the next server happens
immediately, and that is *right* when the next server is a different machine.

The sentence to land, slowly:

> **Nobody wrote a bug. The sentence the provider asked for does not exist in the language
> the policy is written in.**

Two discussion questions, three minutes:

- Where else have you used a tool correctly, inside its design, and still got a bad result
  because your case was not the case it was designed for?
- Which half of the provider's letter did the shop keep? (The half that limits the shop.
  Sit with that for a moment.)

---

## 0:18–0:28 — The Swap

Run Acts 4 and 5.

Show `port.install(java)` on its own and ask the room what that method takes. It takes a
proxy. It does not take the service, it has no way to notify one, and it has no way to
restart one — **there is no such parameter because there is no such step.**

Then put Act 2 and Act 5 side by side and ask the room what is different. Push until
somebody says *nothing except when the attempts happen*. Three attempts in both. Same
allowance, same provider, same payment. The provider was not renegotiated with and did not
get less traffic.

> **The spacing was the difference between a customer walking away and a coffee maker being
> sold, and it cost the provider nothing.**

---

## 0:28–0:36 — Code Walkthrough

Four files, in this order.

**`NginxProxy.forward` and `JavaProxy.forward`, side by side.** Put them on the screen
together. They are the same loop with four lines missing from one. End on the comment at the
bottom of the nginx version — *and here is where the waiting would go, if it could be said
at all.*

**`LocalPort`.** The hinge of the whole project, and it has one field. `install`, `vacate`,
`send`. Point out that `send` throws *connection refused* when nothing is bound, because the
group will need that in ten minutes.

**`PaymentsService`.** Read the whole class out loud; it is short. Two fields and a method
that forwards. Then show `ServiceStaysEmptyTest`, which reads this file with the comments
stripped and fails if *retry*, *backoff*, *timeout*, *keystore* or *tls* appear in it.

**`TheSwapTest`.** Come back to the board from minute five. The test does not check that the
service behaves the same; it asserts `assertSame` on the service's identity, before and
after. Ask the room why that is the stronger claim.

---

## 0:36–0:48 — Exercises

### Exercise 1 — Make it greedier, and watch a test object (everyone, 4 min)

Change `ProxyPolicy.agreedWithTheProvider()` to allow six attempts instead of three, and run
the tests.

Several fail. The one to read aloud is the assertion that both proxies spend the *same*
allowance. Discuss: the shop could have fixed Act 2 by asking for more attempts instead of
better spacing. Why is that a different — and worse — change? Who pays for it?

Put it back.

### Exercise 2 — Stop the doubling (everyone, 3 min)

In `JavaProxy.forward`, delete `backoff *= 2;` so every wait is two hundred milliseconds.
Run the demo. The payment still succeeds — the third attempt lands at 401ms, which is after
300.

So why keep the doubling? Ask before answering. The answer is not about this one payment: it
is about every service in the shop failing at the same instant and coming back at the same
instant. A fixed wait synchronises the whole estate against a provider that has just started
breathing again.

Then ask what a production proxy would add here that this one deliberately does not
(a small random jitter), and why it is absent (a random number would make the demo print
something different on every run, and the tests assert on its exact output).

### Exercise 3 — Put a business rule in the proxy (discussion, 3 min)

Ask the room to write, in Java, a check in `JavaProxy.forward` that refuses refunds older
than ninety days. It takes about four lines and everybody can see how.

Now ask them to write the same rule in an nginx `location` block.

> **The limitation and the fence were the same thing.** You took the fence down at the exact
> moment you took the limitation away, and nothing in the build will ever tell you that
> somebody walked through the gap.

This is the most important three minutes of the session.

### Exercise 4 — Stretch

Make `LocalPort.install` refuse to bind if something is already bound, so a swap *must* go
through `vacate` first. Then ask what would have to change to make a zero-gap swap possible
at all — and notice that the answer involves two ports, a period where both proxies are
running, and something deciding when to move the traffic. That answer is §43.

---

## 0:48–0:57 — The Bill, And The Fence

Run Acts 6 and 7.

Act 6 first, and read the number out: **attempts that reached the provider, zero.** Healthy
provider, healthy network, healthy service. Ask where that failure would show up in the
provider's dashboards. It would not — the request never left the machine.

Draw the conclusion as an operational rule rather than a warning: start the new proxy before
stopping the old one, move one service at a time, keep the old proxy installable. Say plainly
why the last one matters — the fastest fix for a bad new proxy at three in the morning is the
old one.

Then Act 7, and go through the bill item by item rather than reading it as a list. Forty
lines you now own. TLS termination, the access log, connection pooling — gone until somebody
writes them, and forty lines that grow all of that back are not forty lines any more. A JVM
beside every service. And the fence from Exercise 3.

Close the section by asking the room to vote: **would you do this swap in your system?**

Most rooms say no, once they have seen the bill, and that is the right answer. The point of
the hour is not the swap. It is that the swap *was available*, in an afternoon, because the
contract was an address.

---

## 0:57–1:00 — Wrap-Up

One rule on the board:

> **Swap the proxy when the thing you need cannot be said in the configuration language at
> all.** Not when it is awkward. Not when the config file has grown ugly. Not when you would
> rather write Java.

And one question to take away:

> What does your team talk to through an address rather than through a library — and what
> could you therefore replace on a Tuesday afternoon without asking anybody's permission?

---

## Facilitator Notes

**The room will want to blame nginx, and you must not let them.** The session only works if
the group ends up respecting the tool. Every time somebody says nginx is limited, agree —
and then point out that the limitation is why twenty years of configuration files in their
company contain no business logic.

**Do not let Exercise 3 become a joke.** It is funny for about fifteen seconds and then it
is the most serious point of the session. If the room laughs, ask who would find the refund
rule six months later, and how.

**If somebody asks why not just use Envoy or HAProxy**, that is an excellent question and
the honest answer is: usually you should. This project is not an argument for hand-written
proxies. It is an argument that the *interface* — an address — is what makes any of those
options reachable at all. If a better off-the-shelf proxy can express the sentence, use it,
and the swap is exactly the same swap.

**If somebody asks about the millisecond hop**, that was §41's Act 7 and it has not changed
here. Both proxies pay it.

**Timing.** The likeliest overrun is the walkthrough, because the two `forward` methods
invite a line-by-line reading. Show them side by side, name the four missing lines, and move
on. The exercises are where the learning is.

**If you only have thirty minutes:** setup, Acts 2 and 3, Act 5, Exercise 3, and the bill.
Drop the code walkthrough entirely — the two `forward` methods can be a screenshot.

---

## Materials Checklist

- [ ] JDK 21, and `./gradlew test` passing (30 tests) before anybody arrives
- [ ] `./gradlew run` output on screen, in a fixed-width font, at least 76 columns
- [ ] `NginxProxy.forward` and `JavaProxy.forward` open side by side in one window
- [ ] `docs/animation.html` open in a browser tab, for the groups who prefer the picture
- [ ] `docs/sequence-diagram.md` rendered, for the two blocks of arrival times
- [ ] A whiteboard, for the maintenance question at minute five and the vote at minute
      fifty-five
- [ ] The §41 session's closing slide, if the same room did it — the claim you are about to
      pay off is on it
