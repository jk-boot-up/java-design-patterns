package com.jk.explore.state;

import java.util.ArrayList;
import java.util.List;

/**
 * The money actually moved for one order.
 *
 * <p>It exists so that a wrong transition has a visible price. A double
 * refund is not an exception or a log line; it is a second entry here, and a
 * {@link #net()} that says the shop paid the customer more than the customer
 * ever paid the shop.
 */
public final class Ledger {

    /** One movement of money. Positive amounts are taken, negative are given back. */
    public record Entry(String kind, Money amount) {
        @Override
        public String toString() {
            return String.format("%-8s %9s", kind, amount);
        }
    }

    private final List<Entry> entries = new ArrayList<>();

    void charge(Money amount) {
        entries.add(new Entry("charge", amount));
    }

    void refund(Money amount) {
        entries.add(new Entry("refund", amount));
    }

    public List<Entry> entries() {
        return List.copyOf(entries);
    }

    public Money charged() {
        return total("charge");
    }

    public Money refunded() {
        return total("refund");
    }

    /** What the shop is left holding. Negative means it paid out more than it took. */
    public Money net() {
        return charged().minus(refunded());
    }

    public int refundCount() {
        return (int) entries.stream().filter(e -> e.kind().equals("refund")).count();
    }

    private Money total(String kind) {
        return entries.stream()
                .filter(e -> e.kind().equals(kind))
                .map(Entry::amount)
                .reduce(Money.zero(), Money::plus);
    }

    @Override
    public String toString() {
        return entries.isEmpty() ? "(no money moved)" : String.join("; ",
                entries.stream().map(Entry::toString).map(String::trim).toList());
    }
}
