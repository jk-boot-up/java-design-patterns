package com.jk.explore.iterator;

import java.util.Iterator;

/**
 * Runs the whole example. {@code ./gradlew run}
 *
 * <p>Four sections, each making one point. Read the output next to this file
 * and the pattern should need very little explaining.
 */
public class CatalogueDemo {

    public static void main(String[] args) {
        section("1. The naive way: every caller writes the page loop");
        naiveBrowsing();

        section("2. The pattern: the catalogue is just a thing you loop over");
        forEachBrowsing();

        section("3. Pages are fetched only when you reach them");
        laziness();

        section("4. Two walks at once do not interfere");
        twoWalksAtOnce();
    }

    private static void naiveBrowsing() {
        NaiveCatalogueBrowser browser = new NaiveCatalogueBrowser(CatalogueFeed.sampleShop());

        System.out.println("allProducts()  -> " + browser.allProducts().size() + " products (correct)");
        System.out.println("countProducts()-> " + browser.countProducts()
                + " products (WRONG: the loop stops after 3 pages)");
        System.out.println("findCheapest() -> " + browser.findCheapest());
        System.out.println("                 (WRONG: it starts at page 1, so the £4 socks are invisible)");
        System.out.println();
        System.out.println("Three methods, three copies of the page loop, two of them broken.");
        System.out.println("Nothing threw. The shop just quietly shows the wrong thing.");
    }

    private static void forEachBrowsing() {
        ProductCatalogue catalogue = new ProductCatalogue(CatalogueFeed.sampleShop());

        int count = 0;
        Product cheapest = null;
        for (Product product : catalogue) {
            count++;
            if (cheapest == null || product.priceInPounds() < cheapest.priceInPounds()) {
                cheapest = product;
            }
        }

        System.out.println("for (Product p : catalogue) { ... }");
        System.out.println();
        System.out.println("counted        -> " + count + " products (correct)");
        System.out.println("cheapest       -> " + cheapest + " (correct)");
        System.out.println();
        System.out.println("No page numbers anywhere in that loop. There is nothing to get wrong,");
        System.out.println("because the only page loop in the project lives in CatalogueIterator.");
    }

    private static void laziness() {
        CatalogueFeed feed = CatalogueFeed.sampleShop();
        ProductCatalogue catalogue = new ProductCatalogue(feed);

        System.out.println("The feed hands out " + CatalogueFeed.PAGE_SIZE + " products per page, "
                + feed.totalProducts() + " products in total.");
        System.out.println();
        System.out.println("Showing the first 2 products, then stopping:");
        int shown = 0;
        for (Product product : catalogue) {
            System.out.println("  " + product);
            if (++shown == 2) {
                break;
            }
        }
        System.out.println();
        System.out.println("pages fetched  -> " + feed.pagesFetched() + " of 3");
        System.out.println("The customer looked at the first two products, so the warehouse was");
        System.out.println("asked for one page. The rest of the catalogue was never requested.");
    }

    private static void twoWalksAtOnce() {
        ProductCatalogue catalogue = new ProductCatalogue(CatalogueFeed.sampleShop());

        Iterator<Product> outer = catalogue.iterator();
        Iterator<Product> inner = catalogue.iterator();

        System.out.println("Two iterators from the same catalogue:");
        System.out.println("  outer.next() -> " + outer.next().name());
        System.out.println("  outer.next() -> " + outer.next().name());
        System.out.println("  inner.next() -> " + inner.next().name() + "   <- still at the start");
        System.out.println("  outer.next() -> " + outer.next().name());
        System.out.println();
        System.out.println("Each iterator keeps its own position, so they cannot disturb each");
        System.out.println("other. That is why a loop inside a loop over the same catalogue works.");
    }

    private static void section(String title) {
        System.out.println();
        System.out.println("=".repeat(72));
        System.out.println(title);
        System.out.println("=".repeat(72));
    }
}
