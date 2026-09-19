package com.jk.explore.executearound;

public class ExecuteAroundDemo {

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. Open, use, close, by hand.");
        Pool pool = new Pool();
        Connection c = pool.acquire();
        try {
            c.query("orders");
            throw new IllegalStateException("the query broke");
        } catch (IllegalStateException e) {
            System.out.println("  the query broke, and the code that would close the connection was after it.");
        }
        System.out.println("  connections still open: " + pool.stillOpen() + ". repeat that on every failure, and the pool runs dry.");
    }

    private static void two() {
        System.out.println("TWO. The caller gives the work, the pool does the rest.");
        Pool pool = new Pool();
        try {
            pool.withConnection(c -> {
                c.query("orders");
                throw new IllegalStateException("the query broke");
            });
        } catch (IllegalStateException e) {
            System.out.println("  the same failure: " + e.getMessage() + ".");
        }
        System.out.println("  connections opened: " + pool.opened() + ", still open: " + pool.stillOpen() + ". the closing is in one place, in a finally block, and cannot be forgotten.");
    }

    private static void three() {
        System.out.println("THREE. Getting an answer out.");
        Pool pool = new Pool();
        String rows = pool.withConnection(c -> c.query("orders where id = 7"));
        int size = pool.withConnection(c -> c.query("orders").length());
        System.out.println("  a string came out: " + rows + ". a number came out: " + size + ". still open: " + pool.stillOpen() + ".");
    }

    private static void four() {
        System.out.println("FOUR. All or nothing.");
        Ledger ledger = new Ledger(5000);
        try {
            ledger.inTransaction(l -> {
                l.spend(3000);
                l.spend(3000);
            });
        } catch (IllegalStateException e) {
            System.out.println("  two purchases of 3000 from a credit of 5000: the second failed with \"" + e.getMessage() + "\".");
        }
        System.out.println("  balance afterwards: " + ledger.balance() + ". the first purchase was undone too.");
        ledger.inTransaction(l -> l.spend(3000));
        System.out.println("  one purchase of 3000 that works: balance " + ledger.balance() + ".");
    }

    private static void five() {
        System.out.println("FIVE. The same shape, for measuring.");
        FakeClock clock = new FakeClock();
        Timed timed = new Timed(clock);
        String answer = timed.around(() -> {
            clock.advance(5);
            return "receipt sent";
        });
        System.out.println("  " + answer + " in " + timed.lastTicks() + " ticks.");
        try {
            timed.around(() -> {
                clock.advance(9);
                throw new IllegalStateException("mail server timed out");
            });
        } catch (IllegalStateException e) {
            System.out.println("  and a failing job: " + e.getMessage() + ", still measured: " + timed.lastTicks() + " ticks.");
        }
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        Pool pool = new Pool();
        Connection escaped = pool.withConnection(c -> c);
        try {
            escaped.query("orders");
        } catch (IllegalStateException e) {
            System.out.println("  the caller let the connection out of the block, and used it later: " + e.getMessage() + ". the block cannot stop that.");
        }
        System.out.println("  the caller's code is now inside a lambda: it cannot return early, and it cannot throw a checked exception without help.");
        System.out.println("  and with two resources the blocks nest, one inside the other, so the real work drifts to the right.");
    }
}
