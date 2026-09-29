package com.jk.explore.writethrough;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: a write that goes round the cache, write-through, fast reads, a refused write, and the bill.
 */
public final class WriteThroughDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    static String pounds(long p) {
        return String.format("£%d.%02d", p / 100, p % 100);
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. A price change goes round the cache.");
        Database db1 = new Database();
        CacheAside aside = new CacheAside(db1);
        aside.pagePrice("KETTLE-1");
        aside.priceJobUpdate("KETTLE-1", 2700);
        out.add("  the nightly job cuts the kettle to £27.00 in the database");
        out.add("  product page (cache): " + pounds(aside.pagePrice("KETTLE-1")) + "; checkout (database): " + pounds(db1.read("KETTLE-1")));
        out.add("  the job forgot to clear the cache; the customer sees one price and pays another");

        out.add("");
        out.add("TWO. Write-through: every write goes through the cache.");
        Database db2 = new Database();
        WriteThroughStore store = new WriteThroughStore(db2);
        store.get("KETTLE-1");
        store.put("KETTLE-1", 2700);
        out.add("  the job calls store.put(KETTLE-1, £27.00): database written, then cache, before it returns");
        out.add("  product page: " + pounds(store.get("KETTLE-1")) + "; checkout: " + pounds(db2.read("KETTLE-1")));

        out.add("");
        out.add("THREE. Reads come from the cache.");
        int readsBefore = db2.reads();
        for (int i = 0; i < 100; i++) {
            store.get("KETTLE-1");
        }
        out.add("  100 page views: " + (db2.reads() - readsBefore) + " database reads; cache hits so far " + store.hits());

        out.add("");
        out.add("FOUR. A refused write changes nothing.");
        db2.setReadOnly(true);
        try {
            store.put("KETTLE-1", 2500);
        } catch (IllegalStateException e) {
            out.add("  price job tries £25.00: " + e.getMessage());
        }
        out.add("  page and database both still say " + pounds(store.get("KETTLE-1")) + "; the two never disagree");
        db2.setReadOnly(false);

        out.add("");
        out.add("FIVE. The bill: every write waits, and the cache fills.");
        Database db5 = new Database();
        WriteThroughStore s5 = new WriteThroughStore(db5);
        for (int i = 0; i < 1000; i++) {
            s5.put("SKU-" + i, 1000 + i);
        }
        out.add("  the nightly job updates 1000 prices: " + db5.waitedMs() / 1000.0 + " s spent waiting for the database");
        out.add("  and all 1000 now sit in the cache, though most will never be viewed");
        return out;
    }

    private WriteThroughDemo() {
    }
}
