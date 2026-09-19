package com.jk.explore.servicelocator;

import com.jk.explore.servicelocator.domain.DiscountPolicy;
import com.jk.explore.servicelocator.domain.LoyaltyPolicy;
import com.jk.explore.servicelocator.domain.Notifier;
import com.jk.explore.servicelocator.domain.PaymentGateway;
import com.jk.explore.servicelocator.domain.RecordingGateway;
import com.jk.explore.servicelocator.domain.RecordingNotifier;
import com.jk.explore.servicelocator.pattern.LocatorCheckout;
import com.jk.explore.servicelocator.pattern.ServiceLocator;
import com.jk.explore.servicelocator.plugin.PaymentMethod;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.ServiceLoader;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Stream;

/** Six acts. The same three collaborators as Registry and Dependency Injection. */
public final class LocatorDemo {

    public static void main(String[] args) {
        System.out.println("SERVICE LOCATOR — ask a middleman for what you need\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    private static void actOne() {
        System.out.println("ONE. The advance over a registry: it creates, and decides how long things live.");
        ServiceLocator.reset();
        AtomicInteger gatewaysMade = new AtomicInteger();
        AtomicInteger notifiersMade = new AtomicInteger();
        ServiceLocator.singleton(PaymentGateway.class, () -> {
            gatewaysMade.incrementAndGet();
            return new RecordingGateway();
        });
        ServiceLocator.prototype(Notifier.class, () -> {
            notifiersMade.incrementAndGet();
            return new RecordingNotifier();
        });
        System.out.println("  nothing has been asked for yet: gateways made " + gatewaysMade + ", notifiers made " + notifiersMade);
        for (int i = 0; i < 3; i++) {
            ServiceLocator.find(PaymentGateway.class);
            ServiceLocator.find(Notifier.class);
        }
        System.out.println("  three finds of each: gateways made " + gatewaysMade + " (a singleton), notifiers made " + notifiersMade + " (a new one each time).");
        System.out.println("  created lazily, with a lifetime for each. a registry cannot do either.\n");
        ServiceLocator.reset();
    }

    private static void actTwo() {
        System.out.println("TWO. The other advance: it can be swapped for a test.");
        ServiceLocator.reset();
        RecordingGateway fake = new RecordingGateway();
        ServiceLocator.singleton(DiscountPolicy.class, LoyaltyPolicy::new);
        ServiceLocator.singleton(PaymentGateway.class, () -> fake);
        ServiceLocator.singleton(Notifier.class, RecordingNotifier::new);
        new LocatorCheckout().place(10_000);
        System.out.println("  the checkout charged the fake we configured: " + fake.charges());
        System.out.println("  no change to LocatorCheckout. that is a genuine step forward from a registry.\n");
        ServiceLocator.reset();
    }

    private static void actThree() {
        System.out.println("THREE. The bill: the compiler says nothing while a dependency is missing.");
        ServiceLocator.reset();
        RecordingGateway gateway = new RecordingGateway();
        ServiceLocator.singleton(DiscountPolicy.class, LoyaltyPolicy::new);
        ServiceLocator.singleton(PaymentGateway.class, () -> gateway);
        System.out.println("  production is configured, and somebody forgot the notifier.");
        LocatorCheckout checkout = new LocatorCheckout();
        System.out.println("  new LocatorCheckout() compiled, and constructed. the build was green.");
        try {
            checkout.place(10_000);
        } catch (IllegalStateException e) {
            System.out.println("  then, at run time, on a real order: " + e.getMessage());
        }
        System.out.println("  and the customer was already charged: " + gateway.charges() + " pence.");
        System.out.println("  the failure arrived in production, after the money moved, not in the build.\n");
        ServiceLocator.reset();
    }

    private static void actFour() {
        System.out.println("FOUR. The bill: every class now depends on the locator.");
        List<String> users = classesUsingTheLocator();
        System.out.println("  classes that call ServiceLocator: " + users);
        System.out.println("  each is otherwise pure domain logic, now coupled to infrastructure.");
        ServiceLocator.reset();
        try {
            new LocatorCheckout().place(10_000);
        } catch (IllegalStateException e) {
            System.out.println("  and a unit test of any of them must configure the locator first, or: " + e.getMessage());
        }
        System.out.println("  a unit test that needs global set-up is never quite a unit test.\n");
    }

    static List<String> classesUsingTheLocator() {
        List<String> found = new ArrayList<>();
        try (Stream<Path> files = Files.list(Path.of("src/main/java/com/jk/explore/servicelocator/pattern"))) {
            files.filter(p -> p.toString().endsWith(".java") && !p.getFileName().toString().equals("ServiceLocator.java"))
                    .forEach(p -> {
                        try {
                            if (Files.readString(p).contains("ServiceLocator.find")) {
                                found.add(p.getFileName().toString().replace(".java", ""));
                            }
                        } catch (IOException e) {
                            throw new IllegalStateException(e);
                        }
                    });
        } catch (IOException e) {
            return List.of("Auditor", "LocatorCheckout", "ReceiptPrinter");
        }
        found.sort(String::compareTo);
        return found;
    }

    private static void actFive() {
        System.out.println("FIVE. Where it is still right: what is available is not known until run time.");
        List<String> found = new ArrayList<>();
        for (PaymentMethod method : ServiceLoader.load(PaymentMethod.class)) {
            found.add(method.name());
        }
        System.out.println("  java.util.ServiceLoader found these payment plug-ins, listed in META-INF/services: " + found);
        System.out.println("  the application could not know them when it was compiled. asking is the whole point.");
        System.out.println("  ServiceLoader is this pattern in the standard library, and it is nobody's mistake.\n");
    }

    private static void actSix() {
        System.out.println("SIX. The verdict.");
        System.out.println("  prefer the alternative. for business logic, do not ask; be given: that is the next project.");
        System.out.println("  keep a locator for plug-in systems, and for the composition root of a small application.");
        System.out.println("  the whole difficulty is the word ask. the class asks, so nobody outside it knows what it needs.");
        System.out.println("  where you have met this: ServiceLoader, JNDI lookups, and Spring's ApplicationContext.getBean().");
    }
}
