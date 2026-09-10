package com.jk.explore.interpreter;

import java.util.ArrayList;
import java.util.List;

/** Runs the same three orders through the hard-coded rules and the language. */
public class VoucherRuleDemo {

    /** The promotions, exactly as marketing would write them. */
    private static final List<String> PROMOTIONS = List.of(
            "SAVE10   | 10 | country is UK and basket over 50",
            "SAVE15   | 15 | country is UK and basket over 100",
            "FREESHIP |  5 | country is UK and items at least 3");

    private static final List<Order> ORDERS = List.of(
            new Order(120, "UK", 4, false),
            new Order(120, "US", 2, false),
            new Order(30, "UK", 3, false));

    public static void main(String[] args) {
        NaiveVoucherRules naive = new NaiveVoucherRules();
        PromotionBook book = PromotionBook.fromLines(PROMOTIONS);

        System.out.println("=== the rules, as the shop wrote them ===");
        for (Promotion promotion : book.promotions()) {
            // Printed from the tree, not from the line that was read in. If the
            // two ever disagreed, the tree is what the checkout obeys.
            System.out.println("  " + promotion.explain());
        }

        System.out.println();
        System.out.println("=== rules written as Java branches ===");
        for (Order order : ORDERS) {
            System.out.println("  " + order);
            System.out.println("      discount: " + naive.bestPercentFor(order) + "%");
        }
        System.out.println("  the second order is overseas and gets 15% anyway,");
        System.out.println("  and the third one qualifies but is offered nothing.");
        System.out.println("  No exception was thrown for either.");

        System.out.println();
        System.out.println("=== the same rules, read as a language ===");
        for (Order order : ORDERS) {
            System.out.println("  " + order);
            System.out.println("      discount: " + book.bestPercentFor(order) + "%");
            for (String reason : book.reasonsFor(order)) {
                System.out.println("      because " + reason);
            }
        }

        System.out.println();
        System.out.println("=== marketing wants one more, and it is Friday ===");
        List<String> withNewOffer = new ArrayList<>(PROMOTIONS);
        withNewOffer.add("BIGBASKET | 20 | basket over 200 or items at least 10");
        PromotionBook friday = PromotionBook.fromLines(withNewOffer);
        Order bulk = new Order(90, "UK", 12, false);
        System.out.println("  added: " + withNewOffer.get(withNewOffer.size() - 1).trim());
        System.out.println("  " + bulk);
        System.out.println("      discount: " + friday.bestPercentFor(bulk) + "%");
        System.out.println("  One line of text. No new class, and nothing recompiled.");

        System.out.println();
        System.out.println("=== and a rule with a typo in it ===");
        try {
            RuleParser.parse("country is UK and basket ovr 50");
        } catch (IllegalArgumentException e) {
            System.out.println("  refused: " + e.getMessage());
            System.out.println("  on Wednesday, when it is cheap — not at checkout on Friday.");
        }
    }
}
