package com.jk.explore.sidecarjavaproxy.real.gateway;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.atomic.AtomicInteger;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;

/**
 * The provider's side of the contract, with one change from §41's gateway that
 * is the whole reason this project has a Tier 2 at all.
 *
 * <p><b>The wobble is measured in milliseconds, not in attempts.</b> §41's
 * gateway declines the first <i>n</i> attempts at a payment, which makes a
 * retry count observable. That is no use here, because both proxies in this
 * project make exactly three attempts and the thing being compared is
 * <i>when</i> those attempts arrive. So this gateway is unwell for a fixed
 * number of milliseconds after each reset, and healthy afterwards, exactly as
 * Tier 1's simulated provider is. A proxy that spends its three attempts inside
 * the first few milliseconds gets three declines however many it is allowed; a
 * proxy that waits gets paid on the same three.
 *
 * <p><b>Every arrival is timestamped, here, at the far end.</b> The list under
 * {@code arrivals} is milliseconds since the reset, recorded by the provider as
 * the request lands. Not one figure in this project's README comes from a proxy
 * reporting on its own behaviour, because a proxy claiming to have waited is a
 * claim and a supplier's ledger is evidence.
 *
 * <p>The allowance rule is unchanged from §41: the account may make a fixed
 * number of attempts, and the one past it is <i>refused</i> with a {@code 429}
 * rather than declined. Both proxies must treat that refusal as final, and
 * neither may retry it. That is what stops "wait and try again" quietly
 * becoming "ask a struggling supplier more often".
 */
@RestController
public class ProviderController {

    /** Attempts the whole merchant account may make. */
    private volatile int allowance = 12;

    /** How long after a reset the provider declines everything. */
    private volatile long unwellForMillis = 0;

    /** When the current scenario started, for both the wobble and the clock. */
    private volatile long startedAt = System.nanoTime();

    private final AtomicInteger total = new AtomicInteger();
    private final AtomicInteger refused = new AtomicInteger();
    private final Map<String, AtomicInteger> byService = new ConcurrentHashMap<>();
    private final List<Map<String, Object>> arrivals = new CopyOnWriteArrayList<>();

    /** What the last caller's connection actually turned out to be. */
    private volatile String lastTransport = "nothing has called yet";

    @PostMapping("/pay")
    public ResponseEntity<Map<String, Object>> pay(
            @RequestBody Map<String, Object> payment,
            @RequestHeader(name = "X-Service", defaultValue = "unknown") String service,
            HttpServletRequest request) {

        lastTransport = describe(request);

        long atMillis = (System.nanoTime() - startedAt) / 1_000_000L;
        String reference = String.valueOf(payment.getOrDefault("reference", "unknown"));
        int attemptsSoFar = total.incrementAndGet();
        byService.computeIfAbsent(service, k -> new AtomicInteger()).incrementAndGet();

        if (attemptsSoFar > allowance) {
            record(atMillis, reference, service, "refused");
            refused.incrementAndGet();
            return ResponseEntity.status(HttpStatus.TOO_MANY_REQUESTS).body(body(
                    "refused", reference, service,
                    "the account's " + allowance + "-attempt allowance is spent"));
        }

        if (atMillis < unwellForMillis) {
            record(atMillis, reference, service, "declined");
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(body(
                    "declined", reference, service,
                    "arrived at " + atMillis + "ms, unwell until " + unwellForMillis + "ms"));
        }

        record(atMillis, reference, service, "charged");
        Map<String, Object> ok = body("paid", reference, service, "arrived at " + atMillis + "ms");
        ok.put("receipt", "pay_" + reference);
        ok.put("amountPence", payment.get("amountPence"));
        return ResponseEntity.ok(ok);
    }

    /** Everything the gateway saw, from its own end. */
    @GetMapping("/attempts")
    public Map<String, Object> attempts() {
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("allowance", allowance);
        out.put("unwellForMillis", unwellForMillis);
        out.put("total", total.get());
        out.put("refused", refused.get());
        Map<String, Integer> services = new LinkedHashMap<>();
        byService.forEach((name, count) -> services.put(name, count.get()));
        out.put("byService", services);
        out.put("arrivals", new ArrayList<>(arrivals));
        out.put("firstToLastMillis", spread());
        out.put("transport", lastTransport);
        return out;
    }

    /** Clear the tallies, restart the clock, and set up the next scenario. */
    @PostMapping("/reset")
    public Map<String, Object> reset(@RequestBody(required = false) Map<String, Object> settings) {
        if (settings != null) {
            if (settings.get("unwellForMillis") != null) {
                unwellForMillis = Long.parseLong(String.valueOf(settings.get("unwellForMillis")));
            }
            if (settings.get("allowance") != null) {
                allowance = Integer.parseInt(String.valueOf(settings.get("allowance")));
            }
        }
        total.set(0);
        refused.set(0);
        byService.clear();
        arrivals.clear();
        startedAt = System.nanoTime();
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("allowance", allowance);
        out.put("unwellForMillis", unwellForMillis);
        return out;
    }

    /**
     * How far apart the first and last attempts were.
     *
     * <p>This single number is the comparison the project is about. Under a
     * proxy that cannot wait it is a handful of milliseconds; under one that
     * can, it is several hundred. The attempt <i>count</i> is the same either
     * way, which is what makes the spread the honest figure to quote.
     */
    private long spread() {
        if (arrivals.size() < 2) {
            return 0;
        }
        long first = ((Number) arrivals.get(0).get("atMillis")).longValue();
        long last = ((Number) arrivals.get(arrivals.size() - 1).get("atMillis")).longValue();
        return last - first;
    }

    private void record(long atMillis, String reference, String service, String outcome) {
        Map<String, Object> entry = new LinkedHashMap<>();
        entry.put("atMillis", atMillis);
        entry.put("reference", reference);
        entry.put("service", service);
        entry.put("outcome", outcome);
        arrivals.add(entry);
    }

    private Map<String, Object> body(String outcome, String reference, String service, String note) {
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("outcome", outcome);
        out.put("reference", reference);
        out.put("service", service);
        out.put("note", note);
        return out;
    }

    /**
     * Report the transport the caller arrived on.
     *
     * <p>Tomcat stashes the negotiated protocol under a request attribute; there
     * is no portable servlet API for it, which is why the attribute name appears
     * here as a string. It is worth printing in this project for a reason §41
     * did not have: the Java proxy has to present TLS 1.3 to this gateway too,
     * and a forty-line proxy that quietly stopped doing so would otherwise look
     * like a success.
     */
    private String describe(HttpServletRequest request) {
        Object version = request.getAttribute("org.apache.tomcat.util.net.secure_protocol_version");
        if (version != null) {
            return version + " (the caller presented a certificate)";
        }
        return request.getScheme() + ", not encrypted";
    }
}
