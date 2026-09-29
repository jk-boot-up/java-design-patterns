package com.jk.explore.spacebased;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.BooleanSupplier;

/**
 * The five acts: everyone waits on one database, processing units with the data in memory, replication, the database kept up to date in the background, and the bill.
 */
public final class SpaceBasedDemo {

    static final int ORDERS = 300;

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    static void pause(long ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    /** Sends the orders from several threads, spread over the given servers; returns milliseconds taken. */
    static long sale(List<BooleanSupplier> servers, int orders, AtomicInteger sold) throws InterruptedException {
        List<Thread> threads = new ArrayList<>();
        long t0 = System.nanoTime();
        int perThread = orders / servers.size();
        for (BooleanSupplier server : servers) {
            threads.add(new Thread(() -> {
                for (int i = 0; i < perThread; i++) {
                    if (server.getAsBoolean()) {
                        sold.incrementAndGet();
                    }
                }
            }));
        }
        threads.forEach(Thread::start);
        for (Thread t : threads) {
            t.join();
        }
        return (System.nanoTime() - t0) / 1_000_000;
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();

        out.add("ONE. Three app servers, one database.");
        CentralDatabase shared = new CentralDatabase(1000);
        long ms1 = sale(List.of(shared::takeOne, shared::takeOne, shared::takeOne), ORDERS, new AtomicInteger());
        out.add("  " + ORDERS + " kettle orders: " + (ms1 >= 1400 ? "over 1.4 s" : ms1 + " ms") + "; every order queued for the database");
        CentralDatabase shared6 = new CentralDatabase(1000);
        long ms6 = sale(List.of(shared6::takeOne, shared6::takeOne, shared6::takeOne,
                shared6::takeOne, shared6::takeOne, shared6::takeOne), ORDERS, new AtomicInteger());
        out.add("  six app servers: " + (ms6 >= 1400 ? "still over 1.4 s" : ms6 + " ms") + "; the database is the limit, not the servers");

        out.add("");
        out.add("TWO. Processing units, each with the data in memory.");
        CentralDatabase db = new CentralDatabase(1000);
        DataWriter writer = new DataWriter(db, 100);
        DataGrid grid = new DataGrid(writer);
        List<ProcessingUnit> units = new ArrayList<>();
        for (String name : new String[] {"unit-1", "unit-2", "unit-3"}) {
            ProcessingUnit u = new ProcessingUnit(name, 1000, grid);
            grid.join(u);
            units.add(u);
        }
        AtomicInteger sold = new AtomicInteger();
        long ms2 = sale(List.of(units.get(0)::takeOne, units.get(1)::takeOne, units.get(2)::takeOne), ORDERS, sold);
        out.add("  " + sold.get() + " orders in " + (ms2 < 300 ? "under 0.3 s" : ms2 + " ms") + "; no order touched the database");

        out.add("");
        out.add("THREE. The data grid keeps the copies in step.");
        out.add("  before replication each unit has seen only its own sales: "
                + units.stream().map(u -> u.name() + " " + u.stock()).toList());
        int writesBefore = db.writes();
        grid.flush();
        out.add("  after replication: " + units.stream().map(u -> u.name() + " " + u.stock()).toList());

        out.add("");
        out.add("FOUR. The database catches up in the background.");
        out.add("  database stock now " + db.stock() + ", written in " + (db.writes() - writesBefore) + " batches of 100, not " + ORDERS + " writes");
        out.add("  no customer waited for any of those writes");

        out.add("");
        out.add("FIVE. The bill: copies can disagree for a moment.");
        CentralDatabase db5 = new CentralDatabase(1);
        DataGrid grid5 = new DataGrid(new DataWriter(db5, 100));
        ProcessingUnit a = new ProcessingUnit("unit-1", 1, grid5);
        ProcessingUnit b = new ProcessingUnit("unit-2", 1, grid5);
        grid5.join(a);
        grid5.join(b);
        boolean soldA = a.takeOne();
        boolean soldB = b.takeOne();
        grid5.flush();
        out.add("  one kettle left; two customers buy it on two units before the grid catches up");
        out.add("  unit-1 sold: " + soldA + ", unit-2 sold: " + soldB + "; stock after replication: " + a.stock());
        out.add("  and a unit that crashes before the grid copies its sales loses them");
        return out;
    }

    private SpaceBasedDemo() {
    }
}
