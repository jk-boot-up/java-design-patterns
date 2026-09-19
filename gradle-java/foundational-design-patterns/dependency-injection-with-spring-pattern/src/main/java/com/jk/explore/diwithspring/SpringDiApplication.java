package com.jk.explore.diwithspring;

import com.jk.explore.diwithspring.app.CheckoutService;
import com.jk.explore.diwithspring.app.Storefront;
import com.jk.explore.diwithspring.container.Chicken;
import com.jk.explore.diwithspring.container.Egg;
import com.jk.explore.diwithspring.domain.LoyaltyPolicy;
import com.jk.explore.diwithspring.domain.RecordingGateway;
import com.jk.explore.diwithspring.domain.RecordingNotifier;
import com.jk.explore.diwithspring.forms.FieldInjectedCheckout;
import org.springframework.beans.factory.BeanCreationException;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

import java.util.Arrays;
import java.util.List;

/**
 * Six acts. The partner project, Dependency Injection, wired this application
 * by hand in nine lines and wrote a small container. Here the same classes, with
 * one annotation added to each, are wired by Spring Boot's container.
 */
@SpringBootApplication
public class SpringDiApplication {

    public static void main(String[] args) {
        System.out.println("DEPENDENCY INJECTION WITH SPRING — recognise the wiring\n");
        actOne(args);
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix(args);
    }

    private static void actOne(String[] args) {
        System.out.println("ONE. The same graph, with no wiring code.");
        try (ConfigurableApplicationContext context = SpringApplication.run(SpringDiApplication.class, args)) {
            RecordingGateway gateway = context.getBean(RecordingGateway.class);
            context.getBean(Storefront.class).order(10_000);
            System.out.println("  Wiring.build() is gone. Spring built the graph from the constructors.");
            System.out.println("  charged " + gateway.charges() + ", messages sent " + context.getBean(RecordingNotifier.class).sent().size()
                    + ", exactly as by hand.\n");
        }
    }

    private static void actTwo() {
        System.out.println("TWO. What each annotation replaced.");
        try (AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext(
                LoyaltyPolicy.class, RecordingGateway.class, RecordingNotifier.class,
                CheckoutService.class, com.jk.explore.diwithspring.app.ReceiptPrinter.class,
                com.jk.explore.diwithspring.app.Auditor.class, Storefront.class)) {
            List<String> names = Arrays.stream(context.getBeanDefinitionNames()).map(n -> context.getType(n).getSimpleName())
                    .filter(n -> !n.contains("Processor") && !n.contains("Factory") && !n.contains("Registry")).sorted().toList();
            System.out.println("  by hand, in the partner project:  new LoyaltyPolicy(), new CheckoutService(policy, gateway, notifier), ...");
            System.out.println("  here: @Component on each class, and the constructor parameters say the rest.");
            System.out.println("  beans Spring built: " + names);
            System.out.println("  one annotation per class replaced " + names.size() + " lines of new. the constructors are untouched.\n");
        }
    }

    private static void actThree() {
        System.out.println("THREE. A bean that is missing: a real Spring start-up failure.");
        try (AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext()) {
            context.register(LoyaltyPolicy.class, RecordingGateway.class, CheckoutService.class);
            context.refresh();
        } catch (BeanCreationException e) {
            System.out.println("  " + e.getClass().getSimpleName() + ", when the context starts:");
            System.out.println("  " + firstSentence(e.getMessage()));
        }
        System.out.println("  the same failure as the hand-written container, and better than a locator's: at start-up, not on the first order.");
        System.out.println("  still not at compile time.\n");
    }

    private static void actFour() {
        System.out.println("FOUR. A circular dependency.");
        try (AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext()) {
            context.register(Chicken.class, Egg.class);
            context.refresh();
        } catch (BeanCreationException e) {
            Throwable root = e;
            while (root.getCause() != null) {
                root = root.getCause();
            }
            System.out.println("  " + root.getClass().getSimpleName() + ": " + firstSentence(root.getMessage()));
        }
        System.out.println("  since Spring 6 a cycle is refused by default, at start-up.\n");
    }

    private static void actFive() {
        System.out.println("FIVE. Field injection: Spring can fill it, nothing else can.");
        FieldInjectedCheckout invalid = new FieldInjectedCheckout();
        try {
            invalid.place(10_000);
        } catch (NullPointerException e) {
            System.out.println("  new FieldInjectedCheckout() compiled, and placing an order threw NullPointerException.");
        }
        try (AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext(
                LoyaltyPolicy.class, RecordingGateway.class, RecordingNotifier.class, FieldInjectedCheckout.class)) {
            System.out.println("  inside a Spring context it works: " + context.getBean(FieldInjectedCheckout.class).place(10_000));
        }
        System.out.println("  Spring's own guidance is constructor injection, for the reason above.\n");
    }

    private static void actSix(String[] args) {
        System.out.println("SIX. What the magic costs, and the verdict.");
        long handStart = System.nanoTime();
        for (int i = 0; i < 1_000; i++) {
            new Storefront(new CheckoutService(new LoyaltyPolicy(), new RecordingGateway(), new RecordingNotifier()),
                    new com.jk.explore.diwithspring.app.ReceiptPrinter(new RecordingNotifier()),
                    new com.jk.explore.diwithspring.app.Auditor(new RecordingNotifier()));
        }
        long handNanos = (System.nanoTime() - handStart) / 1_000;
        long springStart = System.nanoTime();
        new AnnotationConfigApplicationContext(LoyaltyPolicy.class, RecordingGateway.class, RecordingNotifier.class,
                CheckoutService.class, com.jk.explore.diwithspring.app.ReceiptPrinter.class,
                com.jk.explore.diwithspring.app.Auditor.class, Storefront.class).close();
        long springMillis = (System.nanoTime() - springStart) / 1_000_000;
        System.out.println("  building the graph by hand: about " + handNanos + " nanoseconds each. a Spring context: about " + springMillis + " ms, once.");
        System.out.println("  the cost is real and paid once at start-up. timings vary by machine.");
        System.out.println("  the verdict is unchanged: constructor injection, by hand until the wiring hurts, then a container.");
        System.out.println("  Spring did not add the idea. it removed the typing.");
    }

    private static String firstSentence(String message) {
        String flat = message.replace('\n', ' ');
        return flat.length() > 170 ? flat.substring(0, 170) + "..." : flat;
    }
}
