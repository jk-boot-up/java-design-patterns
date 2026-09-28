package com.jk.explore.stranglerfignginx;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.ExecutorService;

/**
 * The new service: the rewrite, grown one route at a time. So far it has built prices and
 * checkout, and nothing else. It answers the same web addresses the old shop answers, so that
 * NGINX can send a route to either without the customer's browser noticing.
 *
 * <p>It keeps its own baskets, under a cookie of its own called {@code session}. It has never
 * heard of the old shop's {@code LEGACYSESSION}.
 *
 * <p>It writes down the exact path of every request it receives, which is how the fourth act
 * shows what NGINX did to a path on the way through.
 */
public class NewService implements AutoCloseable {

    public static final String NAME = "new-service";
    public static final String SESSION_COOKIE = "session";

    // The rewrite's prices, written to match the old shop's exactly, so that moving a route
    // changes who answers and never what the customer pays.
    static final Map<String, Integer> PRICES = Map.of("SKU-1", 1299, "SKU-2", 450, "SKU-3", 2500);

    private final ExecutorService threads = ShopHttp.threads();
    private final Map<String, List<String>> baskets = new ConcurrentHashMap<>();
    private final List<String> pathsReceived = new CopyOnWriteArrayList<>();
    private final List<String> cookiesReceived = new CopyOnWriteArrayList<>();
    private final int port;
    private HttpServer server;

    private NewService() {
        server = ShopHttp.start(0, threads);
        server.createContext("/", this::handle);
        port = server.getAddress().getPort();
    }

    public static NewService start() {
        return new NewService();
    }

    public int port() {
        return port;
    }

    public List<String> pathsReceived() {
        return List.copyOf(pathsReceived);
    }

    public String lastPathReceived() {
        return pathsReceived.isEmpty() ? null : pathsReceived.get(pathsReceived.size() - 1);
    }

    public String lastCookieReceived() {
        return cookiesReceived.isEmpty() ? null : cookiesReceived.get(cookiesReceived.size() - 1);
    }

    public boolean running() {
        return server != null;
    }

    /** The service goes down: its port stops accepting connections. */
    public void stop() {
        if (server != null) {
            server.stop(0);
            server = null;
        }
    }

    /** The service comes back up, on the same port, so NGINX's configuration still points at it. */
    public void startAgain() {
        if (server == null) {
            server = ShopHttp.start(port, threads);
            server.createContext("/", this::handle);
        }
    }

    private void handle(HttpExchange exchange) throws IOException {
        String method = exchange.getRequestMethod();
        String path = exchange.getRequestURI().getPath();
        pathsReceived.add(path);
        String cookie = exchange.getRequestHeaders().getFirst("Cookie");
        cookiesReceived.add(cookie == null ? "" : cookie);
        try {
            if (method.equals("GET") && path.startsWith("/api/prices/")) {
                String sku = path.substring("/api/prices/".length());
                Integer pence = PRICES.get(sku);
                if (pence == null) {
                    ShopHttp.reply(exchange, 404, NAME, "no such product: " + sku);
                } else {
                    ShopHttp.reply(exchange, 200, NAME, sku + " costs " + pence + " pence");
                }
            } else if (method.equals("POST") && path.equals("/api/checkout")) {
                String session = ShopHttp.cookie(exchange, SESSION_COOKIE);
                List<String> basket = session == null ? List.of() : baskets.getOrDefault(session, List.of());
                if (basket.isEmpty()) {
                    ShopHttp.reply(exchange, 422, NAME, "your basket is empty");
                } else {
                    ShopHttp.reply(exchange, 200, NAME, "order placed: " + basket.size() + " items");
                }
            } else {
                ShopHttp.reply(exchange, 404, NAME, "no such page: " + path);
            }
        } finally {
            exchange.close();
        }
    }

    @Override
    public void close() {
        stop();
        threads.shutdownNow();
    }
}
