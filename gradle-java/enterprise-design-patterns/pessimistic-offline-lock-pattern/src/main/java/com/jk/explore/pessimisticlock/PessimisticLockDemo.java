package com.jk.explore.pessimisticlock;

import java.time.Duration;
import java.util.List;

public class PessimisticLockDemo {

    static final Duration FIFTEEN_MINUTES = Duration.ofMinutes(15);

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static String tryLock(LockManager locks, String sku, String who) {
        try {
            locks.acquire(sku, who, FIFTEEN_MINUTES);
            return "got the lock";
        } catch (LockedBy e) {
            return "refused, " + e.getMessage();
        }
    }

    private static void one() {
        System.out.println("ONE. Lock first, then edit.");
        Clock clock = new Clock();
        LockManager locks = new LockManager(clock);
        System.out.println("  clerk A asks for MUG-BLUE: " + tryLock(locks, "MUG-BLUE", "A") + ".");
        System.out.println("  clerk B asks for MUG-BLUE: " + tryLock(locks, "MUG-BLUE", "B") + ".");
        System.out.println("  the clash was stopped before B could start editing.");
    }

    private static void two() {
        System.out.println("TWO. No lost update.");
        Clock clock = new Clock();
        LockManager locks = new LockManager(clock);
        ProductStore store = new ProductStore(locks);
        locks.acquire("MUG-BLUE", "A", FIFTEEN_MINUTES);
        ProductStore.Product before = store.read("MUG-BLUE");
        store.write("MUG-BLUE", "A", new ProductStore.Product("MUG-BLUE", 1200, before.stock()));
        locks.release("MUG-BLUE", "A");
        locks.acquire("MUG-BLUE", "B", FIFTEEN_MINUTES);
        ProductStore.Product seen = store.read("MUG-BLUE");
        System.out.println("  A raised the price and let go. B then locks and reads: price " + seen.pricePence() + ", stock " + seen.stock() + ".");
        store.write("MUG-BLUE", "B", new ProductStore.Product("MUG-BLUE", seen.pricePence(), 40));
        System.out.println("  B saves the stock count: " + store.read("MUG-BLUE") + ". nothing was overwritten.");
    }

    private static void three() {
        System.out.println("THREE. The bill: waiting.");
        Clock clock = new Clock();
        LockManager locks = new LockManager(clock);
        locks.acquire("MUG-BLUE", "A", FIFTEEN_MINUTES);
        int refusals = 0;
        for (int minute = 0; minute < 3; minute++) {
            if (tryLock(locks, "MUG-BLUE", "B").startsWith("refused")) {
                refusals++;
            }
            clock.advance(Duration.ofMinutes(1));
        }
        System.out.println("  B tries once a minute while A edits: " + refusals + " refusals, and B has done nothing useful.");
        System.out.println("  a lock trades lost updates for waiting.");
    }

    private static void four() {
        System.out.println("FOUR. The bill: a lock nobody let go of.");
        Clock clock = new Clock();
        LockManager locks = new LockManager(clock);
        ProductStore store = new ProductStore(locks);
        locks.acquire("MUG-BLUE", "A", FIFTEEN_MINUTES);
        System.out.println("  A goes to lunch without letting go. B, straight away: " + tryLock(locks, "MUG-BLUE", "B") + ".");
        clock.advance(Duration.ofMinutes(10));
        System.out.println("  after 10 minutes: " + tryLock(locks, "MUG-BLUE", "B") + ".");
        clock.advance(Duration.ofMinutes(6));
        System.out.println("  after 16 minutes the lock has expired: " + tryLock(locks, "MUG-BLUE", "B") + ".");
        try {
            store.write("MUG-BLUE", "A", new ProductStore.Product("MUG-BLUE", 1, 1));
        } catch (IllegalStateException e) {
            System.out.println("  A comes back and saves: " + e.getMessage() + ".");
        }
    }

    private static void five() {
        System.out.println("FIVE. The bill: two clerks, each waiting for the other.");
        Clock clock = new Clock();
        LockManager locks = new LockManager(clock);
        locks.acquire("MUG-BLUE", "A", FIFTEEN_MINUTES);
        locks.acquire("TEA-050", "B", FIFTEEN_MINUTES);
        System.out.println("  A holds MUG-BLUE and now needs TEA-050: " + tryLock(locks, "TEA-050", "A") + ".");
        System.out.println("  B holds TEA-050 and now needs MUG-BLUE: " + tryLock(locks, "MUG-BLUE", "B") + ".");
        System.out.println("  neither can move. that is a deadlock, and it lasts until a lock expires.");
        LockManager ordered = new LockManager(new Clock());
        for (String who : List.of("A", "B")) {
            List<String> wanted = List.of("TEA-050", "MUG-BLUE").stream().sorted().toList();
            String outcome = "took both";
            for (String sku : wanted) {
                String result = tryLock(ordered, sku, who);
                if (result.startsWith("refused")) {
                    outcome = "stopped at " + sku + " holding nothing else";
                    break;
                }
            }
            System.out.println("  taking locks in a fixed order, " + who + " " + outcome + ".");
        }
    }

    private static void six() {
        System.out.println("SIX. How much to lock.");
        LockManager coarse = new LockManager(new Clock());
        System.out.println("  one lock on the whole catalogue: A " + tryLock(coarse, "catalogue", "A") + ". B, editing a different product: " + tryLock(coarse, "catalogue", "B") + ".");
        LockManager fine = new LockManager(new Clock());
        System.out.println("  a lock per product: A " + tryLock(fine, "MUG-BLUE", "A") + ". B on TEA-050: " + tryLock(fine, "TEA-050", "B") + ".");
        System.out.println("  the smaller the thing locked, the fewer people wait. the more things locked, the more there is to forget and to deadlock on.");
    }
}
