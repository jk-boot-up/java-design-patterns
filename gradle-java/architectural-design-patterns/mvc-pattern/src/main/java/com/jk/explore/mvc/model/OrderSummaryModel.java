package com.jk.explore.mvc.model;

import com.jk.explore.mvc.domain.Money;
import com.jk.explore.mvc.domain.Order;
import com.jk.explore.mvc.domain.OrderLine;

import java.util.List;

/**
 * <strong>This class is the whole pattern.</strong>
 *
 * <p>It holds the placed order's state and computes nothing on demand that it
 * has not already computed once, here. {@link #total()} is not an
 * arithmetic expression a view is trusted to repeat correctly — it is a
 * value this class already worked out from the order it was built from, and
 * every view that wants a total asks this class for it rather than deriving
 * its own.
 *
 * <p>That is the entire mechanism by which two views are guaranteed to
 * agree. Not code review, not a shared constant, not a convention — there is
 * exactly one place in the whole program that can produce an order total,
 * and every renderer reads it from here.
 */
public final class OrderSummaryModel {

    private final String orderId;
    private final String customerId;
    private final List<OrderLine> lines;
    private final Money total;

    private OrderSummaryModel(String orderId, String customerId,
                              List<OrderLine> lines, Money total) {
        this.orderId = orderId;
        this.customerId = customerId;
        this.lines = List.copyOf(lines);
        this.total = total;
    }

    public static OrderSummaryModel of(Order order) {
        return new OrderSummaryModel(order.id(), order.customerId(), order.lines(), order.total());
    }

    public String orderId() {
        return orderId;
    }

    public String customerId() {
        return customerId;
    }

    public List<OrderLine> lines() {
        return lines;
    }

    /** The one total. Every view reads this; no view is allowed to add one up itself. */
    public Money total() {
        return total;
    }

    public int itemCount() {
        int count = 0;
        for (OrderLine line : lines) {
            count += line.quantity();
        }
        return count;
    }
}
