package com.jk.explore.remotefacade;

import com.sun.net.httpserver.HttpServer;
import java.util.Map;

/**
 * The pattern: a coarse-grained front for remote callers. One call reads a whole screen's worth; one call makes a whole change.
 *
 * <p>The facade holds no business rules of its own. It calls the order's
 * methods in-process, where calls are cheap, and packs the answer into one
 * reply. A change goes to one order method that checks everything first, so a
 * bad request changes nothing.
 */
public final class OrderFacade {

    /** The whole order screen in one reply. */
    public static String summary(Order o) {
        return o.id() + " | " + o.customer() + " | " + String.join(", ", o.items()) + " | "
                + RemoteFacadeDemo.pounds(o.totalPence()) + " | " + o.address() + " | " + o.slot();
    }

    /** Address and slot together: all or nothing. */
    public static String changeDelivery(Order o, String address, String slot) {
        o.changeDelivery(address, slot);
        return "delivery changed";
    }

    public static void register(HttpServer server, Order order) {
        server.createContext("/order-summary", ex -> Http.reply(ex, 200, summary(order)));
        server.createContext("/order-change-delivery", ex -> {
            Map<String, String> p = Http.params(ex);
            try {
                Http.reply(ex, 200, changeDelivery(order, p.get("to"), p.get("slot")));
            } catch (IllegalArgumentException e) {
                Http.reply(ex, 400, e.getMessage());
            }
        });
    }

    private OrderFacade() {
    }
}
