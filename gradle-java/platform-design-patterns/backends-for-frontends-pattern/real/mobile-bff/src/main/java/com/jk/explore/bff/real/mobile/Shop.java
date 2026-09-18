package com.jk.explore.bff.real.mobile;

import java.util.Map;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

/**
 * The shop's five services, as this backend sees them: five URLs.
 *
 * <p>Every method here is one real HTTP request to another process. That is the only
 * thing this class adds over Tier 1's version, and it is the thing Tier 1 could not
 * show — the calls the phone used to make across a mobile connection are now calls
 * across a data-centre network, and they are still calls.
 */
@Component
public class Shop {

    private static final ParameterizedTypeReference<Map<String, Object>> DOC =
            new ParameterizedTypeReference<>() {};

    private final RestClient client;

    public Shop(RestClient shopClient) {
        this.client = shopClient;
    }

    public Map<String, Object> catalog(String sku) {
        return get("/catalog/" + sku);
    }

    public Map<String, Object> pricing(String sku) {
        return get("/pricing/" + sku);
    }

    public Map<String, Object> inventory(String sku) {
        return get("/inventory/" + sku);
    }

    public Map<String, Object> reviews(String sku) {
        return get("/reviews/" + sku);
    }

    /**
     * Present, and never called by this backend.
     *
     * <p>Left here on purpose. The phone's product screen has no related-products
     * strip, so this backend does not ask — not because recommendations is slow, but
     * because the answer would have nowhere to go. A shared endpoint cannot make that
     * decision for one client; a backend that knows exactly one screen can, and the
     * shop's own call counter proves it made four calls rather than five.
     */
    public Map<String, Object> recommendations(String sku) {
        return get("/recommendations/" + sku);
    }

    private Map<String, Object> get(String path) {
        return client.get().uri(path).retrieve().body(DOC);
    }
}
