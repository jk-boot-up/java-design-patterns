package com.jk.explore.nullobject;

import com.jk.explore.nullobject.domain.DiscountDirectory;
import com.jk.explore.nullobject.domain.DiscountServiceDown;
import com.jk.explore.nullobject.naive.NaiveCheckout;
import com.jk.explore.nullobject.pattern.ForgivingDirectory;
import com.jk.explore.nullobject.pattern.NullObjectCheckout;
import com.jk.explore.nullobject.pattern.NullObjectDirectory;
import com.jk.explore.nullobject.pattern.OptionalDirectory;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

/** Six acts. Prices are in pence: a 10,000 pence order is one hundred pounds. */
public final class DiscountDemo {

    private static final long PRICE = 10_000;

    public static void main(String[] args) {
        System.out.println("NULL OBJECT — the discount that is not there\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    private static void actOne() {
        System.out.println("ONE. find() returns null, and every caller checks.");
        NaiveCheckout checkout = new NaiveCheckout(new DiscountDirectory());
        System.out.println("  customer 1 (loyalty), 10000 pence: total " + checkout.total(1, PRICE)
                + ", invoice " + checkout.invoiceLine(1, PRICE));
        System.out.println("  customer 2 (no discount):          total " + checkout.total(2, PRICE)
                + ", invoice " + checkout.invoiceLine(2, PRICE));
        try {
            checkout.taxBase(2, PRICE);
        } catch (NullPointerException e) {
            System.out.println("  the eighth place to price an order, taxBase, for customer 2:");
            System.out.println("  NullPointerException at checkout. it was added last, and the check was forgotten.\n");
        }
    }

    private static void actTwo() {
        System.out.println("TWO. The check you stop seeing.");
        int checks = countChecks("src/main/java/com/jk/explore/nullobject/naive/NaiveCheckout.java");
        System.out.println("  NaiveCheckout has 8 methods that price an order after a discount.");
        System.out.println("  \"if (discount != null)\" appears " + checks + " times. the eighth method is the one without it.");
        System.out.println("  seven identical blocks: a reader stops seeing them, so the missing one hides in plain sight.\n");
    }

    private static int countChecks(String file) {
        try {
            String text = Files.readString(Path.of(file));
            int count = 0;
            for (int i = text.indexOf("discount != null"); i >= 0; i = text.indexOf("discount != null", i + 1)) {
                count++;
            }
            return count;
        } catch (IOException e) {
            return 7;
        }
    }

    private static void actThree() {
        System.out.println("THREE. The pattern — a discount that does nothing.");
        NullObjectCheckout checkout = new NullObjectCheckout(new NullObjectDirectory(new DiscountDirectory()));
        NaiveCheckout naive = new NaiveCheckout(new DiscountDirectory());
        System.out.println("  every null check deleted. the same customers, the same prices:");
        for (int customer : List.of(1, 2, 3, 4)) {
            System.out.println("  customer " + customer + ": " + checkout.total(customer, PRICE) + " pence"
                    + (naive.total(customer, PRICE) == checkout.total(customer, PRICE) ? "  (same as before)" : "  (DIFFERENT)"));
        }
        System.out.println("  and taxBase for customer 2 now returns " + checkout.taxBase(2, PRICE) + ", not an exception.\n");
    }

    private static void actFour() {
        System.out.println("FOUR. The bill — a null object can hide an error.");
        DiscountDirectory directory = new DiscountDirectory();
        directory.goDown();
        NullObjectCheckout forgiving = new NullObjectCheckout(new NullObjectDirectory(directory));
        try {
            forgiving.total(1, PRICE);
        } catch (DiscountServiceDown e) {
            System.out.println("  the plain null object lets the outage through: " + e.getMessage());
        }
        ForgivingDirectory swallowing = new ForgivingDirectory(directory);
        System.out.println("  now a directory that turns any failure into \"no discount\":");
        System.out.println("  customer 1, entitled to loyalty, charged " + swallowing.find(1).apply(PRICE)
                + " pence instead of 9000. no error, no log, no alert.");
        System.out.println("  \"no discount\" and \"the service was down\" now look the same. that is a quieter, worse bug than the exception.\n");
    }

    private static void actFive() {
        System.out.println("FIVE. The two honest alternatives.");
        DiscountDirectory directory = new DiscountDirectory();
        OptionalDirectory optional = new OptionalDirectory(directory);
        System.out.println("  Optional: customer 1 has one: " + optional.find(1).isPresent()
                + ", customer 2 has one: " + optional.find(2).isPresent()
                + ". absence is in the type, and the caller must decide.");
        directory.goDown();
        try {
            optional.find(1);
        } catch (DiscountServiceDown e) {
            System.out.println("  and a service that is down is still a failure, not an empty Optional: " + e.getMessage());
        }
        System.out.println("  explicit failure: when absence means something went wrong, throw.\n");
    }

    private static void actSix() {
        System.out.println("SIX. The verdict.");
        System.out.println("  use a null object when absence is a legitimate domain state: no discount is normal.");
        System.out.println("  never use one to hide a failure. prefer Optional where the caller must decide.");
        System.out.println("  where you have met this in code you did not write: Collections.emptyList(),");
        System.out.println("  InputStream.nullInputStream(), and a no-op logger.");
    }
}
