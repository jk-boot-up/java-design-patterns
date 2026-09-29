package com.jk.explore.secretsopenbao;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts, against a real OpenBao server started and stopped by this program.
 */
public final class OpenBaoSecretsDemo {

    static final String HARD_CODED = "pay-key-v1";

    public static void main(String[] args) throws Exception {
        if (!OpenBao.containerRuntimeAvailable()) {
            System.out.println(OpenBao.NO_RUNTIME_ADVICE);
            return;
        }
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();

        out.add("ONE. The payment key is written in the code.");
        out.add("  PAYMENT_KEY = \"" + HARD_CODED + "\", built into checkout, refunds and subscriptions");
        out.add("  everyone who can read the repository can read it, and every old copy of it");

        try (OpenBao bao = new OpenBao()) {
            try {
                bao.start();
            } catch (RuntimeException e) {
                out.add(OpenBao.WOULD_NOT_START_ADVICE);
                return out;
            }
            Secrets secrets = new Secrets(bao);

            out.add("");
            out.add("TWO. The key lives in OpenBao; each service has its own token and policy.");
            secrets.storePaymentKey("pay-key-v1");
            secrets.writePaymentsPolicy();
            String checkout = secrets.tokenFor("payments");
            String catalog = secrets.tokenFor("default");
            OpenBao.Reply c = secrets.read(checkout);
            out.add("  checkout's token, policy \"payments\": HTTP " + c.status() + ", key " + c.field("value"));
            OpenBao.Reply k = secrets.read(catalog);
            out.add("  catalog's token, no such policy:     HTTP " + k.status() + ", " + (k.body().contains("permission denied")
                    ? "permission denied" : k.body()));

            out.add("");
            out.add("THREE. Rotating the key: a new version, no rebuild.");
            int version = secrets.storePaymentKey("pay-key-v2");
            out.add("  written as version " + version + "; checkout now reads: " + secrets.read(checkout).field("value"));
            out.add("  version 1 is kept, for a grace period: " + secrets.readVersion(checkout, 1).field("value"));

            out.add("");
            out.add("FOUR. Checkout's token leaks: revoke it at once.");
            secrets.revoke(checkout);
            OpenBao.Reply leaked = secrets.read(checkout);
            out.add("  the leaked token, used by an attacker: HTTP " + leaked.status() + ", "
                    + (leaked.body().contains("permission denied") ? "permission denied" : leaked.body()));
            String fresh = secrets.tokenFor("payments");
            out.add("  checkout gets a new token: HTTP " + secrets.read(fresh).status() + ", key " + secrets.read(fresh).field("value"));
            out.add("  and the payment key itself can be rotated too, as in act three");

            out.add("");
            out.add("FIVE. The bill.");
            out.add("  every service needs one first credential to get a token: use the platform's identity, such as AppRole or Kubernetes auth");
            out.add("  this server runs in development mode: in memory, unsealed, with a root token; production needs storage, unsealing and");
            out.add("  high availability, because every service now depends on it to start");
        }
        return out;
    }

    private OpenBaoSecretsDemo() {
    }
}
