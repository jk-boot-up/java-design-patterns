# Leader Election with Kubernetes Pattern — Video Narration Script

## 1. Leader Election with Kubernetes

Hello, and welcome. This video explains the Leader Election pattern in Java, using a real Kubernetes cluster. This video is presented by Jayasekhar Konduru. First, a simple definition. When several copies of a program are running, leader election lets them agree that exactly one of them does a job. One copy holds a lease: a claim that runs out unless it is renewed. The others wait, and take the lease if the renewals stop. In our online store, the shop runs three copies of its reporting service. So one can crash without the service going away. Every night, exactly one of them must send the manager the sales report. Not three reports, and not none. By the end, you will hear a real Kubernetes server refuse a write. A dead leader leave nobody in charge for a whole lease. A frozen leader wake up and send the report after losing its lease. And the one check that stops it.

## 2. The Scenario

Here is the scenario. The reporting service runs as three copies, called A, B, and C. Each copy is a separate program. Every night, exactly one of them must send the sales report. The plain Java version already solved this with a lease. But its lease was an object inside one program, with a clock that only moved when the program said so. This time, the lease lives in a real Kubernetes server. The copies are real programs. And the clock is the real one. That changes three things.

## 3. Three Copies, Nobody In Charge

First demo: three copies, and nobody in charge. Three copies start, as three separate programs. None of them asks who is in charge. Each is told to send the nightly sales report. And each one does. A sends it, B sends it, and C sends it. The manager receives the same report three times.

## 4. Kubernetes' Words

Before the next demo, some words, through an everyday picture. Imagine a staff room with a notice board. On it is one note, saying who does tonight's job, and until when. The person named on it rewrites the time every few minutes. If the time on the note has passed, anyone else may cross the name out, and write their own. In Kubernetes, the group of machines is called a cluster. The notice board is a program called the A P I server. It stores records, and lets others read and write them. The note is called a Lease. The name on it is the holder. And rewriting the time is called renewing. Our lease lasts five seconds without a renewal. Every note also has a version number, which goes up with each write. If you try to write based on an old version, the server refuses you. That refusal is called a conflict. And one thing the board never does. It never takes a note down because it is old. It does not look at the clock at all.

## 5. One Holds The Lease

Second demo: one copy holds the lease. A starts first, finds no lease, and writes one with its own name. The lease says: holder A, lasting five seconds. A renews it every second. B and C start next. They read the lease, see it is fresh, and are told the leader is A. All three are asked to send the report. Only A sends it. Then two writes are made to the lease, both based on the same version. The first is accepted. The second is refused, with a conflict, because its version is out of date. That refusal is what stops two copies winning at the same moment. And it is the only rule the server enforces.

## 6. The Elector's Settings

The copies do not do this by hand. They use a library called Fabric8, which talks to Kubernetes from Java. It has a built-in elector: the part that keeps asking for the lease, and keeps renewing it. It takes four settings. The lease lasts five seconds. The holder stops leading if it cannot renew for four seconds. Everyone asks again every second. And on a clean shutdown, the holder hands the lease back. Then the elector tells the copy three things. You now lead. You no longer lead. And someone new leads.

## 7. The Leader Stops

Third demo: the leader stops. A is shut down cleanly. On its way out, its elector hands the lease back, by clearing the holder's name. B or C sees the empty lease at its next check. And takes over within a couple of seconds. Then the new leader is killed outright. It gets no chance to hand anything back. So the lease still names the dead copy. The last copy must wait until five seconds have passed since the last renewal, by its own clock. So it takes over only after about one whole lease. For that time, nobody leads. The others cannot tell a dead leader from a slow one, so they wait. Which copy wins, and exactly how long it takes, vary slightly from run to run. So the demo describes them, rather than counting them.

## 8. Who Reads The Clock

Here is how the pieces fit, in words. Three copies, each its own program. And one lease record in the A P I server, which they all read and write. The leader, A, rewrites the lease every second. The lease holds the holder's name, the five seconds, and the time of the last renewal. B and C read it. They add five seconds to the last renewal, and compare that with their own clocks. Notice who reads the clock. Not the server. Each copy. The server only stores the note, and checks the version. And the manager's inbox, where the report goes, sits outside Kubernetes altogether.

## 9. Two Who Think They Lead

Fourth demo, and this is the one to remember. A leads, and B waits. A is told to send the report. It checks that it leads, and it does. So it starts building the report. At that moment, A's whole program freezes. Every thread stops, including the one that renews the lease. A long memory clean-up in Java can do exactly that. No renewals arrive. After five seconds, by B's clock, B takes the lease. B sends the report. Then A wakes up. It finishes the report it had started, and sends it. Because when it checked, it was the leader. The report was sent twice. First B, then A.

## 10. The Lease's Own Record

The lease's own record proves A was wrong. When A sent its report, the lease already named B. And B had renewed it after A's last renewal. A's elector did notice, in the end. When A woke up, it saw it had missed its deadline, and said A no longer leads. But the check had already been made. And the report was already on its way. Nothing on the server could have stopped this. The server never takes a lease away. It only stores it. A check is not a promise.

## 11. Fencing

Fifth demo: fencing. The answer is a number called a fencing token. When a copy starts leading, it keeps the lease's count of how many times the holder has changed. That count only ever goes up. Every report carries it. And the inbox remembers the highest one it has seen. A's token is zero. B's token is one. B sends first, with one. When A wakes and sends with zero, the inbox refuses it. Zero is older than one. Only B's report was sent. The lease could not stop A. But the inbox, the thing being written to, could.

## 12. The Bill

Sixth demo: the bill. B is killed. A is still running. But Fabric8's elector cannot be restarted. When A lost the lease earlier, its elector stopped for good. Two whole leases later, the lease still names the dead B. And nobody leads. A only leads again when it starts a brand-new elector, with token two. In Kubernetes, the usual answer is simpler. A copy that loses the lease exits, and Kubernetes starts it again. Three more costs. A five-second lease means a dead leader can go unnoticed for up to five seconds. A shorter lease lets one slow moment cost a healthy leader its job. Each copy judges the lease by its own clock. So machines whose clocks disagree can take over too early. And all of it needs a Kubernetes server, just for one nightly report.

## 13. What The Simulation Left Out

So what did the plain Java version get right? The whole shape. One leader at a time. A gap when the leader dies. A leader that wakes up, and acts on an old belief. And a token as the answer. All of that holds on a real server. But it left out three things. First, its lease decided for itself when it had expired. A real Kubernetes lease never expires on the server. Each copy decides, with its own clock. Second, the real server checks the version on every write, and refuses an old one. Third, a real elector that loses the lease leaves the race for good. And someone has to start a new one.

## 14. The Verdict

So, here is the verdict. Use a Kubernetes lease to pick one copy, and let the elector do the renewing. Then settle three things, because Kubernetes will not. One. A leader's belief that it leads can be out of date at any moment. So everything it writes must carry a token, and the receiver must check it. Two. A copy that loses the lease should exit, and be restarted. Not stay alive with no way back. Three. The lease length is a choice. Short notices a dead leader quickly. Long survives a slow moment. You cannot have both.

## 15. What Is Real, And When Not

A quick, honest note about this demo. This is a real Kubernetes server, version one point thirty-seven. It runs in a one-machine cluster, made by a tool called kind, inside a single container. The demo creates the cluster at the start, and deletes it at the end. It never touches your own Kubernetes settings. You need Docker switched on, and kind installed. Every number you heard comes from the program's own output. So, when is this too much? If the job is safe to run twice, run it everywhere. If one copy is enough, run one, and let Kubernetes restart it. A lease only earns its keep when several copies must run, and exactly one may act.

## 16. Thanks for Watching

That's Leader Election, with Kubernetes. If you remember one sentence, make it this one. The lease tells everyone else who leads, but only the thing a leader writes to can stop a leader that has already lost. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Make a copy exit the moment it loses the lease. Then work out what would bring it back. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
