package com.jk.explore.broker;

import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.util.Map;

/**
 * The shop's back-end services, each a small web server that answers one kind of question.
 */
public final class Services {

    static final Map<String, Integer> STOCK = Map.of("KETTLE-1", 4, "MUG-1", 20);

    /** Stock: "?sku=KETTLE-1" answers "4". */
    public static HttpServer stock() throws IOException {
        return Http.serve("/", ex -> {
            String sku = ex.getRequestURI().getQuery().replace("sku=", "");
            Http.reply(ex, 200, String.valueOf(STOCK.getOrDefault(sku, 0)));
        });
    }

    /** Price: answers the price and says which instance answered. */
    public static HttpServer price(String instance) throws IOException {
        return Http.serve("/", ex -> Http.reply(ex, 200, "£30.00 (from " + instance + ")"));
    }

    private Services() {
    }
}
