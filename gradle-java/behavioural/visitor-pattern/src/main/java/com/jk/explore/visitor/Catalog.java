package com.jk.explore.visitor;

/**
 * The catalog the whole project reports on.
 *
 * <p>It is the tree from {@code structural/composite-pattern} — the same
 * Electronics root, the same Accessories and Cables branches, the same
 * phone, case, charger and cable at the same prices — with three additions
 * the reports need: stock levels, a spare battery that is restricted, and a
 * bundle. A learner who has done Composite arrives already knowing this
 * shape and can spend the whole project on the traversal instead.
 *
 * <p>Built twice, identically, so that the naive comparison in
 * {@link CatalogReportDemo} is a comparison of designs and not of data.
 */
public final class Catalog {

    private Catalog() {
    }

    /** The tree, as {@link CatalogComponent} nodes. */
    public static Category demoTree() {
        Category cables = new Category("Cables")
                .add(new Product("CBL-001", "USB-C Cable", Money.pounds(9.99), 420));

        Product battery = new Product("BAT-014", "Spare Battery Pack",
                Money.pounds(34.99), 62, Restriction.LITHIUM_BATTERY);
        Product cleaner = new Product("CLN-003", "Screen Cleaner, 200ml",
                Money.pounds(6.50), 190, Restriction.FLAMMABLE);
        Product phoneCase = new Product("CSE-100", "Case", Money.pounds(19.99), 310);
        Product phone = new Product("PHN-900", "Phone", Money.pounds(599.99), 74);

        Category accessories = new Category("Accessories")
                .add(phoneCase)
                .add(new Product("CHG-220", "Charger", Money.pounds(29.99), 148))
                .add(battery)
                .add(cleaner)
                .add(cables);

        // The kit holds the same three products the catalog already lists.
        // They are visited once, as nodes, and never again as contents --
        // Bundle.accept does not walk into the box, so the value report
        // cannot count the phone twice.
        Category kits = new Category("Kits")
                .add(new Bundle("KIT-01", "Starter Kit, 3 items", Money.pounds(639.00), 25)
                        .containing(phone)
                        .containing(phoneCase)
                        .containing(battery));

        return new Category("Electronics")
                .add(phone)
                .add(accessories)
                .add(kits)
                .add(new Category("Clearance"));
    }

    /** The same tree again, as the naive nodes that carry their own reports. */
    public static NaiveCategory naiveDemoTree() {
        NaiveCategory cables = new NaiveCategory("Cables")
                .add(new NaiveProduct("CBL-001", "USB-C Cable", Money.pounds(9.99), 420));

        NaiveCategory accessories = new NaiveCategory("Accessories")
                .add(new NaiveProduct("CSE-100", "Case", Money.pounds(19.99), 310))
                .add(new NaiveProduct("CHG-220", "Charger", Money.pounds(29.99), 148))
                .add(new NaiveProduct("BAT-014", "Spare Battery Pack",
                        Money.pounds(34.99), 62, Restriction.LITHIUM_BATTERY))
                .add(new NaiveProduct("CLN-003", "Screen Cleaner, 200ml",
                        Money.pounds(6.50), 190, Restriction.FLAMMABLE))
                .add(cables);

        NaiveCategory kits = new NaiveCategory("Kits")
                .add(new NaiveBundle("KIT-01", "Starter Kit, 3 items", Money.pounds(639.00), 25)
                        .containing(new NaiveProduct("PHN-900", "Phone",
                                Money.pounds(599.99), 74))
                        .containing(new NaiveProduct("CSE-100", "Case",
                                Money.pounds(19.99), 310))
                        .containing(new NaiveProduct("BAT-014", "Spare Battery Pack",
                                Money.pounds(34.99), 62, Restriction.LITHIUM_BATTERY)));

        return new NaiveCategory("Electronics")
                .add(new NaiveProduct("PHN-900", "Phone", Money.pounds(599.99), 74))
                .add(accessories)
                .add(kits)
                .add(new NaiveCategory("Clearance"));
    }
}
