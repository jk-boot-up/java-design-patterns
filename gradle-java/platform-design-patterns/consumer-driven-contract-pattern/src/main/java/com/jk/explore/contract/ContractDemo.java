package com.jk.explore.contract;

import java.util.List;

public class ContractDemo {

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. Nobody told the consumer.");
        long total = new Checkout().total(PriceProvider.renamed(), "MUG", 2);
        System.out.println("  the catalog renamed priceCents to price and released. checkout, 2 mugs: total " + total + ", meaning the order failed.");
        System.out.println("  it was found in production, by a customer.");
    }

    private static void two() {
        System.out.println("TWO. The consumer writes down what it needs.");
        System.out.println("  checkout's contract: " + new java.util.TreeMap<>(Checkout.CONTRACT.expects()) + ".");
        System.out.println("  reports' contract: " + Reports.CONTRACT.expects() + ".");
        System.out.println("  each lists only the fields it reads, and their types.");
    }

    private static void three() {
        System.out.println("THREE. The provider checks itself.");
        List<String> problems = Verifier.verify(PriceProvider.v1(), "MUG", Checkout.CONTRACT, Reports.CONTRACT);
        System.out.println("  the catalog's real answer against both contracts. problems: " + problems + ". safe to release.");
    }

    private static void four() {
        System.out.println("FOUR. The rename is caught before release.");
        List<String> problems = Verifier.verify(PriceProvider.renamed(), "MUG", Checkout.CONTRACT, Reports.CONTRACT);
        System.out.println("  problems: " + problems + ".");
        System.out.println("  the build fails, and it names the consumer and the field.");
    }

    private static void five() {
        System.out.println("FIVE. Adding is safe, and only the affected are named.");
        System.out.println("  a release that adds a stock field. problems: " + Verifier.verify(PriceProvider.extraField(), "MUG", Checkout.CONTRACT, Reports.CONTRACT) + ".");
        System.out.println("  the rename again, per consumer: checkout " + Verifier.verify(PriceProvider.renamed(), "MUG", Checkout.CONTRACT).size()
                + " problem, reports " + Verifier.verify(PriceProvider.renamed(), "MUG", Reports.CONTRACT).size() + " problems. reports never used that field.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        List<String> problems = Verifier.verify(PriceProvider.pounds(), "MUG", Checkout.CONTRACT, Reports.CONTRACT);
        System.out.println("  a release that now sends pounds, not pence, in the same field. problems: " + problems + ". it passes.");
        System.out.println("  checkout, 2 mugs: total " + new Checkout().total(PriceProvider.pounds(), "MUG", 2) + ", where it should be 3200.");
        System.out.println("  a contract checks the shape, and not the meaning. and every consumer must keep its contract up to date, or the check protects nobody.");
    }
}
