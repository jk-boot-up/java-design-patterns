package com.jk.explore.secrets;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

/**
 * The five acts: a key in the code, a key in the manager, rotation without a rebuild,
 * responding to a leak, and the bill.
 */
public final class SecretsManagerDemo {

    static final long MINUTE = 60;

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. The payment key is written in the code.");
        out.add("  key " + HardCodedConfig.PAYMENT_KEY + " is built into " + HardCodedConfig.BUILT_INTO.length
                + " services: " + String.join(", ", HardCodedConfig.BUILT_INTO));
        out.add("  everyone who can read the repository can read it: " + HardCodedConfig.PEOPLE_WITH_REPO_ACCESS
                + " people, and every old copy of it");
        out.add("  changing it means editing, rebuilding and redeploying " + HardCodedConfig.BUILT_INTO.length + " services");

        out.add("");
        out.add("TWO. The key lives in a secrets manager.");
        SecretsManager manager = new SecretsManager();
        PaymentProvider provider = new PaymentProvider();
        manager.store("payment-key", "pay-key-v1", Set.of("checkout", "refunds", "subscriptions"));
        provider.enable("pay-key-v1");
        CachedSecret checkoutKey = new CachedSecret(manager, "checkout", "payment-key", 5 * MINUTE);
        out.add("  checkout reads it at run time and charges: " + provider.charge(checkoutKey.get(0), "20.00"));
        try {
            manager.read("catalog", "payment-key");
        } catch (SecurityException e) {
            out.add("  catalog asks for it: " + e.getMessage());
        }
        out.add("  the key is in no source file and no build");

        out.add("");
        out.add("THREE. Rotating the key, with no rebuild.");
        provider.enable("pay-key-v2");
        int version = manager.rotate("payment-key", "pay-key-v2");
        out.add("  at minute 0 the key is rotated to version " + version + "; the provider accepts both for now");
        out.add("  minute 2, checkout still uses its cached key: " + checkoutKey.get(2 * MINUTE)
                + " -> " + provider.charge(checkoutKey.get(2 * MINUTE), "20.00"));
        out.add("  minute 5, the cache refreshes:              " + checkoutKey.get(5 * MINUTE)
                + " -> " + provider.charge(checkoutKey.get(5 * MINUTE), "20.00"));
        provider.cancel("pay-key-v1");
        out.add("  minute 10, version 1 is cancelled; checkout: " + provider.charge(checkoutKey.get(10 * MINUTE), "20.00"));

        out.add("");
        out.add("FOUR. The key leaks: rotate and cancel at once.");
        provider.enable("pay-key-v3");
        manager.rotate("payment-key", "pay-key-v3");
        provider.cancel("pay-key-v2");
        out.add("  the leaked key, used by an attacker: " + provider.charge("pay-key-v2", "999.00"));
        out.add("  checkout, its cache still holding version 2: " + provider.charge(checkoutKey.get(11 * MINUTE), "20.00"));
        out.add("  so on a refusal it fetches again at once:    " + checkoutKey.refresh(11 * MINUTE) + " -> "
                + provider.charge(checkoutKey.get(11 * MINUTE), "20.00"));
        out.add("  no code change, no rebuild, no redeploy");

        out.add("");
        out.add("FIVE. The bill: a service every other service now depends on.");
        out.add("  " + manager.audit().size() + " reads logged; e.g. \"" + manager.audit().get(1) + "\"");
        out.add("  if the manager is down when a service starts, it cannot get its keys");
        out.add("  and each service still needs one first credential to reach the manager: give it a platform identity");
        return out;
    }

    private SecretsManagerDemo() {
    }
}
