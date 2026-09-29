package com.jk.explore.money;

import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.List;

/**
 * The six acts: doubles, then Money, currencies, rounding, splitting, and the bill.
 */
public final class MoneyDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. Prices as doubles.");
        NaiveCart naive = new NaiveCart();
        naive.add(0.10, 1);
        naive.add(0.20, 1);
        out.add("  a 10p sticker and a 20p sticker: total " + naive.total());
        out.add("  is it 0.30? " + (naive.total() == 0.30));
        double tenPence = 0;
        for (int i = 0; i < 1000; i++) {
            tenPence += 0.10;
        }
        out.add("  1000 items at 10p, added one by one: " + tenPence);
        out.add("  turned into pence by cutting off the fraction: "
                + NaiveCart.toPenceByTruncating(tenPence) + " pence, not 10000");
        out.add("  and 10 dollars + 10 pounds = " + (10.0 + 10.0) + ", with nobody asking which is which");

        out.add("");
        out.add("TWO. Prices as Money.");
        Money sticker = Money.of("0.10", Currency.GBP).plus(Money.of("0.20", Currency.GBP));
        out.add("  10p + 20p = " + sticker + ", equal to 30p: " + sticker.equals(Money.of("0.30", Currency.GBP)));
        Money sum = Money.zero(Currency.GBP);
        for (int i = 0; i < 1000; i++) {
            sum = sum.plus(Money.of("0.10", Currency.GBP));
        }
        out.add("  1000 items at 10p: " + sum + ", stored as " + sum.minor() + " pence");
        Cart cart = new Cart(Currency.GBP)
                .add("mug", Money.of("9.49", Currency.GBP), 3)
                .add("teapot", Money.of("24.99", Currency.GBP), 1)
                .add("coasters", Money.of("4.99", Currency.GBP), 2);
        out.add("  a cart of 3 mugs at £9.49, a teapot at £24.99, 2 coasters at £4.99: " + cart.total());

        out.add("");
        out.add("THREE. Currencies travel with the amount.");
        try {
            Money.of("10.00", Currency.GBP).plus(Money.of("10.00", Currency.USD));
            out.add("  £10 + $10 was allowed");
        } catch (IllegalArgumentException e) {
            out.add("  £10.00 + $10.00: refused, " + e.getMessage());
        }
        out.add("  a Japanese price has no pennies: " + Money.of("1500", Currency.JPY));
        try {
            Money.of("9.999", Currency.GBP);
            out.add("  £9.999 was accepted");
        } catch (IllegalArgumentException e) {
            out.add("  £9.999: refused, " + e.getMessage());
        }

        out.add("");
        out.add("FOUR. Rounding is a choice, made once.");
        Money price = Money.of("0.99", Currency.GBP);
        Money vatEachLine = Money.zero(Currency.GBP);
        for (int i = 0; i < 10; i++) {
            vatEachLine = vatEachLine.plus(price.times("0.20", RoundingMode.HALF_UP));
        }
        Money vatOnTotal = price.times(10).times("0.20", RoundingMode.HALF_UP);
        out.add("  VAT at 20% on 10 items at 99p, rounded on each line: " + vatEachLine);
        out.add("  the same VAT, rounded once on the total:            " + vatOnTotal);
        out.add("  difference: " + vatEachLine.minus(vatOnTotal) + ", and Money made the rounding visible");

        out.add("");
        out.add("FIVE. Splitting without losing a penny.");
        Money tenPounds = Money.of("10.00", Currency.GBP);
        Money third = Money.ofMinor(tenPounds.minor() / 3, Currency.GBP);
        out.add("  £10 shared by 3 friends, each paying a third: " + third
                + " x 3 = " + third.times(3) + ", a penny short");
        Money[] shares = tenPounds.allocate(1, 1, 1);
        out.add("  allocate(1, 1, 1): " + shares[0] + ", " + shares[1] + ", " + shares[2]
                + " = " + shares[0].plus(shares[1]).plus(shares[2]));
        Money[] discount = cart.discountShares(Money.of("5.00", Currency.GBP));
        out.add("  a £5.00 basket discount spread over the cart's lines by value: "
                + discount[0] + ", " + discount[1] + ", " + discount[2]
                + " = " + discount[0].plus(discount[1]).plus(discount[2]));

        out.add("");
        out.add("SIX. The bill.");
        out.add("  a price is now a class, not a number: every place that stores,");
        out.add("  sends or shows one must convert, e.g. " + Money.of("19.99", Currency.GBP)
                + " is stored as " + Money.of("19.99", Currency.GBP).minor() + " and GBP");
        out.add("  converting pounds to dollars needs a rate and a date: Money does not do it");
        return out;
    }

    private MoneyDemo() {
    }
}
