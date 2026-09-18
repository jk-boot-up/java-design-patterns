package com.jk.explore.externalisedconfig.real.checkout;

import jakarta.validation.constraints.DecimalMax;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotNull;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.validation.annotation.Validated;

import java.math.BigDecimal;

/**
 * The externalised settings, and the guards that come with them.
 *
 * <p>This class is the Tier 2 answer to the four guards the constant used to
 * get for free, and it is worth reading one annotation at a time.
 *
 * <p><strong>{@code @ConfigurationProperties}</strong> binds
 * {@code delivery.freeOver} and {@code delivery.standard} from wherever the
 * environment got them. In this deployment that is the config server, but the
 * class does not know or care — the same binding works against a YAML file, an
 * environment variable or a command-line argument.
 *
 * <p><strong>{@code @RefreshScope}</strong> is the one that earns its keep.
 * Without it, this bean is built once at startup and holds the value it was
 * given for the life of the process, which would put us back to needing a
 * restart. With it, the bean is thrown away and rebuilt the next time anybody
 * asks for it after a {@code POST /actuator/refresh} — so the change reaches
 * production without the deployment.
 *
 * <p><strong>{@code @Validated} with {@code @DecimalMin} and
 * {@code @DecimalMax}</strong> is the declared range. Tier 1 made the argument
 * that a constant gets four guards free — the compiler, a reviewer, version
 * control and a revert — and that moving the value outside throws all four
 * away. This is the second of the four bought back. A threshold of {@code -1}
 * does not silently give the shop away; binding fails, the refresh is
 * rejected, and the previous value stays in force.
 *
 * <p>Note what is <em>not</em> here: no default of fifty pounds hard-coded as
 * a fallback. A default in the code is the constant creeping back in, and the
 * first time the two disagree nobody can tell which one is in force. If the
 * config server has nothing to say about {@code delivery.freeOver}, this
 * service refuses to start, loudly, rather than quoting a number that no
 * record anywhere explains.
 */
@Validated
@RefreshScope
@ConfigurationProperties(prefix = "delivery")
public class DeliverySettings {

    /**
     * The goods total at which delivery becomes free.
     *
     * <p>The range is the interesting part. Five pounds and two hundred pounds
     * are not arbitrary: below five, essentially every basket ships free and
     * the shop is giving away delivery; above two hundred, essentially none
     * does and the offer may as well not exist. Both ends are a mistake
     * somebody could plausibly type, which is the test of whether a range is
     * worth declaring.
     */
    @NotNull
    @DecimalMin("5.00")
    @DecimalMax("200.00")
    private BigDecimal freeOver;

    /** What delivery costs when the basket falls short of the threshold. */
    @NotNull
    @DecimalMin("0.00")
    @DecimalMax("50.00")
    private BigDecimal standard;

    public BigDecimal getFreeOver() {
        return freeOver;
    }

    public void setFreeOver(BigDecimal freeOver) {
        this.freeOver = freeOver;
    }

    public BigDecimal getStandard() {
        return standard;
    }

    public void setStandard(BigDecimal standard) {
        this.standard = standard;
    }
}
