package com.jk.explore.externalisedconfig.real.checkout;

import org.springframework.core.env.ConfigurableEnvironment;
import org.springframework.core.env.EnumerablePropertySource;
import org.springframework.core.env.PropertySource;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Map;

/**
 * One endpoint: quote the delivery on a basket.
 *
 * <p>This is Tier 1's {@code ConfiguredCheckout.quote} with an HTTP door on
 * the front, and the thing to look at is <em>where</em> the threshold is read.
 * It is read inside {@link #quote}, on the request, every time — not in a
 * constructor, not in a field initialiser, not cached in a local. That single
 * placement is the whole pattern. A value read once at startup is a constant
 * that took a longer route to get there.
 *
 * <p>The response also carries {@code thresholdOrigin}, which is not decoration.
 * The first question anybody asks about a surprising number in production is
 * "where did that come from", and a service that cannot answer it has moved
 * the value out of the code without moving the explanation with it.
 */
@RestController
public class QuoteController {

    private static final String THRESHOLD_KEY = "delivery.freeOver";

    private final LastGoodSettings settings;
    private final ConfigurableEnvironment environment;

    QuoteController(LastGoodSettings settings, ConfigurableEnvironment environment) {
        this.settings = settings;
        this.environment = environment;
    }

    /**
     * @param total the basket's goods total, in pounds, as a decimal
     */
    @GetMapping("/quote")
    public Map<String, Object> quote(@RequestParam BigDecimal total) {

        // Read on the request. Underneath, this resolves a @RefreshScope bean,
        // so a refresh that happened one millisecond ago is already reflected
        // here -- and if that refresh brought in a value outside the declared
        // range, the last good one is returned instead.
        LastGoodSettings.Snapshot inForce = settings.current();

        BigDecimal threshold = inForce.freeOver();
        BigDecimal delivery = total.compareTo(threshold) >= 0
                ? BigDecimal.ZERO
                : inForce.standard();

        return Map.of(
                "goodsTotal", money(total),
                "deliveryCost", money(delivery),
                "freeDeliveryOver", money(threshold),
                "thresholdOrigin", originOf(THRESHOLD_KEY),
                "thresholdState", inForce.note(),
                "total", money(total.add(delivery)));
    }

    private static String money(BigDecimal amount) {
        return "£" + amount.setScale(2, RoundingMode.HALF_UP).toPlainString();
    }

    /**
     * Which property source actually supplied a key.
     *
     * <p>Spring's environment is a list of sources consulted in order, and the
     * first one that has the key wins. Walking that list in order and naming
     * the first hit is therefore the honest answer to "where did this value
     * come from" — and it is the answer that changes when somebody sets an
     * environment variable that quietly overrides the config server, which is
     * the confusing production incident this endpoint exists to prevent.
     */
    private String originOf(String key) {
        for (PropertySource<?> source : environment.getPropertySources()) {
            if (source instanceof EnumerablePropertySource<?> enumerable
                    && enumerable.containsProperty(key)) {
                return enumerable.getName();
            }
        }
        return "unknown";
    }
}
