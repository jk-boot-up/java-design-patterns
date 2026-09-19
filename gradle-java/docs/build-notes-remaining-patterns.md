# Build notes: the last 16 registered patterns

This report covers four things worth knowing about how the final batch of patterns was built: the choice to
simulate infrastructure, two demo corrections, one amended commit, and how commits are attributed.

## 1. Simulations, not real infrastructure

**What was done.** The four platform patterns (Blue-Green and Canary, Feature Toggle, Service Mesh,
Consumer-Driven Contract), Serverless and Event-Driven Architecture are written as small plain-Java
simulations. There is no Docker, no Kubernetes, no message broker and no cloud account behind them.

| Project | What stands in for the real thing |
| --- | --- |
| Blue-Green and Canary | A `Router` that sends request number *n* to blue or green by a fixed rule (`n mod 100` against the green share) |
| Feature Toggle | A map of switches read at run time; rollout by customer number modulo 100 |
| Service Mesh | A `Mesh` class that applies one retry, identity and counting policy at each call |
| Consumer-Driven Contract | Contracts as data and a `Verifier` loop over a provider's answer, which is a map |
| Serverless | A `Platform` on a counted clock that starts, keeps warm and drops instances |
| Event-Driven Architecture | An in-memory append-only log with readers that keep their own position |

**Why.** Every demo prints numbers that the tests assert exactly, for example "5 of 200 requests failed" or
"stock 8 without a duplicate check, 9 with one". That only works if a run cannot vary. Real infrastructure
brings timing, start-up delay and network behaviour, so the same demo would print different numbers on
different machines. A counted clock and fixed routing rules remove that. It also matches the repository's
standing approach of forcing each failure to reproduce on every run, with no `Thread.sleep`.

**What it costs.**
- A learner does not see the pattern against the real tool (Istio, LaunchDarkly, Pact, Lambda, Kafka).
  Each project's README lists what it is not, under its non-goals, and names the real tools under
  "Where you have seen it".
- The simulations are teaching models. Their numbers, such as a cold start of 5 ticks or a price of 2 per
  tick for a server, are units chosen to show where a balance tips, not measurements.
- The repository does allow real infrastructure where it is genuinely needed, chiefly in the platform
  category. None of these six projects needed it to teach their point, so none uses it. A later optional
  tier could add real versions, as the Sidecar and Consul projects do.

## 2. Demo output corrected after review

Two demos printed text that did not match what the code did. Both were caught before the projects were
committed as final, and both are fixed.

- **Fluent Interface, act one.** The line described a call with the two booleans as `true, false`, but the
  code ran `false, true`. The label now matches the call, so the swapped-argument example is honest.
- **Callback, act six.** The demo sorted its log by the numeric labels it had itself attached, so the
  "order the lines run in" was manufactured and hid the point. The sort was removed. The demo now prints
  the real run order and states the actual point: the line that asks stock is written below the block that
  ships, and it runs first. The narration and README were regenerated to match.

In the same pass, the Callback README's introduction was reworded, because it described its relation to
Guarded Suspension awkwardly.

## 3. An amended local commit

The Microkernel commit was created before its generated documents existed, because the content build step
had failed part-way on a helper-function mistake in the content file. After fixing that and re-running the
build, the missing docs were added by amending the commit, `Add microkernel`, rather than leaving a second
"fix docs" commit. The commit had not been pushed at the time, so no published history was rewritten. The
Serverless commit was amended the same way, to fix a grammar slip ("a always-on server").

## 4. Commit attribution

None of the commits in this batch carries a `Co-Authored-By` trailer or any mention of Claude or Anthropic.
This follows the repository owner's standing instruction that the history shows them as sole author. The
commit helper used for the batch prints a count of trailer matches after each commit, and that count was 0
every time. The same rule covers pull request descriptions.

## State at the end

- 16 patterns built in this stretch, plus Two-Phase Termination just before them: 146 projects in 11
  categories.
- Category READMEs and their HTML twins updated, and the root README's category table and counts rewritten.
- All commits pushed; `origin/main` is at `816bd48`.
