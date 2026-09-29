package com.jk.explore.pageobjectselenium;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;

/**
 * The shop's checkout and confirmation pages, served over HTTP. Applying a coupon updates the total
 * 300 ms later, from JavaScript, as real pages that call a server do. The designers can rename the
 * apply button.
 */
public final class ShopSite implements AutoCloseable {

    private final HttpServer server;
    private volatile String applyId = "apply-btn";

    public ShopSite() throws IOException {
        server = HttpServer.create(new InetSocketAddress("0.0.0.0", 0), 0);
        server.createContext("/checkout", e -> send(e, checkout()));
        server.createContext("/confirmation", e -> send(e, """
                <html><body><h1 id="message">Thank you for your order</h1><p id="order-number">ORD-1042</p></body></html>
                """));
        server.start();
    }

    private String checkout() {
        return """
                <html><body>
                <input id="coupon"> <button id="%s">Apply</button>
                <p>Total: <span id="total">50.00</span> <span id="coupon-status"></span></p>
                <button id="place-order">Place order</button>
                <script>
                  document.getElementById('%s').onclick = function () {
                    var code = document.getElementById('coupon').value;
                    setTimeout(function () {             // the server answers a moment later
                      if (code === 'SAVE10') {
                        document.getElementById('total').textContent = '45.00';
                        document.getElementById('coupon-status').textContent = 'applied';
                      } else {
                        document.getElementById('coupon-status').textContent = 'not valid';
                      }
                    }, 300);
                  };
                  document.getElementById('place-order').onclick = function () { location.href = '/confirmation'; };
                </script>
                </body></html>
                """.formatted(applyId, applyId);
    }

    private static void send(HttpExchange e, String html) throws IOException {
        byte[] bytes = html.getBytes(StandardCharsets.UTF_8);
        e.getResponseHeaders().set("Content-Type", "text/html; charset=utf-8");
        e.sendResponseHeaders(200, bytes.length);
        try (OutputStream out = e.getResponseBody()) {
            out.write(bytes);
        }
    }

    /** The designers rename the apply button. */
    public void renameApplyButton(String id) {
        this.applyId = id;
    }

    public int port() {
        return server.getAddress().getPort();
    }

    @Override
    public void close() {
        server.stop(0);
    }
}
