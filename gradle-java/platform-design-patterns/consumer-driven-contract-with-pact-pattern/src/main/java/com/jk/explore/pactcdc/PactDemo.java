package com.jk.explore.pactcdc;

public class PactDemo {

    public static void main(String[] args) throws Exception {
        System.setProperty("pact_do_not_track", "true");
        one();
        two();
        three();
        four();
        five();
        six();
    }

    static long checkoutTotal(Release release) throws Exception {
        try (Catalog catalog = new Catalog(release)) {
            return new CheckoutClient("http://127.0.0.1:" + catalog.port()).total("MUG", 2);
        }
    }

    private static void one() throws Exception {
        System.out.println("ONE. Nobody told the consumer.");
        System.out.println("  the catalog renamed priceCents to price and released. checkout, 2 mugs: total " + checkoutTotal(Release.RENAMED) + ", meaning the order failed.");
        System.out.println("  it was found in production, by a customer.");
    }

    private static void two() throws Exception {
        System.out.println("TWO. The consumer writes a pact.");
        boolean ok = Pacts.writeBoth();
        System.out.println("  each consumer's own client was run against Pact's mock of the catalog, and agreed: " + ok + ". two pact files were written.");
        System.out.println("  checkout's pact: " + Pacts.expectations("checkout") + ".");
        System.out.println("  reports' pact: " + Pacts.expectations("reports") + ".");
    }

    private static void three() throws Exception {
        System.out.println("THREE. The provider replays the pacts.");
        Verifier.Outcome o = Verifier.verify(Release.V1);
        System.out.println("  Pact replays each pact against the real catalog over HTTP. interactions checked: " + o.checked() + ", problems: " + o.problems() + ". safe to release.");
    }

    private static void four() throws Exception {
        System.out.println("FOUR. The rename is caught before release.");
        Verifier.Outcome o = Verifier.verify(Release.RENAMED);
        System.out.println("  interactions checked: " + o.checked() + ", failed: " + o.problems().size() + ".");
        o.problems().forEach(p -> System.out.println("  " + p));
        System.out.println("  the build fails, and Pact names the consumer and the field. reports' pact still passes.");
    }

    private static void five() throws Exception {
        System.out.println("FIVE. Adding is safe.");
        Verifier.Outcome o = Verifier.verify(Release.EXTRA_FIELD);
        System.out.println("  a release that adds a stock field. interactions checked: " + o.checked() + ", problems: " + o.problems() + ".");
    }

    private static void six() throws Exception {
        System.out.println("SIX. The bill.");
        Verifier.Outcome o = Verifier.verify(Release.POUNDS);
        System.out.println("  a release that now sends pounds, not pence, in the same field. problems: " + o.problems() + ". it passes.");
        System.out.println("  checkout, 2 mugs: total " + checkoutTotal(Release.POUNDS) + ", where it should be 3200.");
        System.out.println("  a pact checks the shape, and not the meaning. and every consumer must keep its pact up to date, or the check protects nobody.");
    }
}
