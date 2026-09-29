package com.jk.explore.plugin;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: choices scattered in code, plugins from configuration, a new environment, a bad entry caught at startup, and the bill.
 */
public final class PluginDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. Each place picks its own implementation from the environment name.");
        Checkout.placeOrder(ScatteredChoices.gateway("staging"), ScatteredChoices.emailer("staging"))
                .forEach(line -> out.add("  staging: " + line));
        out.add("  \"staging\" was added to the payment choice and missed in the email choice");

        out.add("");
        out.add("TWO. Plugins: a configuration file per environment names the classes.");
        for (String env : new String[] {"dev", "prod"}) {
            PluginFactory f = new PluginFactory(env);
            Checkout.placeOrder(f.get(Services.PaymentGateway.class), f.get(Services.Emailer.class))
                    .forEach(line -> out.add("  " + env + ": " + line));
        }
        out.add("  Checkout names only the interfaces; one factory creates the classes");

        out.add("");
        out.add("THREE. A new environment is a new file, not new code.");
        PluginFactory staging = new PluginFactory("staging");
        Checkout.placeOrder(staging.get(Services.PaymentGateway.class), staging.get(Services.Emailer.class))
                .forEach(line -> out.add("  staging: " + line));
        out.add("  plugins-staging.properties: 2 lines; no Java changed");

        out.add("");
        out.add("FOUR. A bad entry is caught when the shop starts.");
        PluginFactory demo = new PluginFactory("demo");
        demo.check(Services.PaymentGateway.class, Services.Emailer.class).forEach(p -> out.add("  startup check: " + p));
        out.add("  found before the first customer, not by the first customer");

        out.add("");
        out.add("FIVE. The bill: the compiler cannot see the wiring.");
        out.add("  a misspelt class name is a startup error, not a compile error");
        out.add("  \"find usages\" of SandboxEmailer shows nothing: it is only named in text files");
        return out;
    }

    static String pounds(long pence) {
        return String.format("£%d.%02d", pence / 100, pence % 100);
    }

    private PluginDemo() {
    }
}
