package com.jk.explore.stranglerfignginx;

import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * A customer's browser, reduced to what this demo needs: send a request to the shop's one
 * public address, which is NGINX, and keep any cookie the shop sets.
 *
 * <p>It opens a fresh connection for every request. A browser would normally keep a connection
 * open and reuse it; turning that off keeps each request separate, so the second act can say
 * exactly which request NGINX handled with which configuration.
 */
public class Browser {

    static {
        System.setProperty("http.keepAlive", "false");
    }

    private final String address;
    private final Map<String, String> cookies = new LinkedHashMap<>();

    public Browser(String address) {
        this.address = address;
    }

    public Answer get(String path) {
        return send("GET", path);
    }

    public Answer post(String path) {
        return send("POST", path);
    }

    /** One response header of a GET, such as the Cache-Control an old NGINX rule adds. */
    public String headerOf(String path, String header) {
        try {
            HttpURLConnection http = (HttpURLConnection) URI.create(address + path).toURL().openConnection();
            http.setConnectTimeout(5_000);
            http.setReadTimeout(90_000);
            http.getResponseCode();
            String value = http.getHeaderField(header);
            http.disconnect();
            return value;
        } catch (IOException e) {
            throw new IllegalStateException("GET " + path + " failed: " + e.getMessage(), e);
        }
    }

    /** Sets a cookie by hand, as if a site had set it earlier. */
    public Browser withCookie(String name, String value) {
        cookies.put(name, value);
        return this;
    }

    public Map<String, String> cookies() {
        return Map.copyOf(cookies);
    }

    private Answer send(String method, String path) {
        try {
            HttpURLConnection http = (HttpURLConnection) URI.create(address + path).toURL().openConnection();
            http.setRequestMethod(method);
            http.setConnectTimeout(5_000);
            http.setReadTimeout(90_000);
            http.setUseCaches(false);
            if (!cookies.isEmpty()) {
                http.setRequestProperty("Cookie", cookies.entrySet().stream()
                        .map(e -> e.getKey() + "=" + e.getValue()).collect(Collectors.joining("; ")));
            }
            if (method.equals("POST")) {
                http.setDoOutput(true);
                http.getOutputStream().close();
            }
            int status = http.getResponseCode();
            String servedBy = http.getHeaderField("X-Served-By");
            // Header names are not case-sensitive, and the JDK's server sends "Set-cookie".
            for (Map.Entry<String, List<String>> header : http.getHeaderFields().entrySet()) {
                if (header.getKey() != null && header.getKey().equalsIgnoreCase("Set-Cookie")) {
                    for (String c : header.getValue()) {
                        String[] pair = c.split(";", 2)[0].split("=", 2);
                        cookies.put(pair[0].trim(), pair[1].trim());
                    }
                }
            }
            InputStream in = status >= 400 ? http.getErrorStream() : http.getInputStream();
            String body = in == null ? "" : new String(in.readAllBytes(), StandardCharsets.UTF_8);
            http.disconnect();
            return new Answer(status, servedBy == null ? "nginx" : servedBy, body.trim());
        } catch (IOException e) {
            throw new IllegalStateException(method + " " + path + " failed: " + e.getMessage(), e);
        }
    }
}
