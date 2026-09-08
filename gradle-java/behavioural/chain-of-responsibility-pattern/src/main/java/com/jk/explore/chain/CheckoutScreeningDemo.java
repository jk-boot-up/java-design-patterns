package com.jk.explore.chain;

import java.util.List;
import java.util.Map;

/**
 * Runs the naive screening and the chain over the same four orders, so the
 * difference is something you can read rather than something you have to
 * believe.
 */
public final class CheckoutScreeningDemo {

    /** What the warehouse has on the shelf. */
    private static final Map<String, Integer> ON_SHELF =
            Map.of("MON-27", 5, "KEY-01", 20, "DESK-02", 2);

    /** Over the card limit, and scoring 92 with the risk model. Both are true. */
    private static final CheckoutRequest MONITOR = new CheckoutRequest(
            "R2001", List.of(new BasketItem("MON-27", "27-inch monitor", 329, 1)),
            "GB", "SW1A 1AA", 250, 92);

    /** Jersey. No courier we use covers it. */
    private static final CheckoutRequest JERSEY = new CheckoutRequest(
            "R2002", List.of(new BasketItem("KEY-01", "Mechanical keyboard", 45, 1)),
            "GB", "JE3 8QX", 2000, 10);

    /** Scoring 64 — the band the risk model exists to flag. */
    private static final CheckoutRequest GREY_BAND = new CheckoutRequest(
            "R2003", List.of(new BasketItem("KEY-01", "Mechanical keyboard", 45, 2)),
            "GB", "M1 4BT", 2000, 64);

    /** A trade account: invoiced monthly, so no card is checked. Also Jersey. */
    private static final CheckoutRequest TRADE = new CheckoutRequest(
            "R2004", List.of(new BasketItem("DESK-02", "Standing desk", 180, 2)),
            "GB", "JE2 3AB", 0, 20);

    public static void main(String[] args) {
        naive();
        chain();
        reordered();
        tradeChain();
        System.out.println();
        System.out.println("And the honest note: if your checks and their order never change,");
        System.out.println("write the four ifs. This pattern earns its keep when the order is");
        System.out.println("something you need to change without editing any of the checks.");
    }

    private static void naive() {
        heading("1.  The naive method — four checks in one method");
        NaiveScreening naive = new NaiveScreening(ON_SHELF);

        System.out.println(MONITOR);
        System.out.println("   -> " + naive.validate(MONITOR));
        System.out.println("      Both things are true. It reports the card, because the card is");
        System.out.println("      checked first. The customer tries another card and it works.");
        System.out.println();

        System.out.println(GREY_BAND);
        System.out.println("   -> " + naive.validate(GREY_BAND));
        System.out.println("      A score of 64 is the case a person should look at. The return");
        System.out.println("      type is a boolean, so there is nowhere to put that answer.");
        System.out.println();

        System.out.println(TRADE);
        System.out.println("   -> " + naive.validateTradeAccount(TRADE));
        System.out.println("      The trade method is a copy with the card check removed on");
        System.out.println("      purpose — and the address check removed by accident.");
        System.out.println("      Two desks are on their way to Jersey.");
    }

    private static void chain() {
        heading("2.  The same checks, as a chain");
        ScreeningChain standard = standardChain();
        System.out.println(standard);
        System.out.println();

        for (CheckoutRequest request : List.of(MONITOR, JERSEY, GREY_BAND)) {
            System.out.println(request);
            System.out.println("   -> " + standard.screen(request));
            System.out.println();
        }
        System.out.println("   Read the \"never ran\" lines. Those are not checks that were");
        System.out.println("   ignored — they are checks that never executed. No warehouse");
        System.out.println("   query, no risk model call, nothing billed for.");
    }

    private static void reordered() {
        heading("3.  Same links, one different order");
        ScreeningChain paymentFirst = new ScreeningChain("payment-before-fraud",
                Decision.approved("end of chain", "no link objected"),
                new AddressCheck(), new StockCheck(ON_SHELF),
                new PaymentLimitCheck(), new FraudScoreCheck());
        System.out.println(paymentFirst);
        System.out.println();
        System.out.println(MONITOR);
        System.out.println("   -> " + paymentFirst.screen(MONITOR));
        System.out.println();
        System.out.println("   That is the naive answer again, reproduced exactly — and the only");
        System.out.println("   thing that changed is the order of two arguments. The naive");
        System.out.println("   behaviour was never wrong. It was a setting you could not change");
        System.out.println("   without editing the checks.");
    }

    private static void tradeChain() {
        heading("4.  A different policy, by wiring only");
        ScreeningChain trade = new ScreeningChain("trade-account",
                Decision.approved("end of chain", "no link objected"),
                new AddressCheck(), new StockCheck(ON_SHELF), new FraudScoreCheck());
        System.out.println(trade);
        System.out.println();
        System.out.println(TRADE);
        System.out.println("   -> " + trade.screen(TRADE));
        System.out.println();
        System.out.println("   The card check is left out because trade accounts are invoiced.");
        System.out.println("   Nothing was copied, so nothing could drift, so the address check");
        System.out.println("   is still there — and Jersey is caught.");
    }

    /** Address, stock, fraud, payment — the order the business actually wants. */
    private static ScreeningChain standardChain() {
        return new ScreeningChain("standard",
                Decision.approved("end of chain", "no link objected"),
                new AddressCheck(), new StockCheck(ON_SHELF),
                new FraudScoreCheck(), new PaymentLimitCheck());
    }

    private static void heading(String title) {
        System.out.println();
        System.out.println("=".repeat(72));
        System.out.println(title);
        System.out.println("=".repeat(72));
    }

    private CheckoutScreeningDemo() {
    }
}
