package com.jk.explore.dependencyinjection.app;

/** The top of the application. It is given everything it needs. */
public class Storefront {

    private final CheckoutService checkout;
    private final ReceiptPrinter printer;
    private final Auditor auditor;

    public Storefront(CheckoutService checkout, ReceiptPrinter printer, Auditor auditor) {
        this.checkout = checkout;
        this.printer = printer;
        this.auditor = auditor;
    }

    public String order(long price) {
        String receipt = checkout.place(price);
        printer.print(receipt);
        auditor.audit("order placed");
        return receipt;
    }
}
