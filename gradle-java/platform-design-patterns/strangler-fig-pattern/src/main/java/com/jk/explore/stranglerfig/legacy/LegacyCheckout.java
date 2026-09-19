package com.jk.explore.stranglerfig.legacy;

import com.jk.explore.stranglerfig.domain.Line;
import com.jk.explore.stranglerfig.domain.Mailer;
import com.jk.explore.stranglerfig.domain.Order;
import com.jk.explore.stranglerfig.domain.Payer;
import com.jk.explore.stranglerfig.domain.Pricer;
import com.jk.explore.stranglerfig.domain.Pricing;
import com.jk.explore.stranglerfig.domain.Result;
import com.jk.explore.stranglerfig.domain.StockKeeper;

import java.util.HashMap;
import java.util.Map;

/**
 * <strong>The legacy checkout: one large class that does pricing, stock, payment
 * and email.</strong> It works. It is also where every change is slow and every
 * incident starts. Its four capabilities are public methods so that a router can
 * call one without the others, which is the seam a strangler needs.
 *
 * <p>Two of its behaviours are quirks that customers have paid for years: VAT is
 * rounded on each line, and delivery is free only when the goods cost strictly
 * more than fifty pounds.
 */
public class LegacyCheckout implements Pricer, StockKeeper, Payer, Mailer {

    public static final long FREE_DELIVERY_ABOVE_PENCE = 5_000;
    public static final long DELIVERY_PENCE = 495;

    private final Map<String, Integer> stock = new HashMap<>();
    private int charges;
    private int emails;

    public LegacyCheckout(Map<String, Integer> openingStock) {
        stock.putAll(openingStock);
    }

    @Override
    public Pricing price(Order order) {
        long vat = 0;
        for (Line line : order.lines()) {
            vat += (line.linePence() * 20 + 50) / 100; // half-up, per line
        }
        long subtotal = order.subtotalPence();
        long delivery = subtotal > FREE_DELIVERY_ABOVE_PENCE ? 0 : DELIVERY_PENCE;
        return new Pricing(subtotal, vat, delivery, subtotal + vat + delivery);
    }

    @Override
    public boolean reserve(Order order) {
        for (Line line : order.lines()) {
            if (stock.getOrDefault(line.sku(), 0) < line.quantity()) {
                return false;
            }
        }
        order.lines().forEach(l -> stock.merge(l.sku(), -l.quantity(), Integer::sum));
        return true;
    }

    @Override
    public int onHand(String sku) {
        return stock.getOrDefault(sku, 0);
    }

    @Override
    public String charge(long totalPence) {
        return "L-" + (++charges);
    }

    @Override
    public boolean confirm(Order order) {
        emails++;
        return true;
    }

    /** The whole thing, in one call. */
    public Result checkout(Order order) {
        Pricing pricing = price(order);
        boolean reserved = reserve(order);
        String charge = reserved ? charge(pricing.totalPence()) : null;
        boolean emailed = charge != null && confirm(order);
        return new Result(pricing, reserved, charge, emailed);
    }

    public int emailsSent() {
        return emails;
    }
}
