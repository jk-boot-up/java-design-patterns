package com.jk.explore.dependencyinjection.wiring;

import com.jk.explore.dependencyinjection.app.Auditor;
import com.jk.explore.dependencyinjection.app.CheckoutService;
import com.jk.explore.dependencyinjection.app.ReceiptPrinter;
import com.jk.explore.dependencyinjection.app.Storefront;
import com.jk.explore.dependencyinjection.domain.LoyaltyPolicy;
import com.jk.explore.dependencyinjection.domain.RecordingGateway;
import com.jk.explore.dependencyinjection.domain.RecordingNotifier;

/**
 * <strong>The whole application, wired by hand.</strong> Everything between
 * the two marker comments is what a container does for you. It is about ten
 * lines, and it is plain Java: a container is an optimisation of something you
 * could write yourself.
 */
public final class Wiring {

    private Wiring() {
    }

    /** What the wiring built, so a caller can look inside. */
    public record Application(Storefront storefront, RecordingGateway gateway, RecordingNotifier notifier) {
    }

    public static Application build() {
        // wiring begins
        LoyaltyPolicy policy = new LoyaltyPolicy();
        RecordingGateway gateway = new RecordingGateway();
        RecordingNotifier notifier = new RecordingNotifier();

        CheckoutService checkout = new CheckoutService(policy, gateway, notifier);
        ReceiptPrinter printer = new ReceiptPrinter(notifier);
        Auditor auditor = new Auditor(notifier);

        Storefront storefront = new Storefront(checkout, printer, auditor);
        // wiring ends
        return new Application(storefront, gateway, notifier);
    }
}
