package com.jk.explore.bff.real.shop;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * The second design: one endpoint in front of the five, for everybody.
 *
 * <p>This is the design most shops reach for, and it deserves to be taken seriously
 * rather than set up to fail. It removes four round trips from the customer's own
 * connection, which is the expensive part, and the pattern that replaces it keeps that
 * improvement rather than undoing it.
 *
 * <p>It also supports {@code ?fields=}, and that support is the reason this class
 * exists at all. Asking for six fields by name gets a response that is <em>smaller
 * than the phone's backend sends</em>, over real HTTP, measurable with {@code
 * Content-Length}. If this pattern were about payload size, this file would be the end
 * of the project. What it cannot do is add a field nobody owns — see {@code
 * /api/products/&#123;sku&#125;?fields=delivery}, which returns nothing, because a
 * delivery <em>sentence</em> is not in any of the five services and putting it here
 * would change a document five other clients also receive.
 */
@RestController
public class SharedApiController {

    private final Catalogue catalogue;
    private final CallCounter calls;

    public SharedApiController(Catalogue catalogue, CallCounter calls) {
        this.catalogue = catalogue;
        this.calls = calls;
    }

    @GetMapping("/api/products/{sku}")
    public Map<String, Object> product(
            @PathVariable String sku,
            @RequestParam(required = false) String fields) {

        // One call from the device, five inside the shop. That second number does not
        // improve here and does not improve under the pattern either; what changes is
        // which network the calls are on.
        calls.record("catalog");
        calls.record("pricing");
        calls.record("inventory");
        calls.record("reviews");
        calls.record("recommendations");

        Map<String, Object> whole = new LinkedHashMap<>(catalogue.catalog(sku));
        whole.put("pricing", catalogue.pricing(sku));
        whole.put("inventory", catalogue.inventory(sku));
        whole.put("reviews", catalogue.reviews(sku));
        whole.put("recommendations", catalogue.recommendations(sku));

        if (fields == null || fields.isBlank()) {
            return whole;
        }
        return project(whole, List.of(fields.split(",")));
    }

    /**
     * Keep only the named paths, where a path may reach one level into a nested
     * document — {@code pricing.nowPence}, say.
     *
     * <p>Thirty lines, and worth exactly as much as it looks: this is a real answer to
     * the size problem, and a reader who stops here has genuinely solved the size
     * problem. A name that is not in the document is dropped rather than rejected,
     * which is what every real implementation of this does and is also how the delivery
     * sentence comes back empty instead of erroring.
     */
    private static Map<String, Object> project(Map<String, Object> doc, List<String> paths) {
        Map<String, Object> out = new LinkedHashMap<>();
        for (String raw : paths) {
            String path = raw.trim();
            int dot = path.indexOf('.');
            if (dot < 0) {
                if (doc.containsKey(path)) {
                    out.put(path, doc.get(path));
                }
                continue;
            }
            String head = path.substring(0, dot);
            String tail = path.substring(dot + 1);
            Object nested = doc.get(head);
            if (nested instanceof Map<?, ?> map && map.containsKey(tail)) {
                @SuppressWarnings("unchecked")
                Map<String, Object> child =
                        (Map<String, Object>) out.computeIfAbsent(head, k -> new LinkedHashMap<String, Object>());
                child.put(tail, map.get(tail));
            }
        }
        return out;
    }
}
