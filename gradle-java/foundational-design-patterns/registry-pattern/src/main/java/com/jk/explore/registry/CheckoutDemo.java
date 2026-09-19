package com.jk.explore.registry;

import com.jk.explore.registry.domain.DiscountPolicy;
import com.jk.explore.registry.domain.LoyaltyPolicy;
import com.jk.explore.registry.domain.Notifier;
import com.jk.explore.registry.domain.PaymentGateway;
import com.jk.explore.registry.domain.RecordingGateway;
import com.jk.explore.registry.domain.RecordingNotifier;
import com.jk.explore.registry.naive.PassedDownCheckout;
import com.jk.explore.registry.pattern.OrderDependence;
import com.jk.explore.registry.pattern.OrderDependence.NamedTest;
import com.jk.explore.registry.pattern.Registry;
import com.jk.explore.registry.pattern.RegistryCheckout;

import java.util.List;

/** Six acts. The same three collaborators as the next two projects, so all three can be compared. */
public final class CheckoutDemo {

    public static void main(String[] args) {
        System.out.println("REGISTRY — the well-known place everything is kept\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    private static void actOne() {
        System.out.println("ONE. Pass it down — through six constructors.");
        RecordingGateway gateway = new RecordingGateway();
        PassedDownCheckout checkout = new PassedDownCheckout(new LoyaltyPolicy(), gateway, new RecordingNotifier());
        System.out.println("  " + checkout.place(10_000) + ", charged " + gateway.charges());
        System.out.println("  the gateway went through Storefront, CartService, OrderCoordinator, PricingStage,");
        System.out.println("  PaymentStage and Charger. only the last one uses it. the other five forward it.");
        System.out.println("  that is real friction, and every dependency is honestly visible in a signature.\n");
    }

    private static void actTwo() {
        System.out.println("TWO. The pattern — a well-known place to ask.");
        Registry.clear();
        RecordingGateway gateway = new RecordingGateway();
        Registry.register(DiscountPolicy.class, new LoyaltyPolicy());
        Registry.register(PaymentGateway.class, gateway);
        Registry.register(Notifier.class, new RecordingNotifier());
        RegistryCheckout checkout = new RegistryCheckout();
        System.out.println("  " + checkout.place(10_000) + ", charged " + gateway.charges());
        System.out.println("  RegistryCheckout's constructor takes nothing. six constructors became none.\n");
        Registry.clear();
    }

    private static void actThree() {
        System.out.println("THREE. The bill: the dependencies are invisible.");
        Registry.clear();
        RegistryCheckout checkout = new RegistryCheckout();
        System.out.println("  new RegistryCheckout() compiled and ran. its signature says it needs nothing.");
        try {
            checkout.place(10_000);
        } catch (IllegalStateException e) {
            System.out.println("  the first call failed: " + e.getMessage());
        }
        System.out.println("  three things had to be registered first, and nothing in the class says so.\n");
    }

    private static void actFour() {
        System.out.println("FOUR. The bill: a test fails because of the order the tests ran in.");
        NamedTest usesTheRealGateway = new NamedTest("checkoutChargesTheRealGateway", () -> {
            Registry.register(DiscountPolicy.class, new LoyaltyPolicy());
            Registry.register(Notifier.class, new RecordingNotifier());
            if (!Registry.contents().contains("PaymentGateway")) {
                Registry.register(PaymentGateway.class, new RecordingGateway());
            }
            long charged = ((RecordingGateway) Registry.get(PaymentGateway.class)).charges().size();
            new RegistryCheckout().place(10_000);
            long after = ((RecordingGateway) Registry.get(PaymentGateway.class)).charges().size();
            if (after - charged != 1 || after != 1) {
                throw new AssertionError("expected exactly one charge in total, saw " + after);
            }
        });
        NamedTest leavesAGatewayBehind = new NamedTest("refundTestLeavesItsGatewayBehind", () -> {
            RecordingGateway g = new RecordingGateway();
            g.charge(500);
            Registry.register(PaymentGateway.class, g);
        });
        System.out.println("  order one: " + OrderDependence.run(List.of(usesTheRealGateway, leavesAGatewayBehind)));
        System.out.println("  order two: " + OrderDependence.run(List.of(leavesAGatewayBehind, usesTheRealGateway)));
        System.out.println("  neither test changed. the order did. that is the symptom teams meet first.\n");
    }

    private static void actFive() {
        System.out.println("FIVE. The bill: what is in it, right now?");
        Registry.clear();
        System.out.println("  at start-up:            " + Registry.contents());
        Registry.register(DiscountPolicy.class, new LoyaltyPolicy());
        System.out.println("  after one class ran:    " + Registry.contents());
        Registry.register(PaymentGateway.class, new RecordingGateway());
        Registry.register(Notifier.class, new RecordingNotifier());
        System.out.println("  after two more:         " + Registry.contents());
        System.out.println("  that answer is not in any one file. it depends on what ran, and in what order.");
        System.out.println("  it is also a static map shared by every thread, so thread safety is now a question.\n");
        Registry.clear();
    }

    private static void actSix() {
        System.out.println("SIX. The verdict.");
        System.out.println("  use a registry narrowly: for a very few things that are truly application-wide,");
        System.out.println("  set up once at start-up and never changed. not for collaborators that vary or need testing.");
        System.out.println("  the fix for what it hides is a middleman that can find and create things: a service locator.");
        System.out.println("  where you have met this: System.getProperties(), a static Logger factory, Locale.getDefault().");
    }
}
