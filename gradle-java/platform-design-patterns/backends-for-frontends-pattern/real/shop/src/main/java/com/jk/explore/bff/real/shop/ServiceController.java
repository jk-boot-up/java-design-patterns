package com.jk.explore.bff.real.shop;

import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * The five services, each on its own path.
 *
 * <p>Every endpoint here returns its whole document, because that is what a service
 * with one published shape does. Nothing in this class knows about a phone or a
 * desktop, and it should not: a client asking for less is a request these endpoints
 * have no vocabulary for, and inventing one is the design the next class along tries
 * and the pattern rejects.
 */
@RestController
public class ServiceController {

    private final Catalogue catalogue;
    private final CallCounter calls;

    public ServiceController(Catalogue catalogue, CallCounter calls) {
        this.catalogue = catalogue;
        this.calls = calls;
    }

    @GetMapping("/catalog/{sku}")
    public Map<String, Object> catalog(@PathVariable String sku) {
        calls.record("catalog");
        return catalogue.catalog(sku);
    }

    @GetMapping("/pricing/{sku}")
    public Map<String, Object> pricing(@PathVariable String sku) {
        calls.record("pricing");
        return catalogue.pricing(sku);
    }

    @GetMapping("/inventory/{sku}")
    public Map<String, Object> inventory(@PathVariable String sku) {
        calls.record("inventory");
        return catalogue.inventory(sku);
    }

    @GetMapping("/reviews/{sku}")
    public Map<String, Object> reviews(@PathVariable String sku) {
        calls.record("reviews");
        return catalogue.reviews(sku);
    }

    @GetMapping("/recommendations/{sku}")
    public Map<String, Object> recommendations(@PathVariable String sku) {
        calls.record("recommendations");
        return catalogue.recommendations(sku);
    }

    /**
     * The pricing team's review, as an endpoint the demo can call.
     *
     * <p>It takes no body and changes one boolean: from here on, the shop says this
     * product's higher price was not held long enough to be advertised against. Both
     * backends are told, because both read pricing on every request. What they do with
     * it is the last act.
     */
    @PostMapping("/pricing/review")
    public Map<String, Object> applyPricingReview() {
        catalogue.applyPricingReview();
        return Map.of(
                "listPriceHeldLongEnough", catalogue.listPriceHeldLongEnough(),
                "note", "the higher price no longer qualifies to be advertised against");
    }

    /** The shop's own tally of calls that arrived, and a way to zero it between acts. */
    @GetMapping("/calls")
    public Map<String, Object> calls() {
        return calls.snapshot();
    }

    @PostMapping("/calls/reset")
    public Map<String, Object> resetCalls() {
        calls.reset();
        return calls.snapshot();
    }
}
