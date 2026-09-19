package com.jk.explore.registryspring;

import com.jk.explore.registryspring.app.InjectedCheckout;
import com.jk.explore.registryspring.app.LocatorStyleCheckout;
import com.jk.explore.registryspring.app.Settings;
import com.jk.explore.registryspring.domain.LoyaltyPolicy;
import com.jk.explore.registryspring.domain.Notifier;
import com.jk.explore.registryspring.domain.PaymentGateway;
import com.jk.explore.registryspring.domain.RecordingGateway;
import com.jk.explore.registryspring.domain.RecordingNotifier;
import com.jk.explore.registryspring.domain.SmsNotifier;
import org.springframework.beans.BeansException;
import org.springframework.beans.factory.NoUniqueBeanDefinitionException;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.core.env.Environment;

import java.util.Arrays;

/**
 * Six acts. The partner project, Registry, built a static registry by hand and
 * listed its costs. Spring's {@code ApplicationContext} is a registry too, built
 * far better, and this project shows what it fixes and what it leaves.
 */
@SpringBootApplication
public class RegistrySpringApplication {

    public static void main(String[] args) {
        System.out.println("REGISTRY WITH SPRING — the context is a registry you did not write\n");
        try (ConfigurableApplicationContext context = SpringApplication.run(RegistrySpringApplication.class, args)) {
            actOne(context);
            actTwo(context);
            actThree();
            actFour(context);
            actFive();
            actSix();
        }
    }

    private static void actOne(ConfigurableApplicationContext context) {
        System.out.println("ONE. The ApplicationContext is the registry.");
        System.out.println("  Registry.get(PaymentGateway.class) in the partner project is context.getBean(PaymentGateway.class) here: "
                + context.getBean(PaymentGateway.class).getClass().getSimpleName());
        System.out.println("  registered by declaration: @Component on a class. beans of type PaymentGateway: "
                + Arrays.toString(context.getBeanNamesForType(PaymentGateway.class)));
        System.out.println("  no static map, no register() calls scattered through the code, and a missing bean fails at start-up.\n");
    }

    private static void actTwo(ConfigurableApplicationContext context) {
        System.out.println("TWO. Used well, nobody calls it. Used badly, it is the hand-built registry again.");
        System.out.println("  InjectedCheckout is given its collaborators: " + context.getBean(InjectedCheckout.class).place(10_000));
        System.out.println("  LocatorStyleCheckout calls context.getBean three times: " + context.getBean(LocatorStyleCheckout.class).place(10_000));
        System.out.println("  same result. but LocatorStyleCheckout's constructor takes nothing, and its dependencies are invisible again.");
        try {
            new LocatorStyleCheckout().place(10_000);
        } catch (NullPointerException e) {
            System.out.println("  new LocatorStyleCheckout() compiled, and threw NullPointerException: it needs Spring to hand it the context.\n");
        }
    }

    private static void actThree() {
        System.out.println("THREE. The failure of its own: shared state, through the context cache.");
        System.out.println("  Spring's test support caches a context and reuses it across tests with the same configuration.");
        try (ConfigurableApplicationContext shared = SpringApplication.run(RegistrySpringApplication.class)) {
            RecordingGateway gateway = shared.getBean(RecordingGateway.class);
            shared.getBean(InjectedCheckout.class).place(10_000);
            System.out.println("  test A ran on the shared context and charged once. the gateway is a singleton, so it remembers: " + gateway.charges());
            RecordingGateway seenByB = shared.getBean(RecordingGateway.class);
            System.out.println("  test B, on the same cached context, starts by expecting a clean gateway. it sees: " + seenByB.charges());
            System.out.println("  that is the hand-built registry's order-dependent test failure, in Spring. the tests in this project prove it.");
        }
        try (ConfigurableApplicationContext fresh = SpringApplication.run(RegistrySpringApplication.class)) {
            System.out.println("  a fresh context (what @DirtiesContext gives) sees: " + fresh.getBean(RecordingGateway.class).charges()
                    + ", at the price of starting Spring again.\n");
        }
    }

    private static void actFour(ConfigurableApplicationContext context) {
        System.out.println("FOUR. The Environment is a registry of strings.");
        Environment env = context.getEnvironment();
        System.out.println("  checkout.currency = " + env.getProperty("checkout.currency"));
        System.out.println("  checkout.curency (a typo) = " + env.getProperty("checkout.curency") + ", where the right answer was GBP. no error, no warning.");
        try (AnnotationConfigApplicationContext broken = new AnnotationConfigApplicationContext()) {
            broken.getEnvironment().getPropertySources().addFirst(
                    new org.springframework.core.env.MapPropertySource("empty", java.util.Map.of()));
            broken.register(org.springframework.context.support.PropertySourcesPlaceholderConfigurer.class, Settings.class);
            broken.refresh();
        } catch (BeansException e) {
            Throwable root = e;
            while (root.getCause() != null) {
                root = root.getCause();
            }
            System.out.println("  a required @Value with the same typo fails when the context starts:");
            System.out.println("  " + root.getMessage());
        }
        System.out.println("  the untyped lookup is silent; the injected one is not.\n");
    }

    private static void actFive() {
        System.out.println("FIVE. Asking by type is ambiguous the moment there are two.");
        try (AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext(
                RecordingNotifier.class, SmsNotifier.class)) {
            try {
                ctx.getBean(Notifier.class);
            } catch (NoUniqueBeanDefinitionException e) {
                System.out.println("  context.getBean(Notifier.class) with two Notifiers: " + e.getClass().getSimpleName());
                System.out.println("  found: " + e.getBeanNamesFound() + ". a run-time error at the call site, not a compile error.");
            }
        }
        System.out.println();
    }

    private static void actSix() {
        System.out.println("SIX. The verdict.");
        System.out.println("  Spring's context is the registry done well: declared, checked at start-up, and mostly never called.");
        System.out.println("  keep calling getBean to main, to tests and to framework glue. in business code, inject instead.");
        System.out.println("  a getBean inside a business class is a Service Locator, with all its costs.");
        System.out.println("  and keep singleton state out of anything a test shares.");
    }
}
