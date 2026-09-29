package com.jk.explore.tokenspring;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.security.oauth2.jwt.JwtEncoder;

/**
 * The five acts: two real instances of the shop's Spring Boot server, called over HTTP.
 */
public final class SpringTokenAuthDemo {

    static final String SECRET = "demo-only-secret-keep-real-keys-in-a-secrets-manager-32b";
    static final HttpClient HTTP = HttpClient.newBuilder().cookieHandler(new java.net.CookieManager()).build();

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        try (ConfigurableApplicationContext a = start(SECRET); ConfigurableApplicationContext b = start(SECRET)) {
            String serverA = base(a);
            String serverB = base(b);

            out.add("ONE. Sessions kept in one server's memory.");
            get(serverA + "/session/login?customer=ana", null);
            out.add("  ana signs in on server A; the session cookie is kept");
            out.add("  next request, to A: " + show(get(serverA + "/session/cart", null)));
            out.add("  next request, to B: " + show(get(serverB + "/session/cart", null)));

            out.add("");
            out.add("TWO. A signed token from Spring Security, accepted by any instance.");
            String token = post(serverA + "/token", basic("ana", "demo-password")).body();
            String payload = new String(Base64.getUrlDecoder().decode(token.split("\\.")[1]), StandardCharsets.UTF_8);
            out.add("  POST /token with ana's password returns a JWT; its payload names sub=ana and an exp 15 minutes on");
            out.add("  server A: " + show(get(serverA + "/cart", bearer(token))));
            out.add("  server B: " + show(get(serverB + "/cart", bearer(token))) + "  (no shared session store)");

            out.add("");
            out.add("THREE. Forged and expired tokens are refused.");
            String[] parts = token.split("\\.");
            String benPayload = Base64.getUrlEncoder().withoutPadding()
                    .encodeToString(payload.replace("\"ana\"", "\"ben\"").getBytes(StandardCharsets.UTF_8));
            String forged = parts[0] + "." + benPayload + "." + parts[2];
            out.add("  payload changed to ben: " + show(get(serverA + "/cart", bearer(forged))));
            String expired = ShopApp.issue(a.getBean(JwtEncoder.class), "ana", Duration.ofMinutes(-2));
            out.add("  a token that expired 2 minutes ago: " + show(get(serverA + "/cart", bearer(expired))));

            out.add("");
            out.add("FOUR. Signing out early.");
            String laptop = post(serverA + "/token", basic("ana", "demo-password")).body();
            post(serverA + "/signout", bearer(laptop));
            out.add("  ana signs out on server A, which adds the token to its revoked list");
            out.add("  server A: " + show(get(serverA + "/cart", bearer(laptop))));
            out.add("  server B: " + show(get(serverB + "/cart", bearer(laptop))) + "  (its own list does not have it)");
            out.add("  so keep tokens short-lived, and share any revoked list");

            out.add("");
            out.add("FIVE. The bill: the key, and what the token shows.");
            out.add("  anyone can read the payload: " + (payload.contains("\"sub\":\"ana\"") ? "sub=ana, and when it expires" : payload));
            try (ConfigurableApplicationContext thief = start(SECRET)) {
                String minted = ShopApp.issue(thief.getBean(JwtEncoder.class), "ben", Duration.ofMinutes(15));
                out.add("  someone who stole the secret signs a token for ben: server A says " + show(get(serverA + "/cart", bearer(minted))));
            }
        }
        return out;
    }

    static ConfigurableApplicationContext start(String secret) {
        return new SpringApplicationBuilder(ShopApp.class)
                .properties("server.port=0", "shop.secret=" + secret, "spring.main.banner-mode=off",
                        "logging.level.root=OFF")
                .run();
    }

    static String base(ConfigurableApplicationContext ctx) {
        return "http://127.0.0.1:" + ctx.getEnvironment().getProperty("local.server.port");
    }

    static String basic(String user, String password) {
        return "Basic " + Base64.getEncoder().encodeToString((user + ":" + password).getBytes(StandardCharsets.UTF_8));
    }

    static String bearer(String token) {
        return "Bearer " + token;
    }

    static HttpResponse<String> get(String url, String authorization) throws Exception {
        HttpRequest.Builder r = HttpRequest.newBuilder(URI.create(url)).GET();
        if (authorization != null) {
            r.header("Authorization", authorization);
        }
        return HTTP.send(r.build(), HttpResponse.BodyHandlers.ofString());
    }

    static HttpResponse<String> post(String url, String authorization) throws Exception {
        return HTTP.send(HttpRequest.newBuilder(URI.create(url)).header("Authorization", authorization)
                .POST(HttpRequest.BodyPublishers.noBody()).build(), HttpResponse.BodyHandlers.ofString());
    }

    /** "200 ana's cart", or for a refusal, the status and the reason Spring Security gave. */
    static String show(HttpResponse<String> r) {
        if (r.statusCode() == 200) {
            return "200 " + r.body();
        }
        String why = r.headers().firstValue("WWW-Authenticate").orElse("");
        int at = why.indexOf("error_description=\"");
        String reason = at < 0 ? r.body() : why.substring(at + 19, why.indexOf('"', at + 19));
        reason = reason.replace("An error occurred while attempting to decode the Jwt: ", "").replaceAll(" at \\d{4}-.*", "");
        return r.statusCode() + " " + reason;
    }

    private SpringTokenAuthDemo() {
    }
}
