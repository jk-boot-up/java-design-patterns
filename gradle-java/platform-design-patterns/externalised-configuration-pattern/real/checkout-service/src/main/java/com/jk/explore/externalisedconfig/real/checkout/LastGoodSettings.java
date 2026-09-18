package com.jk.explore.externalisedconfig.real.checkout;

import org.springframework.beans.factory.ObjectProvider;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;

/**
 * Keeps the last value that passed validation, and hands it out when the
 * current one does not.
 *
 * <p><strong>Why this class exists is the most useful thing in the Tier 2
 * directory, so it is worth the paragraph.</strong>
 *
 * <p>Tier 1 made a promise: when a change is rejected, the shop keeps trading
 * on the last value that was accepted. A rejected change should be a
 * non-event for customers. Spring does not give you that for free, and the
 * first version of this demo assumed it did.
 *
 * <p>What actually happens with a plain {@code @RefreshScope @Validated}
 * bean is this. A refresh discards the bean. The next request asks for it, so
 * Spring rebuilds it, binds the new value, runs validation, and validation
 * fails — which means the request fails. Then the next request fails the same
 * way, and so does every request after it. The bad value never reaches a
 * customer, which is the important half, but neither does anything else: the
 * checkout endpoint returns 500 until somebody fixes the configuration. One
 * mistyped number in a file took the shop down without any code being
 * deployed, which is precisely the risk the pattern is supposed to be
 * managing.
 *
 * <p>So the range check on its own is not the whole guard. The guard is the
 * range check <em>plus</em> somewhere to fall back to, and that second half
 * is this class. It is about thirty lines, and every team that externalises a
 * value and stops at {@code @Validated} is missing it.
 *
 * <p>This is a deliberately plain singleton, not a refresh-scoped bean. It has
 * to survive the refresh that destroys {@link DeliverySettings}, because
 * surviving the refresh is its entire job.
 */
@Component
public class LastGoodSettings {

    /**
     * A usable pair of settings, and whether they are the ones currently
     * configured.
     *
     * @param freeOver the threshold in force right now
     * @param standard the delivery charge in force right now
     * @param current  {@code true} if these are the configured values,
     *                 {@code false} if the configured values were rejected
     *                 and these are the last ones that passed
     * @param note     a human-readable account of the above, for the response
     */
    public record Snapshot(BigDecimal freeOver, BigDecimal standard,
                           boolean current, String note) {
    }

    /**
     * Resolved fresh on every call rather than injected once, because
     * injecting a {@code @RefreshScope} bean into a singleton captures a proxy
     * whose target is rebuilt on refresh — and rebuilding is exactly the
     * moment that can throw.
     */
    private final ObjectProvider<DeliverySettings> configured;

    private volatile BigDecimal lastGoodFreeOver;
    private volatile BigDecimal lastGoodStandard;

    LastGoodSettings(ObjectProvider<DeliverySettings> configured) {
        this.configured = configured;
    }

    /**
     * The settings to trade on right now.
     *
     * @throws RuntimeException if the configured settings are invalid
     *                          <em>and</em> nothing has ever been accepted, in
     *                          which case there is no last-good value to fall
     *                          back to and failing is the only honest answer.
     *                          In practice this cannot happen after startup,
     *                          because the service refuses to start on an
     *                          invalid value in the first place.
     */
    public Snapshot current() {
        try {
            DeliverySettings fresh = configured.getObject();

            // Both getters are called inside the try. Touching the proxy is
            // what forces the rebuild, and therefore the bind and the
            // validation, so this is where the failure surfaces.
            BigDecimal freeOver = fresh.getFreeOver();
            BigDecimal standard = fresh.getStandard();

            lastGoodFreeOver = freeOver;
            lastGoodStandard = standard;
            return new Snapshot(freeOver, standard, true, "in force");

        } catch (RuntimeException rejected) {
            if (lastGoodFreeOver == null) {
                throw rejected;
            }
            return new Snapshot(lastGoodFreeOver, lastGoodStandard, false,
                    "the configured value was rejected; trading on the last "
                            + "value that passed validation");
        }
    }
}
