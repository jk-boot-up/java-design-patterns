package com.jk.explore.stranglerfig.route;

import com.jk.explore.stranglerfig.domain.Capability;
import com.jk.explore.stranglerfig.domain.Mailer;
import com.jk.explore.stranglerfig.domain.Order;
import com.jk.explore.stranglerfig.domain.Payer;
import com.jk.explore.stranglerfig.domain.Pricer;
import com.jk.explore.stranglerfig.domain.Pricing;
import com.jk.explore.stranglerfig.domain.Result;
import com.jk.explore.stranglerfig.domain.StockKeeper;

import java.util.ArrayList;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;

/**
 * <strong>The router in front of the legacy checkout.</strong> Each capability has
 * its own switch. Moving pricing across does not move stock, and if pricing
 * misbehaves, pricing alone comes back. In SHADOW mode a capability is served by
 * legacy, the new implementation is called too, and any difference is recorded.
 */
public class Router {

    private final Map<Capability, Route> routes = new EnumMap<>(Capability.class);
    private final Pricer legacyPricer, newPricer;
    private final StockKeeper legacyStock, newStock;
    private final Payer legacyPayer, newPayer;
    private final Mailer legacyMailer, newMailer;
    private final List<String> differences = new ArrayList<>();
    private int compared;

    public Router(Pricer legacyPricer, Pricer newPricer, StockKeeper legacyStock, StockKeeper newStock,
                  Payer legacyPayer, Payer newPayer, Mailer legacyMailer, Mailer newMailer) {
        this.legacyPricer = legacyPricer;
        this.newPricer = newPricer;
        this.legacyStock = legacyStock;
        this.newStock = newStock;
        this.legacyPayer = legacyPayer;
        this.newPayer = newPayer;
        this.legacyMailer = legacyMailer;
        this.newMailer = newMailer;
        for (Capability c : Capability.values()) {
            routes.put(c, Route.LEGACY);
        }
    }

    public void route(Capability capability, Route route) {
        routes.put(capability, route);
    }

    public Route routeOf(Capability capability) {
        return routes.get(capability);
    }

    public Result checkout(Order order) {
        Pricing pricing = price(order);
        boolean reserved = reserve(order);
        String charge = reserved ? charge(pricing.totalPence()) : null;
        boolean emailed = charge != null && confirm(order);
        return new Result(pricing, reserved, charge, emailed);
    }

    private Pricing price(Order order) {
        return switch (routes.get(Capability.PRICING)) {
            case LEGACY -> legacyPricer.price(order);
            case NEW -> newPricer.price(order);
            case SHADOW -> {
                Pricing served = legacyPricer.price(order);
                Pricing shadow = newPricer.price(order);
                compared++;
                if (!served.equals(shadow)) {
                    differences.add("order " + order.id() + ": legacy " + served + ", new " + shadow);
                }
                yield served;
            }
        };
    }

    private boolean reserve(Order order) {
        return routes.get(Capability.STOCK) == Route.NEW ? newStock.reserve(order) : legacyStock.reserve(order);
    }

    private String charge(long total) {
        return routes.get(Capability.PAYMENT) == Route.NEW ? newPayer.charge(total) : legacyPayer.charge(total);
    }

    private boolean confirm(Order order) {
        return routes.get(Capability.EMAIL) == Route.NEW ? newMailer.confirm(order) : legacyMailer.confirm(order);
    }

    /** How many orders the shadow has compared. */
    public int compared() {
        return compared;
    }

    /** What the shadow found: every order where legacy and new disagreed. */
    public List<String> differences() {
        return List.copyOf(differences);
    }

    public void clearShadow() {
        differences.clear();
        compared = 0;
    }
}
