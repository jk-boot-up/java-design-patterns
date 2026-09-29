package com.jk.explore.microfrontends;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: one front-end for everything, a page assembled from team fragments, a failing fragment, an independent release, and the bill.
 */
public final class MicroFrontendsDemo {

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();

        out.add("ONE. One front-end renders the whole product page.");
        OneFrontEnd one = new OneFrontEnd();
        out.add("  " + one.productPage("KETTLE-1"));
        one.breakRecommendations();
        try {
            one.productPage("KETTLE-1");
        } catch (IllegalStateException e) {
            out.add("  a bug in the recommendations section: the whole page fails (" + e.getMessage() + ")");
        }
        out.add("  and fixing it means releasing the whole front-end, every team's code together");

        try (TeamApp product = new TeamApp("product team", () -> "steel kettle, £30.00");
             TeamApp basket = new TeamApp("basket team", () -> "2 items, £38.00");
             TeamApp recs = new TeamApp("recommendations team", () -> "mug, teapot")) {

            PageAssembler page = new PageAssembler()
                    .slot("product", product.url()).slot("basket", basket.url()).slot("recommendations", recs.url());

            out.add("");
            out.add("TWO. Micro-frontends: each team serves its own part of the page.");
            out.add("  " + page.render());
            out.add("  three team apps, each on its own server; the page is a layout with three slots");

            out.add("");
            out.add("THREE. One team's failure stays in its slot.");
            recs.release(() -> {
                throw new IllegalStateException("index out of range");
            });
            out.add("  " + page.render());
            recs.release(() -> "mug, teapot");
            recs.slowDown(1000);
            out.add("  and when it is slow: " + page.render());
            recs.slowDown(0);

            out.add("");
            out.add("FOUR. Each team releases on its own.");
            basket.release(() -> "2 items, £38.00, free delivery over £40");
            out.add("  " + page.render());
            out.add("  the basket team released version 2; the product and recommendations apps were not touched");

            out.add("");
            out.add("FIVE. The bill: more requests, and teams drift apart.");
            PageAssembler count = new PageAssembler()
                    .slot("product", product.url()).slot("basket", basket.url()).slot("recommendations", recs.url());
            count.render();
            out.add("  one page view: 1 page + " + count.requests() + " fragment requests");
            product.release(() -> "steel kettle, 30.00 GBP");
            out.add("  " + count.render());
            out.add("  one team now writes \"30.00 GBP\", another \"£38.00\": the page looks like two shops");
        }
        return out;
    }

    private MicroFrontendsDemo() {
    }
}
