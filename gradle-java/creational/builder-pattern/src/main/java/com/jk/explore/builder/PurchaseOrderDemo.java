package com.jk.explore.builder;

import java.util.List;

/**
 * Builds the same kind of order three ways: by hand with the fluent
 * builder, through a fixed preset, and then deliberately wrong, to show
 * that the missing pieces are caught before an object exists.
 */
public class PurchaseOrderDemo {

    public static void main(String[] args) {
        Address home = new Address("14 Elm Street", "Leeds", "LS1 4AP", "UK");

        LineItem mug = new LineItem("MUG-01", "Ceramic mug", Money.pounds(8.50), 2);
        LineItem book = new LineItem("BK-42", "Effective Java", Money.pounds(34.99), 1);

        // Built by hand: only the options this particular order needs are chained on.
        PurchaseOrder handBuilt = PurchaseOrder.builder("ORD-9001", "CUST-100")
                .addItem(mug)
                .addItem(book)
                .shippingAddress(home)
                .giftMessage("Happy birthday!")
                .couponCode("WELCOME10")
                .build();
        System.out.println(handBuilt);
        System.out.println("  subtotal " + handBuilt.subtotal() + ", total " + handBuilt.total());

        // The same shape, without a caller ever writing the recipe out again.
        PurchaseOrder gift = PurchaseOrderPresets.giftOrder(
                "ORD-9002", "CUST-101", List.of(mug), home, "Congratulations!");
        System.out.println(gift);

        PurchaseOrder standard = PurchaseOrderPresets.standardOrder(
                "ORD-9003", "CUST-102", List.of(book), home);
        System.out.println(standard);

        PurchaseOrder express = PurchaseOrderPresets.expressOrder(
                "ORD-9004", "CUST-103", List.of(mug, book), home);
        System.out.println(express);
        System.out.println("  notes: " + express.notes().orElse("(none)"));

        // Reusing a builder after build() does not reach back into the finished order.
        PurchaseOrder.Builder reused = PurchaseOrder.builder("ORD-9005", "CUST-104")
                .addItem(mug)
                .shippingAddress(home);
        PurchaseOrder first = reused.build();
        reused.addItem(book).priority();
        PurchaseOrder second = reused.build();
        System.out.println("first items: " + first.items().size() + ", second items: " + second.items().size());

        // The two required facts are checked at build(), not one field at a time.
        try {
            PurchaseOrder.builder("ORD-9006", "CUST-105").build();
        } catch (IllegalStateException e) {
            System.out.println("Rejected: " + e.getMessage());
        }

        try {
            PurchaseOrder.builder("ORD-9007", "CUST-106").addItem(mug).build();
        } catch (IllegalStateException e) {
            System.out.println("Rejected: " + e.getMessage());
        }
    }
}
