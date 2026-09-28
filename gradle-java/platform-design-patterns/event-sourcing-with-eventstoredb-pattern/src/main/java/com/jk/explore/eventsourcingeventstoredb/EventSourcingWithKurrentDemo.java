package com.jk.explore.eventsourcingeventstoredb;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import io.kurrent.dbclient.EventData;
import io.kurrent.dbclient.StreamNotFoundException;

/**
 * Six acts against a real KurrentDB server (the database once called EventStoreDB), started and
 * stopped by this program.
 *
 * <p>The shop's loyalty scheme gives one point per pound and lets customers spend points on later
 * orders. Every customer's points live in one stream of events. Nothing stores a balance; it is
 * added up from the stream each time. The acts show a real log being read back, two checkouts
 * spending the same points at the same moment with and without the check that stops them, a retry
 * the server recognises, a screen that catches up by reading the log, and what deleting a stream
 * really removes.
 */
public class EventSourcingWithKurrentDemo {

    static final LocalDate MARCH_1 = LocalDate.of(2025, 3, 1);
    static final LocalDate MARCH_3 = LocalDate.of(2025, 3, 3);
    static final LocalDate MARCH_8 = LocalDate.of(2025, 3, 8);
    static final LocalDate MARCH_14 = LocalDate.of(2025, 3, 14);
    static final LocalDate APRIL_2 = LocalDate.of(2025, 4, 2);
    static final int SPEND = 100;

    public static void main(String[] args) {
        if (!KurrentServer.containerRuntimeAvailable()) {
            System.out.println(KurrentServer.NO_RUNTIME_ADVICE);
            return;
        }
        try (KurrentServer server = new KurrentServer()) {
            try {
                server.start();
            } catch (RuntimeException e) {
                System.out.println(KurrentServer.WOULD_NOT_START_ADVICE);
                return;
            }
            one(server);
            two(server);
            three(server);
            four(server);
            SupportDashboard dashboard = five(server);
            six(server, dashboard);
            dashboard.close();
        }
    }

    /** The four things that happened to C-4417 in March, as the plain-Java twin tells them. */
    static List<LoyaltyEvent> march(String customer) {
        return List.of(
                new PointsAwarded(customer, 60, "ORD-8801", MARCH_1),
                new PointsRedeemed(customer, 25, "ORD-8814", MARCH_3),
                new PointsAwarded(customer, 120, "ORD-8907", MARCH_8),
                new PointsExpired(customer, 15, MARCH_14));
    }

    /**
     * Writes March one event at a time, each append expecting the revision the last one produced,
     * which is how a careful writer builds a stream.
     */
    static long writeMarch(LoyaltyLog log, String customer) {
        long revision = -1;
        for (LoyaltyEvent event : march(customer)) {
            revision = revision < 0
                    ? log.appendToNewStream(customer, EventJson.toEventData(event))
                    : log.appendExpecting(customer, revision, EventJson.toEventData(event));
        }
        return revision;
    }

    /** Append, and read it back from another connection. */
    private static void one(KurrentServer server) {
        System.out.println("ONE. A real log, read back from the start.");
        try (LoyaltyLog writer = new LoyaltyLog(server.connect());
             LoyaltyLog reader = new LoyaltyLog(server.connect())) {
            long last = writeMarch(writer, "C-4417");
            System.out.println("  4 events appended to the stream " + LoyaltyLog.streamFor("C-4417")
                    + ". KurrentDB numbered them revision 0 to " + last + ".");
            System.out.println("  a second connection reads the stream from the start and adds it up:");
            LoyaltyLog.History history = reader.read("C-4417");
            int running = 0;
            for (int i = 0; i < history.events().size(); i++) {
                LoyaltyEvent e = history.events().get(i);
                running += e.effectOnBalance();
                System.out.printf("    revision %d  %s  %-44s balance %d%n", i, e.on(), e.because(), running);
            }
            System.out.println("  balance: " + history.balance() + " points, from " + history.events().size()
                    + " events. nothing stores " + history.balance() + "; it was added up just now.");
            System.out.println("  the client can append to a stream, read it, and delete all of it. it has no call that changes one event.");
        }
    }

    /** Two checkouts, no check. Both spend the same points. */
    private static void two(KurrentServer server) {
        System.out.println("TWO. Two checkouts at once, with no check.");
        try (LoyaltyLog log = new LoyaltyLog(server.connect())) {
            writeMarch(log, "C-5120");
        }
        Race race = race(server, "C-5120", LoyaltyLog.Check.NONE);
        Checkout.Look seen = race.firstLook();
        System.out.println("  C-5120 has " + seen.balance() + " points. the website and the phone app both look: "
                + seen.balance() + " points, at revision " + seen.revision() + ".");
        System.out.println("  both decide " + SPEND + " is not more than " + seen.balance() + ", and both append a redemption with the check off.");
        System.out.println("  both appends accepted, at revisions " + race.accepted().get(0) + " and " + race.accepted().get(1)
                + ". balance now: " + race.after().balance() + " points.");
        System.out.println("  the customer spent " + (2 * SPEND) + " points they had only " + seen.balance() + " of, and the server was never asked to mind.");
    }

    /** The same race, with the expected revision. One is refused. */
    private static void three(KurrentServer server) {
        System.out.println("THREE. The same race, with the expected revision.");
        try (LoyaltyLog log = new LoyaltyLog(server.connect())) {
            writeMarch(log, "C-5121");
        }
        Race race = race(server, "C-5121", LoyaltyLog.Check.EXPECTED_REVISION);
        LoyaltyLog.StreamMovedOn refusal = race.refused().get(0);
        Checkout.Look seen = race.firstLook();
        System.out.println("  C-5121 has " + seen.balance() + " points. both checkouts look: " + seen.balance()
                + " points, at revision " + seen.revision() + ". both append, expecting revision " + seen.revision() + ".");
        System.out.println("  appends accepted: " + race.accepted().size() + ", at revision " + race.accepted().get(0)
                + ". appends refused: " + race.refused().size() + ".");
        System.out.println("  the refusal is WrongExpectedVersion: " + refusal.getMessage() + ".");
        System.out.println("  the refused checkout looks again: " + race.secondLook().balance() + " points, at revision "
                + race.secondLook().revision() + ". " + SPEND + " is more than " + race.secondLook().balance()
                + ", so it tells the customer no.");
        System.out.println("  balance now: " + race.after().balance() + " points. nothing was locked; the server compared one number.");
    }

    /** A retry after a lost reply, with a new event id and with the same one. */
    private static void four(KurrentServer server) {
        System.out.println("FOUR. A retry the server recognises.");
        PointsAwarded award = new PointsAwarded("C-5122", 45, "ORD-9001", APRIL_2);
        try (LoyaltyLog log = new LoyaltyLog(server.connect())) {
            log.append("C-5122", EventJson.toEventData(award));
            log.append("C-5122", EventJson.toEventData(award));
            LoyaltyLog.History careless = log.read("C-5122");
            System.out.println("  the shop awards C-5122 45 points for order ORD-9001, loses the reply, and sends the award again.");
            System.out.println("  sent again with a new event id: " + careless.events().size() + " awards for ORD-9001 in the stream. balance "
                    + careless.balance() + ".");

            UUID id = UUID.randomUUID();
            EventData once = EventJson.toEventData(id, award.withCustomer("C-5123"));
            long first = log.appendToNewStream("C-5123", once);
            long retry = log.appendToNewStream("C-5123", EventJson.toEventData(id, award.withCustomer("C-5123")));
            LoyaltyLog.History careful = log.read("C-5123");
            System.out.println("  for C-5123 the first send is written at revision " + first
                    + ", expecting a stream that does not exist yet.");
            System.out.println("  sent again with the same event id and the same expectation: the server answers revision "
                    + retry + " again, and writes nothing.");
            System.out.println("  " + careful.events().size() + " award in the stream. balance " + careful.balance()
                    + ". the retry was recognised, not refused, so the shop never has to guess.");
        }
    }

    /** A screen built only by reading the log, started last, catching up. */
    private static SupportDashboard five(KurrentServer server) {
        System.out.println("FIVE. A screen that catches up.");
        SupportDashboard dashboard = new SupportDashboard(server.connect());
        dashboard.start();
        Poll.until("the dashboard to catch up", dashboard::caughtUp);
        System.out.println("  the support dashboard starts after all of that and asks for every loyalty stream from the start.");
        System.out.println("  it receives " + dashboard.eventsWhenCaughtUp() + " events that were already stored, and the server tells it it has caught up.");
        System.out.println("  it shows C-4417 = " + dashboard.balanceOf("C-4417") + ", C-5120 = " + dashboard.balanceOf("C-5120")
                + ", C-5121 = " + dashboard.balanceOf("C-5121") + ", C-5122 = " + dashboard.balanceOf("C-5122") + ".");
        try (LoyaltyLog log = new LoyaltyLog(server.connect())) {
            long revision = log.read("C-4417").revision();
            log.appendExpecting("C-4417", revision, EventJson.toEventData(new PointsAwarded("C-4417", 20, "ORD-9300", APRIL_2)));
        }
        Poll.until("the dashboard to show the new award", () -> Integer.valueOf(160).equals(dashboard.balanceOf("C-4417")));
        System.out.println("  a new order awards C-4417 20 points. moments later the dashboard shows C-4417 = "
                + dashboard.balanceOf("C-4417") + ", with " + dashboard.eventsSeen() + " events received in all.");
        System.out.println("  nobody told the dashboard. it is a second copy, kept current by reading the log.");
        return dashboard;
    }

    /** What deleting a stream removes, and what it does not. */
    private static void six(KurrentServer server, SupportDashboard dashboard) {
        System.out.println("SIX. The bill: deleting a stream.");
        try (LoyaltyLog log = new LoyaltyLog(server.connect())) {
            log.delete("C-5122");
            String read;
            try {
                log.read("C-5122");
                read = "it is still there";
            } catch (StreamNotFoundException e) {
                read = "stream not found";
            }
            System.out.println("  customer C-5122 asks to be forgotten, and the shop deletes the stream " + LoyaltyLog.streamFor("C-5122") + ".");
            System.out.println("  reading the stream now: " + read + ".");
            System.out.println("  reading the store's whole log, every stream at once: " + log.countInWholeLog("C-5122")
                    + " events of " + LoyaltyLog.streamFor("C-5122") + " are still there, until a clean-up called a scavenge runs.");
            System.out.println("  the support dashboard still shows C-5122 = " + dashboard.balanceOf("C-5122")
                    + ". the delete reached the stream, not the copies built from it.");
            long reused = log.append("C-5122", EventJson.toEventData(new PointsAwarded("C-5122", 10, "ORD-9400", APRIL_2)));
            LoyaltyLog.History after = log.read("C-5122");
            System.out.println("  a later order writes to the same stream name. it is accepted at revision " + reused
                    + ", not 0, and reading the stream shows " + after.events().size() + " event.");
            System.out.println("  and this server ran with security off: no TLS, no passwords, in 1 container. production must never run like that.");
        }
    }

    /** What happened when two checkouts spent the same points at the same moment. */
    record Race(Checkout.Look firstLook, List<Long> accepted, List<LoyaltyLog.StreamMovedOn> refused, Checkout.Look secondLook,
                LoyaltyLog.History after) {
    }

    /**
     * The website and the phone app each look at the customer's points, wait for each other so that
     * both have looked before either writes, and then both try to spend {@link #SPEND} at once.
     */
    static Race race(KurrentServer server, String customer, LoyaltyLog.Check check) {
        CyclicBarrier bothHaveLooked = new CyclicBarrier(2);
        List<Long> accepted = Collections.synchronizedList(new ArrayList<>());
        List<LoyaltyLog.StreamMovedOn> refused = Collections.synchronizedList(new ArrayList<>());
        List<Checkout.Look> firstLooks = Collections.synchronizedList(new ArrayList<>());
        List<Checkout.Look> secondLooks = Collections.synchronizedList(new ArrayList<>());
        ExecutorService pool = Executors.newFixedThreadPool(2);
        try (Checkout website = new Checkout("the website", new LoyaltyLog(server.connect()));
             Checkout app = new Checkout("the phone app", new LoyaltyLog(server.connect()))) {
            List<Future<?>> running = new ArrayList<>();
            int n = 0;
            for (Checkout checkout : List.of(website, app)) {
                String order = "ORD-920" + (++n);
                running.add(pool.submit(() -> {
                    Checkout.Look seen = checkout.look(customer);
                    firstLooks.add(seen);
                    bothHaveLooked.await(30, TimeUnit.SECONDS);
                    try {
                        accepted.add(checkout.redeem(customer, seen, SPEND, order, APRIL_2, check));
                    } catch (LoyaltyLog.StreamMovedOn e) {
                        refused.add(e);
                        secondLooks.add(checkout.look(customer));
                    }
                    return null;
                }));
            }
            for (Future<?> f : running) {
                f.get(60, TimeUnit.SECONDS);
            }
            List<Long> sorted = new ArrayList<>(accepted);
            Collections.sort(sorted);
            try (LoyaltyLog reader = new LoyaltyLog(server.connect())) {
                if (!firstLooks.get(0).equals(firstLooks.get(1))) {
                    throw new IllegalStateException("the two checkouts saw different things: " + firstLooks);
                }
                return new Race(firstLooks.get(0), sorted, List.copyOf(refused), secondLooks.isEmpty() ? null : secondLooks.get(0),
                        reader.read(customer));
            }
        } catch (Exception e) {
            throw new IllegalStateException("the race did not finish", e);
        } finally {
            pool.shutdownNow();
        }
    }
}
