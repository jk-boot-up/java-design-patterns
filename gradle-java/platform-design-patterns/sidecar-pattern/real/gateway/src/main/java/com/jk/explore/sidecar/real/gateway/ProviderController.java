package com.jk.explore.sidecar.real.gateway;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
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
 * The provider's side of the contract, with the two rules Tier 1 dramatises.
 *
 * <p><b>The wobble.</b> Set {@code declineFirst} to 2 and the first two attempts
 * at any one payment come back {@code 503}. The third succeeds. A caller with a
 * three-attempt policy gets paid; a caller with a one-attempt policy does not,
 * and neither caller had to change for that to be true.
 *
 * <p><b>The allowance.</b> The merchant account is allowed twelve attempts.
 * The thirteenth is not declined, it is <i>refused</i> -- {@code 429} -- and a
 * refusal is the one failure that must never be retried, because retrying it is
 * how one service's stale policy takes the whole account down. The proxy
 * beside each service is configured to retry {@code 503} and nothing else, so
 * this rule is enforced in exactly one file for every service in the shop.
 */
@RestController
public class ProviderController {

    /** Attempts the whole merchant account may make. Twelve, as in Tier 1. */
    private volatile int allowance = 12;

    /** How many attempts at each payment to decline before letting it through. */
    private volatile int declineFirst = 0;

    private final AtomicInteger total = new AtomicInteger();
    private final AtomicInteger refused = new AtomicInteger();
    private final Map<String, AtomicInteger> byService = new ConcurrentHashMap<>();
    private final Map<String, AtomicInteger> byReference = new ConcurrentHashMap<>();

    /** What the last caller's connection actually turned out to be. */
    private volatile String lastTransport = "nothing has called yet";

    @PostMapping("/pay")
    public ResponseEntity<Map<String, Object>> pay(
            @RequestBody Map<String, Object> payment,
            @RequestHeader(name = "X-Service", defaultValue = "unknown") String service,
            HttpServletRequest request) {

        lastTransport = describe(request);

        String reference = String.valueOf(payment.getOrDefault("reference", "unknown"));
        int attemptsSoFar = total.incrementAndGet();
        byService.computeIfAbsent(service, k -> new AtomicInteger()).incrementAndGet();

        if (attemptsSoFar > allowance) {
            refused.incrementAndGet();
            return ResponseEntity.status(HttpStatus.TOO_MANY_REQUESTS).body(body(
                    "refused", reference, service,
                    "the account's " + allowance + "-attempt allowance is spent"));
        }

        int attemptsAtThisPayment =
                byReference.computeIfAbsent(reference, k -> new AtomicInteger()).incrementAndGet();

        if (attemptsAtThisPayment <= declineFirst) {
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(body(
                    "declined", reference, service,
                    "attempt " + attemptsAtThisPayment + " -- try again"));
        }

        Map<String, Object> ok = body("paid", reference, service,
                "attempt " + attemptsAtThisPayment);
        ok.put("receipt", "pay_" + reference);
        ok.put("amountPence", payment.get("amountPence"));
        return ResponseEntity.ok(ok);
    }

    /** Everything the gateway saw, from its own end. */
    @GetMapping("/attempts")
    public Map<String, Object> attempts() {
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("allowance", allowance);
        out.put("total", total.get());
        out.put("refused", refused.get());
        Map<String, Integer> services = new LinkedHashMap<>();
        byService.forEach((name, count) -> services.put(name, count.get()));
        out.put("byService", services);
        out.put("transport", lastTransport);
        return out;
    }

    /** Clear the tallies and set up the next scenario. */
    @PostMapping("/reset")
    public Map<String, Object> reset(@RequestBody(required = false) Map<String, Object> settings) {
        if (settings != null) {
            if (settings.get("declineFirst") != null) {
                declineFirst = Integer.parseInt(String.valueOf(settings.get("declineFirst")));
            }
            if (settings.get("allowance") != null) {
                allowance = Integer.parseInt(String.valueOf(settings.get("allowance")));
            }
        }
        total.set(0);
        refused.set(0);
        byService.clear();
        byReference.clear();
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("allowance", allowance);
        out.put("declineFirst", declineFirst);
        return out;
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
     * here as a string. If it is ever missing the scheme still tells the reader
     * the honest thing, which is whether this connection was encrypted at all.
     */
    private String describe(HttpServletRequest request) {
        Object version = request.getAttribute("org.apache.tomcat.util.net.secure_protocol_version");
        if (version != null) {
            return version + " (the caller presented a certificate)";
        }
        return request.getScheme() + ", not encrypted";
    }
}
