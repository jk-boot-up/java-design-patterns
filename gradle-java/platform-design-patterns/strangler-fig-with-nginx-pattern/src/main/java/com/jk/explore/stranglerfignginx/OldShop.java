package com.jk.explore.stranglerfignginx;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * The old shop: one program that does everything. Prices, stock, the basket, checkout and
 * order history all live here, behind the same address.
 *
 * <p>It is a real HTTP server, the JDK's built-in one, running inside this demo's own Java
 * program. NGINX, in its container, reaches it over the network.
 *
 * <p>It keeps each customer's basket in its own memory and remembers which basket is whose
 * with a cookie it names {@code LEGACYSESSION}. That detail is the whole of the sixth act.
 */
public class OldShop implements AutoCloseable {

    public static final String NAME = "old-shop";
    public static final String SESSION_COOKIE = "LEGACYSESSION";

    static final Map<String, Integer> PRICES = Map.of("SKU-1", 1299, "SKU-2", 450, "SKU-3", 2500);
    static final Map<String, Integer> STOCK = Map.of("SKU-1", 40, "SKU-2", 12, "SKU-3", 3);

    private final ExecutorService threads = ShopHttp.threads();
    private final HttpServer server;
    private final Map<String, List<String>> baskets = new ConcurrentHashMap<>();
    private final AtomicInteger sessions = new AtomicInteger();
    private final AtomicInteger orders = new AtomicInteger(1001);
    private final AtomicInteger priceRequests = new AtomicInteger();

    // When set, the next price request waits here until the demo lets it go. This is how
    // the demo keeps one request open, on purpose, while NGINX reloads.
    private volatile CountDownLatch gate;
    private volatile boolean heldRequestArrived;

    private OldShop() {
        server = ShopHttp.start(0, threads);
        server.createContext("/", this::handle);
    }

    public static OldShop start() {
        return new OldShop();
    }

    public int port() {
        return server.getAddress().getPort();
    }

    public int priceRequests() {
        return priceRequests.get();
    }

    /** The next price request will wait, open, until {@link #releaseHeldRequest()} is called. */
    public void holdTheNextPriceRequest() {
        heldRequestArrived = false;
        gate = new CountDownLatch(1);
    }

    /** True once the held price request has reached the old shop and is waiting. */
    public boolean heldRequestArrived() {
        return heldRequestArrived;
    }

    public void releaseHeldRequest() {
        CountDownLatch g = gate;
        gate = null;
        if (g != null) {
            g.countDown();
        }
    }

    private void handle(HttpExchange exchange) throws IOException {
        String method = exchange.getRequestMethod();
        String path = exchange.getRequestURI().getPath();
        try {
            if (method.equals("GET") && path.startsWith("/api/prices/")) {
                price(exchange, path.substring("/api/prices/".length()));
            } else if (method.equals("GET") && path.startsWith("/api/stock/")) {
                String sku = path.substring("/api/stock/".length());
                Integer onHand = STOCK.get(sku);
                if (onHand == null) {
                    ShopHttp.reply(exchange, 404, NAME, "no such product: " + sku);
                } else {
                    ShopHttp.reply(exchange, 200, NAME, sku + ": " + onHand + " in stock");
                }
            } else if (method.equals("GET") && path.equals("/api/basket")) {
                List<String> basket = basketOf(exchange);
                ShopHttp.reply(exchange, 200, NAME, "basket: " + basket.size() + " items");
            } else if (method.equals("POST") && path.equals("/api/basket/items")) {
                addToBasket(exchange);
            } else if (method.equals("POST") && path.equals("/api/checkout")) {
                checkout(exchange);
            } else if (method.equals("GET") && path.startsWith("/api/orders/")) {
                ShopHttp.reply(exchange, 200, NAME, "order " + path.substring("/api/orders/".length()) + ": delivered");
            } else {
                ShopHttp.reply(exchange, 404, NAME, "no such page: " + path);
            }
        } finally {
            exchange.close();
        }
    }

    private void price(HttpExchange exchange, String sku) throws IOException {
        priceRequests.incrementAndGet();
        CountDownLatch g = gate;
        if (g != null) {
            heldRequestArrived = true;
            try {
                if (!g.await(60, TimeUnit.SECONDS)) {
                    ShopHttp.reply(exchange, 504, NAME, "held too long");
                    return;
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }
        }
        Integer pence = PRICES.get(sku);
        if (pence == null) {
            ShopHttp.reply(exchange, 404, NAME, "no such product: " + sku);
        } else {
            ShopHttp.reply(exchange, 200, NAME, sku + " costs " + pence + " pence");
        }
    }

    private List<String> basketOf(HttpExchange exchange) {
        String session = ShopHttp.cookie(exchange, SESSION_COOKIE);
        if (session == null) {
            return List.of();
        }
        return baskets.getOrDefault(session, List.of());
    }

    private void addToBasket(HttpExchange exchange) throws IOException {
        String sku = ShopHttp.query(exchange, "sku");
        if (sku == null || !PRICES.containsKey(sku)) {
            ShopHttp.reply(exchange, 404, NAME, "no such product: " + sku);
            return;
        }
        String session = ShopHttp.cookie(exchange, SESSION_COOKIE);
        if (session == null || !baskets.containsKey(session)) {
            session = "L-" + sessions.incrementAndGet();
            baskets.put(session, new ArrayList<>());
            exchange.getResponseHeaders().add("Set-Cookie", SESSION_COOKIE + "=" + session + "; Path=/");
        }
        List<String> basket = baskets.get(session);
        synchronized (basket) {
            basket.add(sku);
        }
        ShopHttp.reply(exchange, 200, NAME, "basket: " + basket.size() + " items");
    }

    private void checkout(HttpExchange exchange) throws IOException {
        List<String> basket = basketOf(exchange);
        if (basket.isEmpty()) {
            ShopHttp.reply(exchange, 422, NAME, "your basket is empty");
            return;
        }
        int total = basket.stream().mapToInt(PRICES::get).sum();
        ShopHttp.reply(exchange, 200, NAME,
                "order " + orders.incrementAndGet() + " placed: " + basket.size() + " items, " + total + " pence");
    }

    @Override
    public void close() {
        releaseHeldRequest();
        server.stop(0);
        threads.shutdownNow();
    }
}
