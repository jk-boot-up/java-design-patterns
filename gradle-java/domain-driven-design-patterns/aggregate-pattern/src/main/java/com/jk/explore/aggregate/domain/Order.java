package com.jk.explore.aggregate.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * The aggregate root. An order and its lines are one thing, changed as one thing, and this class is the
 * only door. Every rule that spans the lines lives here, so no caller can break one:
 * <ul>
 *   <li>a line has between 1 and 10 of an item, and an item appears on one line only;</li>
 *   <li>the order total may not pass the credit limit of one thousand pounds;</li>
 *   <li>an order that is placed can no longer change;</li>
 *   <li>an order cannot be placed empty.</li>
 * </ul>
 * It refers to its customer by id, not by object, because the customer is a different aggregate.
 */
public final class Order {

    public static final int MAX_PER_LINE = 10;
    public static final Money CREDIT_LIMIT = Money.pounds(1000);

    private final OrderId id;
    private final CustomerId customer;
    private final List<OrderLine> lines = new ArrayList<>();
    private boolean placed;

    public Order(OrderId id, CustomerId customer) {
        this.id = id;
        this.customer = customer;
    }

    public OrderId id() {
        return id;
    }

    public CustomerId customer() {
        return customer;
    }

    public boolean isPlaced() {
        return placed;
    }

    /** A read-only view. The list cannot be changed from outside, and the lines cannot be built outside. */
    public List<OrderLine> lines() {
        return Collections.unmodifiableList(lines);
    }

    public Money total() {
        return lines.stream().map(OrderLine::subtotal).reduce(Money.ZERO, Money::plus);
    }

    public void addLine(String sku, Money unitPrice, int quantity) {
        if (placed) {
            throw new InvariantViolated("a placed order cannot change");
        }
        if (quantity < 1 || quantity > MAX_PER_LINE) {
            throw new InvariantViolated("a line has between 1 and " + MAX_PER_LINE + " of an item");
        }
        for (int i = 0; i < lines.size(); i++) {
            OrderLine existing = lines.get(i);
            if (existing.sku().equals(sku)) {
                if (existing.quantity() + quantity > MAX_PER_LINE) {
                    throw new InvariantViolated("a line has between 1 and " + MAX_PER_LINE + " of an item");
                }
                lines.set(i, new OrderLine(sku, existing.unitPrice(), existing.quantity() + quantity));
                if (total().compareTo(CREDIT_LIMIT) > 0) {
                    lines.set(i, existing);
                    throw new InvariantViolated("the order total may not pass " + CREDIT_LIMIT);
                }
                return;
            }
        }
        OrderLine line = new OrderLine(sku, unitPrice, quantity);
        if (total().plus(line.subtotal()).compareTo(CREDIT_LIMIT) > 0) {
            throw new InvariantViolated("the order total may not pass " + CREDIT_LIMIT);
        }
        lines.add(line);
    }

    public void place() {
        if (lines.isEmpty()) {
            throw new InvariantViolated("an order cannot be placed empty");
        }
        placed = true;
    }

    /** A deep copy, so a stored order and a loaded order are never the same object. */
    public Order copy() {
        Order copy = new Order(id, customer);
        copy.lines.addAll(lines);
        copy.placed = placed;
        return copy;
    }
}
