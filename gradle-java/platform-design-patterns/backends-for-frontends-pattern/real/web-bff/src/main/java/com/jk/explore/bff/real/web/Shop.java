package com.jk.explore.bff.real.web;

import java.util.Map;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

/**
 * The shop's five services, as this backend sees them: five URLs.
 *
 * <p>Identical to the phone backend's copy of this class, and it should be. Neither
 * backend has privileged access and neither can reach anything the other cannot. Both
 * can call all five services. What differs between the two backends is entirely which
 * of these methods each one chooses to call, and what it does with the answers — which
 * is the pattern's claim stated as code rather than as a diagram.
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

    /** Called here, unlike in the phone's backend, because this page has the strip. */
    public Map<String, Object> recommendations(String sku) {
        return get("/recommendations/" + sku);
    }

    private Map<String, Object> get(String path) {
        return client.get().uri(path).retrieve().body(DOC);
    }
}
