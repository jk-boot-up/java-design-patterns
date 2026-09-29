package com.jk.explore.pagecontroller;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import java.io.IOException;
import java.util.Map;

/**
 * Without the pattern: one handler for every page, choosing by path in one long method.
 *
 * <p>Someone added quantity parsing at the top, for the basket page. It now
 * runs for every page, and the product page, which has no quantity, fails.
 */
public final class OneHandler implements HttpHandler {

    @Override
    public void handle(HttpExchange ex) throws IOException {
        try {
            Map<String, String> p = Web.params(ex);
            int qty = Integer.parseInt(p.get("qty"));
            String path = ex.getRequestURI().getPath();
            if (path.equals("/product")) {
                Web.reply(ex, 200, Shop.describe(p.get("sku")));
            } else if (path.equals("/basket")) {
                Web.reply(ex, 200, "basket: " + qty + " x " + p.get("add"));
            } else {
                Web.reply(ex, 404, "no such page");
            }
        } catch (RuntimeException e) {
            Web.reply(ex, 500, "server error: " + e.getClass().getSimpleName());
        }
    }
}
