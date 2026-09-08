package com.jk.explore.builder;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;

/**
 * An order placed by a customer: some required facts, and a handful of
 * options that most orders never use.
 *
 * <p>This is the telescoping-constructor problem, in the flesh. Every order
 * needs a customer, at least one item and a shipping address. Some orders
 * are gift-wrapped, with a message. Some are marked priority. Some carry a
 * coupon. Some have a note for the warehouse. None of that combination is
 * fixed, and a constructor that tried to cover it would need a boolean and
 * a nullable string for every option, in a fixed order the caller would
 * have to memorise.
 *
 * <p>The type is immutable once built — every field is final, and
 * {@link #items()} returns a copy — so a {@link Builder} that keeps being
 * reused after {@link Builder#build()} cannot reach back in and change an
 * order that has already shipped.
 */
public final class PurchaseOrder {

    private final String orderId;
    private final String customerId;
    private final List<LineItem> items;
    private final Address shippingAddress;
    private final boolean giftWrapped;
    private final String giftMessage;
    private final String couponCode;
    private final boolean priority;
    private final String notes;

    private PurchaseOrder(Builder builder) {
        this.orderId = builder.orderId;
        this.customerId = builder.customerId;
        this.items = List.copyOf(builder.items);
        this.shippingAddress = builder.shippingAddress;
        this.giftWrapped = builder.giftWrapped;
        this.giftMessage = builder.giftMessage;
        this.couponCode = builder.couponCode;
        this.priority = builder.priority;
        this.notes = builder.notes;
    }

    /** A static factory that hands back the builder — the two patterns compose. */
    public static Builder builder(String orderId, String customerId) {
        return new Builder(orderId, customerId);
    }

    public String orderId() {
        return orderId;
    }

    public String customerId() {
        return customerId;
    }

    public List<LineItem> items() {
        return items;
    }

    public Address shippingAddress() {
        return shippingAddress;
    }

    public boolean isGiftWrapped() {
        return giftWrapped;
    }

    public Optional<String> giftMessage() {
        return Optional.ofNullable(giftMessage);
    }

    public Optional<String> couponCode() {
        return Optional.ofNullable(couponCode);
    }

    public boolean isPriority() {
        return priority;
    }

    public Optional<String> notes() {
        return Optional.ofNullable(notes);
    }

    public Money subtotal() {
        Money sum = Money.zero();
        for (LineItem item : items) {
            sum = sum.plus(item.total());
        }
        return sum;
    }

    /** Gift wrap and priority shipping each add a flat fee; a coupon knocks 10% off. */
    public Money total() {
        Money total = subtotal();
        if (giftWrapped) {
            total = total.plus(Money.pounds(2.50));
        }
        if (priority) {
            total = total.plus(Money.pounds(6.00));
        }
        if (couponCode != null) {
            total = Money.pence(Math.round(total.asPence() * 0.9));
        }
        return total;
    }

    @Override
    public String toString() {
        return "PurchaseOrder{" + orderId
                + ", customer=" + customerId
                + ", items=" + items.size()
                + ", giftWrapped=" + giftWrapped
                + ", priority=" + priority
                + ", coupon=" + (couponCode == null ? "none" : couponCode)
                + ", total=" + total()
                + "}";
    }

    /**
     * Builds a {@link PurchaseOrder} one piece at a time.
     *
     * <p>The two required facts besides the order and customer id — at
     * least one item, and a shipping address — are checked in
     * {@link #build()}, not before, because the builder's whole job is to
     * be filled in gradually and in any order. Every method returns
     * {@code this}, which is what makes the calls chain.
     */
    public static final class Builder {

        private final String orderId;
        private final String customerId;
        private final List<LineItem> items = new ArrayList<>();
        private Address shippingAddress;
        private boolean giftWrapped;
        private String giftMessage;
        private String couponCode;
        private boolean priority;
        private String notes;

        private Builder(String orderId, String customerId) {
            this.orderId = Objects.requireNonNull(orderId, "orderId");
            this.customerId = Objects.requireNonNull(customerId, "customerId");
        }

        public Builder addItem(LineItem item) {
            items.add(Objects.requireNonNull(item, "item"));
            return this;
        }

        public Builder shippingAddress(Address address) {
            this.shippingAddress = Objects.requireNonNull(address, "shippingAddress");
            return this;
        }

        /** Wrapping with no message. See {@link #giftMessage(String)} for the common case. */
        public Builder giftWrap() {
            this.giftWrapped = true;
            return this;
        }

        /**
         * A gift message implies wrapping — nobody writes a card for a box that
         * is not wrapped — so this sets both. That rule lives here exactly
         * once, instead of in every caller that wants a gift message.
         */
        public Builder giftMessage(String message) {
            this.giftMessage = Objects.requireNonNull(message, "giftMessage");
            this.giftWrapped = true;
            return this;
        }

        public Builder couponCode(String code) {
            this.couponCode = Objects.requireNonNull(code, "couponCode");
            return this;
        }

        public Builder priority() {
            this.priority = true;
            return this;
        }

        public Builder notes(String notes) {
            this.notes = Objects.requireNonNull(notes, "notes");
            return this;
        }

        /**
         * Validates and assembles the order. Safe to call more than once —
         * each call reads the builder's current state and produces an
         * independent, immutable {@link PurchaseOrder} — but a builder is
         * normally used once and discarded.
         */
        public PurchaseOrder build() {
            if (items.isEmpty()) {
                throw new IllegalStateException("a purchase order needs at least one item");
            }
            if (shippingAddress == null) {
                throw new IllegalStateException("a purchase order needs a shipping address");
            }
            return new PurchaseOrder(this);
        }
    }
}
