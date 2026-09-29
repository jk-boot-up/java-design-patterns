package com.jk.explore.extensionobject;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: the ever-growing product class, extensions, asking for a role, a new role, and the bill.
 */
public final class ExtensionObjectDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. One product class with a field for every feature.");
        FatProduct mug = new FatProduct("MUG-1", "mug", 800L, null, null, null, null, null);
        out.add("  FatProduct has " + mug.fields() + " fields; a mug leaves " + mug.emptyFields() + " of them empty");
        out.add("  adding subscriptions means a 9th field, in the class the whole shop depends on");

        out.add("");
        out.add("TWO. A small core product, with extra roles attached.");
        Product ebook = new Product("EBOOK-1", "Java Basics e-book", 999)
                .with(Extensions.Download.class, new Extensions.Download("https://shop.example/d/EBOOK-1", 3));
        Product kettle = new Product("KETTLE-1", "kettle", 3000)
                .with(Extensions.Warranty.class, new Extensions.Warranty(2));
        Product mug2 = new Product("MUG-1", "mug", 800);
        out.add("  e-book roles: " + ebook.extensionNames() + "; kettle: " + kettle.extensionNames()
                + "; mug: " + mug2.extensionNames());
        out.add("  the Product class has 3 fields and knows nothing about downloads or warranties");

        out.add("");
        out.add("THREE. Checkout asks each product: do you have this role?");
        Checkout.afterPayment(List.of(ebook, kettle, mug2)).forEach(a -> out.add("  " + a));
        out.add("  the mug has no extra roles, so nothing extra happens");

        out.add("");
        out.add("FOUR. A new role, added without editing Product.");
        Product beans = new Product("BEANS-1", "coffee beans", 1200)
                .with(Extensions.Subscription.class, new Extensions.Subscription(4));
        Checkout.afterPayment(List.of(beans)).forEach(a -> out.add("  " + a));
        out.add("  Product.java unchanged; the subscriptions team owns its own record");

        out.add("");
        out.add("FIVE. The bill: nothing checks that a role is there.");
        Product ebook2 = new Product("EBOOK-2", "Java Advanced e-book", 1499);
        List<String> none = Checkout.afterPayment(List.of(ebook2));
        out.add("  an e-book added without its Download role: " + none.size() + " actions after payment");
        out.add("  the compiler did not complain; the customer paid and got nothing");
        out.add("  and reading the Product class no longer tells you what a product can do");
        return out;
    }

    private ExtensionObjectDemo() {
    }
}
