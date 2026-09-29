package com.jk.explore.privateclassdata;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * The five acts: a method that changes its own figures, private class data, no way to write, working state beside it, and the bill.
 */
public final class PrivateClassDataDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. The invoice's own method changes its figures.");
        LooseInvoice loose = new LooseInvoice("INV-7", 10000);
        out.add("  invoice INV-7 for £100.00, printed with a 10% staff discount");
        out.add("  first print:  " + loose.printWithStaffDiscount(10));
        out.add("  second print: " + loose.printWithStaffDiscount(10));
        out.add("  the invoice itself now says " + pounds(loose.netPence()) + "; it was issued for £100.00");

        out.add("");
        out.add("TWO. The figures live in a private data object.");
        Invoice invoice = new Invoice("INV-7", "Priya", 10000);
        for (int i = 1; i <= 3; i++) {
            out.add("  print " + i + ": " + invoice.printWithStaffDiscount(10));
        }
        out.add("  the invoice still says " + pounds(invoice.netPence()));

        out.add("");
        out.add("THREE. Nothing can write the figures, not even the invoice.");
        long writers = Arrays.stream(InvoiceData.class.getDeclaredMethods()).map(Method::getName)
                .filter(n -> n.startsWith("set")).count();
        out.add("  InvoiceData setters: " + writers + "; its fields are final");
        out.add("  the loose invoice's shortcut, data.netPence = ..., would not compile");

        out.add("");
        out.add("FOUR. Working state can still change, beside the data.");
        out.add("  times printed: " + invoice.timesPrinted() + "; figures unchanged: " + pounds(invoice.netPence()));
        out.add("  the class decides which fields may change, one by one");

        out.add("");
        out.add("FIVE. The bill: one more class, one more hop.");
        out.add("  every read is data.netPence() instead of netPence");
        out.add("  for a class with two fields and no risky methods, it is ceremony");
        return out;
    }

    static String pounds(long pence) {
        return String.format("£%d.%02d", pence / 100, pence % 100);
    }

    private PrivateClassDataDemo() {
    }
}
