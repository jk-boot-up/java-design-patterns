package com.jk.explore.strategyspring;

import org.springframework.beans.factory.NoUniqueBeanDefinitionException;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

@SpringBootApplication
public class ShippingApplication {

    static final Shipment LIGHT = new Shipment(300, 20, 2000);
    static final Shipment MIDDLE = new Shipment(1000, 150, 4900);
    static final Shipment HEAVY = new Shipment(5000, 400, 8000);

    static SpringApplicationBuilder builder() {
        return new SpringApplicationBuilder(ShippingApplication.class).web(WebApplicationType.NONE);
    }

    static String pounds(long pence) {
        return String.format("%d.%02d", pence / 100, pence % 100);
    }

    public static void main(String[] args) {
        try (ConfigurableApplicationContext ctx = builder().run()) {
            CheckoutService checkout = ctx.getBean(CheckoutService.class);

            System.out.println("ONE. Spring finds the strategies.");
            System.out.println("  rules found: " + checkout.ruleNames() + ".");
            System.out.println("  the keys are bean names, chosen in the @Component annotations.");

            System.out.println("TWO. The same shipments, every rule.");
            for (String name : checkout.ruleNames()) {
                System.out.println("  " + String.format("%-18s", name)
                        + " light " + pounds(checkout.quote(name, LIGHT))
                        + "  middle " + pounds(checkout.quote(name, MIDDLE))
                        + "  heavy " + pounds(checkout.quote(name, HEAVY)));
            }
            try {
                checkout.quote("teleport", LIGHT);
            } catch (IllegalArgumentException e) {
                System.out.println("  a name at run time that is unknown: " + e.getMessage());
            }
        }

        System.out.println("THREE. Configuration chooses.");
        try (ConfigurableApplicationContext ctx = builder().properties("shipping.rule=distance").run()) {
            SelectedShipping chosen = ctx.getBean(SelectedShipping.class);
            System.out.println("  shipping.rule=" + chosen.name() + ": the heavy shipment costs " + pounds(chosen.cost(HEAVY)) + ".");
        }
        try (ConfigurableApplicationContext ctx = builder().properties("shipping.rule=teleport").run()) {
            System.out.println("  unexpectedly started");
        } catch (Exception e) {
            Throwable root = e;
            while (root.getCause() != null) {
                root = root.getCause();
            }
            System.out.println("  shipping.rule=teleport: the application does not start. " + root.getMessage());
        }

        System.out.println("FOUR. Four beans, one interface.");
        try (ConfigurableApplicationContext ctx = builder()
                .initializers(c -> ((org.springframework.context.support.GenericApplicationContext) c).registerBean(NeedsOneRule.class))
                .run()) {
            System.out.println("  unexpectedly started");
        } catch (Exception e) {
            Throwable root = e;
            while (root.getCause() != null) {
                root = root.getCause();
            }
            System.out.println("  a class that asks for a single ShippingCostRule: "
                    + (root instanceof NoUniqueBeanDefinitionException n ? "expected a single bean but found " + n.getNumberOfBeansFound() + "." : root.getMessage()));
        }

        System.out.println("FIVE. A fifth rule.");
        try (ConfigurableApplicationContext ctx = builder()
                .initializers(c -> ((org.springframework.context.support.GenericApplicationContext) c).registerBean("express", ExpressRule.class))
                .run()) {
            CheckoutService checkout = ctx.getBean(CheckoutService.class);
            System.out.println("  rules found: " + checkout.ruleNames() + ".");
            System.out.println("  express quotes the heavy shipment at " + pounds(checkout.quote("express", HEAVY)) + ". CheckoutService did not change.");
        }

        System.out.println("SIX. A default when nobody chooses.");
        try (ConfigurableApplicationContext ctx = builder()
                .initializers(c -> {
                    c.addBeanFactoryPostProcessor(bf -> bf.getBeanDefinition("flat").setPrimary(true));
                    ((org.springframework.context.support.GenericApplicationContext) c).registerBean(NeedsOneRule.class);
                })
                .run()) {
            System.out.println("  with the flat rule marked primary, the same class starts, and prices the heavy shipment at "
                    + pounds(ctx.getBean(NeedsOneRule.class).cost(HEAVY)) + ".");
            System.out.println("  the map still holds all four: " + ctx.getBean(CheckoutService.class).ruleNames() + ".");
        }
    }
}
