package com.jk.explore.valueobject;

import com.jk.explore.valueobject.domain.CurrencyMismatch;
import com.jk.explore.valueobject.domain.EmailAddress;
import com.jk.explore.valueobject.domain.Money;
import com.jk.explore.valueobject.naive.BareEmailSignup;
import com.jk.explore.valueobject.naive.IdentityMoney;
import com.jk.explore.valueobject.naive.MutableMoney;
import com.jk.explore.valueobject.naive.NaivePricing;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class ValueObjectDemo {

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. Money as a double.");
        System.out.println("  three stamps at 1.10: " + NaivePricing.total(1.10, 3) + ".");
        System.out.println("  0.1 + 0.2 == 0.3: " + (0.1 + 0.2 == 0.3) + ".");
        System.out.println("  ten pounds added to ten dollars: " + NaivePricing.add(10, "GBP", 10, "USD") + ".");
        System.out.println("  the number has no idea what it is a number of.");
    }

    private static void two() {
        System.out.println("TWO. Money as a value.");
        Money stamps = Money.gbp(110).times(3);
        System.out.println("  three stamps at " + Money.gbp(110) + ": " + stamps + ".");
        try {
            Money.gbp(1000).plus(Money.usd(1000));
        } catch (CurrencyMismatch e) {
            System.out.println("  ten pounds plus ten dollars: refused, " + e.getMessage() + ".");
        }
        System.out.println("  the amount and its currency travel together.");
    }

    private static void three() {
        System.out.println("THREE. Equal by value.");
        Set<Money> money = new HashSet<>(List.of(Money.gbp(500), Money.gbp(500), Money.gbp(500)));
        System.out.println("  three separate objects of 5.00, in a set: " + money.size() + ".");
        Set<IdentityMoney> identity = new HashSet<>(List.of(new IdentityMoney(500), new IdentityMoney(500), new IdentityMoney(500)));
        System.out.println("  the same with a class that compares by identity: " + identity.size() + ".");
        System.out.println("  " + Money.gbp(500).equals(Money.gbp(500)) + " for two 5.00s, and " + Money.gbp(500).equals(Money.usd(500)) + " for 5.00 and 5.00 dollars.");
    }

    private static void four() {
        System.out.println("FOUR. Never changed.");
        MutableMoney shared = new MutableMoney(2000);
        long orderAsPrice = shared.pence();
        MutableMoney orderBsPrice = shared;
        orderBsPrice.subtract(500);
        System.out.println("  a mutable price shared by two orders. order B takes 5.00 off. order A now costs: " + shared.pence() + " pence, not " + orderAsPrice + ".");
        Money price = Money.gbp(2000);
        Money discounted = price.minus(Money.gbp(500));
        System.out.println("  the same with values: order B pays " + discounted + ", order A still pays " + price + ".");
    }

    private static void five() {
        System.out.println("FIVE. Valid from the moment it exists.");
        BareEmailSignup signup = new BareEmailSignup();
        signup.signUp("ada@example.com");
        signup.importFromPartner("not an email");
        System.out.println("  strings: two methods checked, the third did not. stored: " + signup.stored() + ".");
        try {
            EmailAddress.of("not an email");
        } catch (IllegalArgumentException e) {
            System.out.println("  an EmailAddress: " + e.getMessage() + ". it cannot be built wrong.");
        }
        System.out.println("  a method that receives an EmailAddress never checks. " + EmailAddress.of("  Ada@Example.COM ").value() + ".");
    }

    private static void six() {
        System.out.println("SIX. Splitting is a decision.");
        double[] shares = NaivePricing.splitThreeWays(10.00);
        System.out.println("  ten pounds three ways, rounded: " + shares[0] + " + " + shares[1] + " + " + shares[2] + " = " + Math.round((shares[0] + shares[1] + shares[2]) * 100) / 100.0 + ". a penny vanished.");
        List<Money> allocated = Money.gbp(1000).allocate(3);
        System.out.println("  allocated: " + allocated + ", adding up to " + allocated.stream().reduce(Money.gbp(0), Money::plus) + ".");
        System.out.println("  the type has to say who gets the odd penny. that is a rule, and it lives in one place.");
    }
}
