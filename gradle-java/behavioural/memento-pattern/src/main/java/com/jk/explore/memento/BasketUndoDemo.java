package com.jk.explore.memento;

/**
 * Runs the same shopping trip through both baskets, so the difference is
 * something you watch rather than something you are told.
 *
 * <p>The trip: three products, a voucher, and then the shopper removes the
 * laptop stand by mistake and presses undo.
 */
public final class BasketUndoDemo {

    public static void main(String[] args) {
        naive();
        System.out.println();
        withMemento();
    }

    private static void naive() {
        System.out.println("=== undo without a snapshot ===");

        NaiveBasket basket = new NaiveBasket();
        basket.add("USB-C cable", 9, 2);
        basket.add("Laptop stand", 34, 1);
        basket.add("Desk mat", 18, 1);
        basket.applyVoucher("SAVE5");

        System.out.println("  the basket the shopper built:");
        System.out.println(basket.describe());

        basket.save();                       // "so we can undo this"
        basket.remove("Laptop stand");       // ...removed by mistake
        System.out.println("  after removing the laptop stand by mistake:");
        System.out.println(basket.describe());

        basket.undo();
        System.out.println("  after pressing undo:");
        System.out.println(basket.describe());
        System.out.println("  ^ the stand did not come back, and neither did anything else");

        // The second bug, on a fresh basket so the first one does not hide it.
        NaiveBasket second = new NaiveBasket();
        second.add("Desk mat", 18, 1);
        second.applyVoucher("SAVE5");
        second.save();
        second.applyVoucher("");         // the shopper clears the voucher...
        second.undo();                   // ...and changes their mind
        System.out.println("  and on a fresh basket, undoing a cleared voucher:");
        System.out.println("    voucher: " + (second.voucher().isEmpty()
                ? "(none)" : second.voucher()) + "    total: £" + second.total());
        System.out.println("  ^ the voucher stays cleared. Even with the aliasing fixed it would,");
        System.out.println("    because save() never wrote the voucher down in the first place.");
    }

    private static void withMemento() {
        System.out.println("=== undo with a snapshot ===");

        Basket basket = new Basket();
        BasketHistory history = new BasketHistory();

        basket.add("USB-C cable", 9, 2);
        basket.add("Laptop stand", 34, 1);
        basket.add("Desk mat", 18, 1);
        basket.applyVoucher("SAVE5");

        System.out.println("  the basket the shopper built:");
        System.out.println(basket.describe());

        history.record(basket, "removed the laptop stand");
        basket.remove("Laptop stand");
        System.out.println("  after removing the laptop stand by mistake:");
        System.out.println(basket.describe());

        String undone = history.undo(basket);
        System.out.println("  after pressing undo (" + undone + "):");
        System.out.println(basket.describe());
        System.out.println("  ^ the stand is back, the voucher is back, the total is back");

        // And the voucher is state too, so it undoes the same way.
        history.record(basket, "removed the voucher");
        basket.applyVoucher("");
        System.out.println("  the shopper then removes the voucher, and undoes that too:");
        history.undo(basket);
        System.out.println("    voucher: " + basket.voucher()
                + "    total: £" + basket.total()
                + "    undo steps left: " + history.size());
    }

    private BasketUndoDemo() {
    }
}
