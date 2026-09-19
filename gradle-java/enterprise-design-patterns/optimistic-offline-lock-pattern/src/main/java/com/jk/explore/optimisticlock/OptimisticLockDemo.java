package com.jk.explore.optimisticlock;

import java.util.function.UnaryOperator;

public class OptimisticLockDemo {

    static final Product MUG = new Product("MUG-BLUE", 1000, 50);

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static String describe(Product p) {
        return String.format("price £%d.%02d, stock %d", p.pricePence() / 100, p.pricePence() % 100, p.stock());
    }

    private static void one() {
        System.out.println("ONE. No lock: the last write wins.");
        LastWriteWinsStore store = new LastWriteWinsStore();
        store.insert(MUG);
        Product clerkA = store.load("MUG-BLUE");
        Product clerkB = store.load("MUG-BLUE");
        store.save(clerkA.withPrice(1200));
        store.save(clerkB.withStock(40));
        System.out.println("  clerk A raises the price to 12.00 and saves. clerk B counts 40 in stock and saves.");
        System.out.println("  the row now: " + describe(store.load("MUG-BLUE")) + ". clerk A's price has vanished, and no error was raised.");
    }

    private static void two() {
        System.out.println("TWO. A version on every row.");
        OptimisticStore store = new OptimisticStore();
        store.insert(MUG);
        Versioned<Product> clerkA = store.load("MUG-BLUE");
        Versioned<Product> clerkB = store.load("MUG-BLUE");
        store.save(clerkA.with(clerkA.value().withPrice(1200)));
        System.out.println("  clerk A saves: accepted. the row is now at version " + store.load("MUG-BLUE").version() + ".");
        try {
            store.save(clerkB.with(clerkB.value().withStock(40)));
        } catch (StaleWrite e) {
            System.out.println("  clerk B saves: " + e.getMessage() + ".");
        }
        System.out.println("  the row still says: " + describe(store.load("MUG-BLUE").value()) + ".");
    }

    private static void three() {
        System.out.println("THREE. Reload, reapply, save.");
        OptimisticStore store = new OptimisticStore();
        store.insert(MUG);
        Versioned<Product> clerkB = store.load("MUG-BLUE");
        Versioned<Product> clerkA = store.load("MUG-BLUE");
        store.save(clerkA.with(clerkA.value().withPrice(1200)));
        int attempts = saveWithRetry(store, "MUG-BLUE", p -> p.withStock(40), clerkB);
        System.out.println("  clerk B is refused, reloads, reapplies the stock count, and saves after " + attempts + " attempts.");
        System.out.println("  the row: " + describe(store.load("MUG-BLUE").value()) + ". both changes survived.");
    }

    /** Applies a change and saves it, starting from a row that may already be stale. Returns the attempts used. */
    static int saveWithRetry(OptimisticStore store, String sku, UnaryOperator<Product> change, Versioned<Product> firstRead) {
        Versioned<Product> loaded = firstRead;
        for (int attempt = 1; ; attempt++) {
            try {
                store.save(loaded.with(change.apply(loaded.value())));
                return attempt;
            } catch (StaleWrite e) {
                loaded = store.load(sku);
            }
        }
    }

    private static void four() {
        System.out.println("FOUR. The version is per row, not per field.");
        OptimisticStore store = new OptimisticStore();
        store.insert(MUG);
        Versioned<Product> priceClerk = store.load("MUG-BLUE");
        Versioned<Product> stockClerk = store.load("MUG-BLUE");
        store.save(priceClerk.with(priceClerk.value().withPrice(1200)));
        boolean refused = false;
        try {
            store.save(stockClerk.with(stockClerk.value().withStock(40)));
        } catch (StaleWrite e) {
            refused = true;
        }
        System.out.println("  one clerk changed the price and another changed the stock. different fields. second save refused: " + refused + ".");
        System.out.println("  a conflict that was not one. a finer version, per field, would have let both through, at the price of more bookkeeping.");
    }

    private static void five() {
        System.out.println("FIVE. The bill: a busy row.");
        OptimisticStore store = new OptimisticStore();
        store.insert(new Product("MUG-BLUE", 1000, 0));
        int clerks = 10;
        int attempts = 0;
        java.util.List<Versioned<Product>> reads = new java.util.ArrayList<>();
        for (int i = 0; i < clerks; i++) {
            reads.add(store.load("MUG-BLUE"));
        }
        for (int i = 0; i < clerks; i++) {
            attempts += saveWithRetry(store, "MUG-BLUE", p -> p.withStock(p.stock() + 1), reads.get(i));
        }
        System.out.println("  " + clerks + " clerks each add one to the stock of the same product, all having read it at the start.");
        System.out.println("  final stock: " + store.load("MUG-BLUE").value().stock() + ". saves attempted: " + attempts + ". saves refused: " + (attempts - clerks) + ".");
        System.out.println("  nothing was lost, and a row that everyone wants is a row where most of the work is repeated.");
    }

    private static void six() {
        System.out.println("SIX. The bill: you find out at the end.");
        OptimisticStore store = new OptimisticStore();
        store.insert(MUG);
        Versioned<Product> editor = store.load("MUG-BLUE");
        Product edited = editor.value();
        int edits = 0;
        for (int i = 0; i < 5; i++) {
            edited = edited.withStock(edited.stock() - 1);
            edits++;
        }
        Versioned<Product> other = store.load("MUG-BLUE");
        store.save(other.with(other.value().withPrice(900)));
        try {
            store.save(editor.with(edited));
        } catch (StaleWrite e) {
            System.out.println("  a user makes " + edits + " changes over a long session. on save: " + e.getMessage() + ".");
        }
        System.out.println("  all " + edits + " changes are discarded, and the user learns it only now. the cost of a conflict is paid when it is found.");
    }
}
