package com.jk.explore.plugin;

/**
 * Without the pattern: every place that needs a service picks the implementation itself, from the environment name.
 *
 * <p>When "staging" was added, the payment choice was updated and the email
 * choice was missed, so staging fell through to the real emailer.
 */
public final class ScatteredChoices {

    public static Services.PaymentGateway gateway(String env) {
        if (env.equals("prod")) {
            return new Implementations.CardGateway();
        }
        return new Implementations.FakeGateway();
    }

    public static Services.Emailer emailer(String env) {
        if (env.equals("dev")) {
            return new Implementations.SandboxEmailer();
        }
        return new Implementations.SmtpEmailer();
    }

    private ScatteredChoices() {
    }
}
