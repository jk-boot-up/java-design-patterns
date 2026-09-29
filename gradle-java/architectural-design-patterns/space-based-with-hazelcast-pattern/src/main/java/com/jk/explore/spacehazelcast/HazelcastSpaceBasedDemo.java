package com.jk.explore.spacehazelcast;

import com.hazelcast.map.IMap;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;

/**
 * The five acts, with three real Hazelcast members as the processing units.
 */
public final class HazelcastSpaceBasedDemo {

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();

        out.add("ONE. App servers, one database.");
        SlowDatabase direct = new SlowDatabase();
        long start = System.nanoTime();
        for (int i = 0; i < 300; i++) {
            direct.sellOne();
        }
        long dbMillis = (System.nanoTime() - start) / 1_000_000;
        out.add("  300 kettle orders, each written to the database: " + (dbMillis > 1400 ? "over 1.4 s" : "under 1.4 s")
                + "; more app servers would only queue for the same database");

        SlowDatabase database = new SlowDatabase();
        try (Grid grid = new Grid(3, database)) {
            IMap<String, Integer> stock = grid.stock(0);
            stock.set("KETTLE-1", 1000);

            out.add("");
            out.add("TWO. Three Hazelcast members, the stock in their memory.");
            out.add("  cluster formed: " + grid.members() + " members");
            int before = database.writes();
            start = System.nanoTime();
            for (int i = 0; i < 300; i++) {
                grid.stock(i % 3).executeOnKey("KETTLE-1", new SellOne());
            }
            long gridMillis = (System.nanoTime() - start) / 1_000_000;
            out.add("  300 orders spread over the 3 units: " + (gridMillis < 1000 ? "under 1 s" : "over 1 s")
                    + "; database writes during the orders: " + (database.writes() - before));

            out.add("");
            out.add("THREE. One grid, not three copies to keep in step.");
            out.add("  stock read on each unit: [" + grid.stock(0).get("KETTLE-1") + ", "
                    + grid.stock(1).get("KETTLE-1") + ", " + grid.stock(2).get("KETTLE-1") + "]");
            out.add("  each key lives on one owner, with a backup on another member; every unit asks the owner");

            out.add("");
            out.add("FOUR. The database catches up in the background.");
            long deadline = System.currentTimeMillis() + 30_000;
            while (database.stock() != 700 && System.currentTimeMillis() < deadline) {
                Thread.sleep(50);
            }
            int writes = database.writes() - before;
            out.add("  database stock now " + database.stock() + ", after " + (writes <= 3 ? "at most 3" : writes)
                    + " writes for 300 sales: write-behind keeps only the latest value");
            out.add("  no customer waited for any of those writes");

            out.add("");
            out.add("FIVE. The last kettle, and a crash.");
            stock.set("KETTLE-2", 1);
            CompletableFuture<Object> a = CompletableFuture.supplyAsync(() ->
                    grid.stock(1).executeOnKey("KETTLE-2", new SellOne()));
            CompletableFuture<Object> b = CompletableFuture.supplyAsync(() ->
                    grid.stock(2).executeOnKey("KETTLE-2", new SellOne()));
            int sold = (Boolean.TRUE.equals(a.get()) ? 1 : 0) + (Boolean.TRUE.equals(b.get()) ? 1 : 0);
            out.add("  two customers try for the last kettle on two units at once: sold " + sold + " of 2; stock "
                    + stock.get("KETTLE-2"));
            grid.kill(2);
            IMap<String, Integer> survivor = grid.stock(0);
            out.add("  unit 3 crashes: KETTLE-1 on the survivors still " + survivor.get("KETTLE-1")
                    + ", its backup copy took over");
            out.add("  the bill: every unit holds the data in memory, the cluster must be run and watched, and");
            out.add("  if the whole grid stops before write-behind runs, the latest sales never reach the database");
        }
        return out;
    }

    private HazelcastSpaceBasedDemo() {
    }
}
