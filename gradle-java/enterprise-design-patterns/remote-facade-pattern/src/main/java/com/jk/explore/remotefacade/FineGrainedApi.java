package com.jk.explore.remotefacade;

import com.sun.net.httpserver.HttpServer;

/**
 * Without the pattern: the order's small methods published one by one over the network.
 */
public final class FineGrainedApi {

    public static void register(HttpServer server, Order order) {
        server.createContext("/order/customer", ex -> Http.reply(ex, 200, order.customer()));
        server.createContext("/order/items", ex -> Http.reply(ex, 200, String.join(", ", order.items())));
        server.createContext("/order/total", ex -> Http.reply(ex, 200, RemoteFacadeDemo.pounds(order.totalPence())));
        server.createContext("/order/address", ex -> Http.reply(ex, 200, order.address()));
        server.createContext("/order/slot", ex -> Http.reply(ex, 200, order.slot()));
        server.createContext("/order/change-address", ex -> {
            order.changeAddress(Http.params(ex).get("to"));
            Http.reply(ex, 200, "address changed");
        });
        server.createContext("/order/book-slot", ex -> {
            try {
                order.bookSlot(Http.params(ex).get("slot"));
                Http.reply(ex, 200, "slot booked");
            } catch (IllegalArgumentException e) {
                Http.reply(ex, 400, e.getMessage());
            }
        });
    }

    private FineGrainedApi() {
    }
}
