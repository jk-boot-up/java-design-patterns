package com.jk.explore.secrets;

/**
 * Before: the payment key written into configuration that is committed with the code
 * and copied into every service's build.
 */
public final class HardCodedConfig {

    public static final String PAYMENT_KEY = "pay-key-v1";
    public static final String[] BUILT_INTO = {"checkout", "refunds", "subscriptions"};
    public static final int PEOPLE_WITH_REPO_ACCESS = 40;

    private HardCodedConfig() {
    }
}
