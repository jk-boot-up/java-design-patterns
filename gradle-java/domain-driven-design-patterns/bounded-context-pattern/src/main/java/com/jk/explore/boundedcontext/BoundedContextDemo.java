package com.jk.explore.boundedcontext;

import com.jk.explore.boundedcontext.naive.GodCustomer;
import com.jk.explore.boundedcontext.sales.Buyer;
import com.jk.explore.boundedcontext.sales.SalesContext;
import com.jk.explore.boundedcontext.shared.CustomerId;
import com.jk.explore.boundedcontext.shared.EventBus;
import com.jk.explore.boundedcontext.shipping.Recipient;
import com.jk.explore.boundedcontext.shipping.ShippingContext;
import com.jk.explore.boundedcontext.support.Contact;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDate;
import java.util.stream.Stream;

public class BoundedContextDemo {

    static final LocalDate TODAY = LocalDate.of(2026, 9, 19);
    static final CustomerId ADA = new CustomerId("ada");

    public static void main(String[] args) throws IOException {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. One Customer for everyone.");
        System.out.println("  fields in the company-wide Customer class: " + GodCustomer.fieldCount() + ".");
        System.out.println("  each context uses a handful of them, and every one depends on the whole class, so one context's change is every context's change.");
    }

    private static void two() {
        System.out.println("TWO. The same word, three meanings.");
        Buyer buyer = new Buyer(ADA, "Ada Lovelace", 500_000, LocalDate.of(2026, 8, 1));
        Recipient recipient = new Recipient(ADA, "Ada Lovelace", "12 Byron Road", 1);
        Contact contact = new Contact(ADA, "Ada Lovelace", "020 7946 0000", 0);
        System.out.println("  is Ada an active customer?");
        System.out.println("    Sales, bought in the last 90 days:  " + buyer.isActive(TODAY) + ".");
        System.out.println("    Shipping, a parcel on its way:      " + recipient.isActive() + ".");
        System.out.println("    Support, an open ticket:            " + contact.isActive() + ".");
        System.out.println("  one class cannot answer all three. each answer is right, in its own context.");
    }

    private static void three() {
        System.out.println("THREE. A model for each context.");
        System.out.println("  Sales:    Buyer with " + Buyer.class.getRecordComponents().length + " fields: credit limit, last purchase.");
        System.out.println("  Shipping: Recipient with " + Recipient.class.getRecordComponents().length + " fields: address, parcels in transit.");
        System.out.println("  Support:  Contact with " + Contact.class.getRecordComponents().length + " fields: phone, open tickets.");
        System.out.println("  none of them knows the others' types. they share one thing, the CustomerId.");
    }

    private static void four() {
        System.out.println("FOUR. The contexts talk by events.");
        EventBus bus = new EventBus();
        SalesContext sales = new SalesContext(bus);
        ShippingContext shipping = new ShippingContext(bus);
        sales.register(new Buyer(ADA, "Ada Lovelace", 500_000, LocalDate.of(2026, 8, 1)));
        shipping.register(new Recipient(ADA, "Ada Lovelace", "12 Byron Road", 1));
        sales.rename(ADA, "Ada King");
        System.out.println("  Sales renames Ada. Sales says: " + sales.buyer(ADA).name() + ". Shipping says: " + shipping.recipient(ADA).name() + ". events waiting: " + bus.waiting() + ".");
        bus.deliver();
        System.out.println("  after the event is delivered, Shipping says: " + shipping.recipient(ADA).name() + ".");
        System.out.println("  Shipping translated a Sales fact into a change to its own Recipient. it never saw a Buyer.");
    }

    private static void five() throws IOException {
        System.out.println("FIVE. The boundary can be checked.");
        System.out.println("  imports of one context's types by another: " + crossImports() + ".");
        System.out.println("  Shipping can add a field to Recipient and nothing in Sales or Support needs to change.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        System.out.println("  Ada's name is now stored three times: Sales, Shipping, Support.");
        System.out.println("  between the rename and the delivery, two contexts disagreed about her name. that gap is called eventual consistency.");
        System.out.println("  and every context needs its own translator for every event it cares about.");
    }

    /** Counts the imports in which one context's package uses another context's package. */
    static int crossImports() throws IOException {
        String[] contexts = {"sales", "shipping", "support"};
        int count = 0;
        try (Stream<Path> files = Files.walk(Path.of("src/main/java"))) {
            for (Path file : files.filter(f -> f.toString().endsWith(".java")).toList()) {
                String text = Files.readString(file);
                for (String own : contexts) {
                    if (file.toString().contains("/" + own + "/")) {
                        for (String other : contexts) {
                            if (!other.equals(own) && text.contains("import com.jk.explore.boundedcontext." + other + ".")) {
                                count++;
                            }
                        }
                    }
                }
            }
        }
        return count;
    }
}
