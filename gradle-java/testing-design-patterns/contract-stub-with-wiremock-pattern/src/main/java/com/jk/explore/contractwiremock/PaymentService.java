package com.jk.explore.contractwiremock;

import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * The payment team's real service over HTTP. Version 2 renamed the reply field "result" to "outcome".
 */
public final class PaymentService implements AutoCloseable {

    private static final Pattern FIELD = Pattern.compile("\"(\\w+)\":\"([^\"]*)\"");
    private final HttpServer server;

    public PaymentService(int version) throws IOException {
        String field = version >= 2 ? "outcome" : "result";
        server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        server.createContext("/charges", exchange -> {
            String body = new String(exchange.getRequestBody().readAllBytes(), StandardCharsets.UTF_8);
            double amount = Double.parseDouble(value(body, "amount"));
            String reply;
            if (amount <= 0) {
                reply = "{\"" + field + "\":\"REJECTED\",\"reason\":\"amount must be positive\"}";
            } else if (value(body, "card").endsWith("0002")) {
                reply = "{\"" + field + "\":\"DECLINED\",\"reason\":\"insufficient funds\"}";
            } else {
                reply = "{\"" + field + "\":\"APPROVED\",\"reason\":\"\"}";
            }
            byte[] bytes = reply.getBytes(StandardCharsets.UTF_8);
            exchange.getResponseHeaders().set("Content-Type", "application/json");
            exchange.sendResponseHeaders(200, bytes.length);
            try (OutputStream out = exchange.getResponseBody()) {
                out.write(bytes);
            }
        });
        server.start();
    }

    static String value(String json, String name) {
        Matcher m = FIELD.matcher(json);
        while (m.find()) {
            if (m.group(1).equals(name)) {
                return m.group(2);
            }
        }
        return null;
    }

    public String url() {
        return "http://127.0.0.1:" + server.getAddress().getPort();
    }

    @Override
    public void close() {
        server.stop(0);
    }
}
