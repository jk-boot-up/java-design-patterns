package com.jk.explore.pagecontroller;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import java.io.IOException;
import java.util.Map;

/**
 * The pattern: one controller per page. Each reads its own input, makes its own decisions and sends its own reply.
 */
public final class Controllers {

    /** GET /product?sku=... */
    public static final class ProductController implements HttpHandler {
        public void handle(HttpExchange ex) throws IOException {
            String sku = Web.params(ex).get("sku");
            if (!Shop.PRODUCTS.containsKey(sku)) {
                Web.reply(ex, 404, "no product " + sku);
                return;
            }
            Web.reply(ex, 200, Shop.describe(sku));
        }
    }

    /** GET /basket?add=...&qty=... ; needs a logged-in customer. */
    public static final class BasketController implements HttpHandler {
        public void handle(HttpExchange ex) throws IOException {
            if (!Web.loggedIn(ex)) {
                Web.reply(ex, 401, "please log in");
                return;
            }
            Map<String, String> p = Web.params(ex);
            int qty;
            try {
                qty = Integer.parseInt(p.getOrDefault("qty", "1"));
            } catch (NumberFormatException e) {
                Web.reply(ex, 400, "quantity must be a number");
                return;
            }
            Web.reply(ex, 200, "basket: " + qty + " x " + p.get("add"));
        }
    }

    /** GET /checkout ; should need a logged-in customer too, but its author forgot the check. */
    public static final class CheckoutController implements HttpHandler {
        public void handle(HttpExchange ex) throws IOException {
            Web.reply(ex, 200, "checkout: pay £63.44 with the card on file");
        }
    }

    /** GET /reviews?sku=... ; added in act four. */
    public static final class ReviewsController implements HttpHandler {
        public void handle(HttpExchange ex) throws IOException {
            Web.reply(ex, 200, "reviews for " + Web.params(ex).get("sku") + ": 4.5 stars from 12 customers");
        }
    }

    private Controllers() {
    }
}
