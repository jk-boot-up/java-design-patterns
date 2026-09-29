package com.jk.explore.writebehind;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: writing every change, writing behind, the database down, a crash, and the bill.
 */
public final class WriteBehindDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Three customers each change their cart ten times: add, raise, lower, remove... Returns ms waited. */
    static int shop(CartStore store) {
        int waited = 0;
        for (String cart : List.of("priya", "tom", "ana")) {
            for (int n = 1; n <= 10; n++) {
                waited += store.set(cart, n % 2 == 0 ? "mug" : "tea", n);
            }
        }
        return waited;
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. Write every change straight to the database.");
        Database d1 = new Database();
        int waited = shop(new WriteThroughStore(d1));
        out.add("  3 customers, 10 cart changes each: " + d1.writes() + " database writes");
        out.add("  customers waited " + waited + " ms in total, " + Database.MS_PER_WRITE + " ms on every click");

        out.add("");
        out.add("TWO. Write to memory now, to the database later.");
        Database d2 = new Database();
        WriteBehindStore store = new WriteBehindStore(d2);
        int waited2 = shop(store);
        out.add("  the same 30 changes: customers waited " + waited2 + " ms; " + store.waiting() + " carts waiting");
        out.add("  flush after 5 seconds: " + store.flush() + " database writes, one per cart");
        out.add("  priya's cart in the database: " + new java.util.TreeMap<>(d2.load("priya")));

        out.add("");
        out.add("THREE. The database goes down.");
        d2.setUp(false);
        store.set("priya", "kettle", 1);
        store.set("tom", "mug", 2);
        out.add("  2 more changes; customers waited 0 ms and kept shopping");
        out.add("  flush: " + (store.flush() < 0 ? "failed, database unavailable" : "ok")
                + "; " + store.waiting() + " carts still waiting");
        d2.setUp(true);
        out.add("  database back; next flush: " + store.flush() + " writes");

        out.add("");
        out.add("FOUR. The server crashes before a flush.");
        store.set("priya", "teapot", 1);
        store.set("priya", "mug", 12);
        store.set("ana", "tea", 3);
        out.add("  3 changes made, flush due in 5 seconds");
        out.add("  crash: " + store.crash() + " changes lost; priya's teapot is not in the database: "
                + !d2.load("priya").containsKey("teapot"));

        out.add("");
        out.add("FIVE. The bill: the database is behind.");
        Database d3 = new Database();
        WriteBehindStore s3 = new WriteBehindStore(d3);
        s3.set("priya", "kettle", 1);
        s3.flush();
        s3.set("priya", "kettle", 3);
        out.add("  checkout sees " + s3.get("priya").get("kettle") + " kettles; the stock report reading the database sees "
                + d3.load("priya").get("kettle"));
        out.add("  so never write behind an order, a payment or stock: only what you can afford to lose");
        return out;
    }

    private WriteBehindDemo() {
    }
}
