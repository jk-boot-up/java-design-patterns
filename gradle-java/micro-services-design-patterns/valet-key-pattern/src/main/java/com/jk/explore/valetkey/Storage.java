package com.jk.explore.valetkey;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;

/**
 * The file storage service. It accepts the shop's own master credential, or a valet key: a URL whose signature it checks.
 */
public final class Storage implements AutoCloseable {

    static final String MASTER = "master-credential-only-the-shop-has";

    private final HttpServer server;
    private final Signer signer;
    private final Map<String, byte[]> files = new ConcurrentHashMap<>();

    public Storage(Signer signer) throws IOException {
        this.signer = signer;
        server = HttpServer.create(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0), 0);
        server.setExecutor(Executors.newCachedThreadPool());
        server.createContext("/", this::handle);
        server.start();
    }

    private void handle(HttpExchange ex) throws IOException {
        String method = ex.getRequestMethod();
        String path = ex.getRequestURI().getPath();
        byte[] body = ex.getRequestBody().readAllBytes();
        boolean master = MASTER.equals(ex.getRequestHeaders().getFirst("Authorization"));
        if (!master) {
            Map<String, String> q = query(ex.getRequestURI().getRawQuery());
            if (!q.containsKey("sig")) {
                reply(ex, 401, "no key");
                return;
            }
            long expires = Long.parseLong(q.get("expires"));
            long max = Long.parseLong(q.get("max"));
            if (!signer.sign(method, path, expires, max).equals(q.get("sig"))) {
                reply(ex, 403, "key does not allow " + method + " " + path);
                return;
            }
            if (System.currentTimeMillis() > expires) {
                reply(ex, 403, "key expired");
                return;
            }
            if (body.length > max) {
                reply(ex, 413, "file too large: " + body.length + " bytes, key allows " + max);
                return;
            }
        }
        if (method.equals("PUT")) {
            files.put(path, body);
            reply(ex, 201, "stored " + path + " (" + body.length + " bytes)");
        } else {
            byte[] f = files.get(path);
            reply(ex, f == null ? 404 : 200, f == null ? "not found" : f.length + " bytes");
        }
    }

    private static Map<String, String> query(String q) {
        Map<String, String> m = new HashMap<>();
        if (q != null) {
            for (String kv : q.split("&")) {
                String[] p = kv.split("=", 2);
                m.put(p[0], p.length > 1 ? p[1] : "");
            }
        }
        return m;
    }

    private static void reply(HttpExchange ex, int status, String text) throws IOException {
        byte[] b = text.getBytes();
        ex.sendResponseHeaders(status, b.length);
        try (OutputStream out = ex.getResponseBody()) {
            out.write(b);
        }
    }

    public String url() {
        return "http://localhost:" + server.getAddress().getPort();
    }

    public int fileCount() {
        return files.size();
    }

    @Override
    public void close() {
        server.stop(0);
    }
}
