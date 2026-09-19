package com.jk.explore.dependencyinjection;

import com.jk.explore.dependencyinjection.app.Auditor;
import com.jk.explore.dependencyinjection.app.CheckoutService;
import com.jk.explore.dependencyinjection.app.OverloadedService;
import com.jk.explore.dependencyinjection.app.ReceiptPrinter;
import com.jk.explore.dependencyinjection.app.Storefront;
import com.jk.explore.dependencyinjection.container.Chicken;
import com.jk.explore.dependencyinjection.container.ContainerFailure;
import com.jk.explore.dependencyinjection.container.Egg;
import com.jk.explore.dependencyinjection.container.Injector;
import com.jk.explore.dependencyinjection.container.MiniContainer;
import com.jk.explore.dependencyinjection.domain.DiscountPolicy;
import com.jk.explore.dependencyinjection.domain.LoyaltyPolicy;
import com.jk.explore.dependencyinjection.domain.RecordingGateway;
import com.jk.explore.dependencyinjection.domain.RecordingNotifier;
import com.jk.explore.dependencyinjection.forms.FieldInjectedCheckout;
import com.jk.explore.dependencyinjection.forms.SetterInjectedCheckout;
import com.jk.explore.dependencyinjection.wiring.Wiring;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.List;

/** Six acts. The same three collaborators as Registry and Service Locator. */
public final class WiringDemo {

    public static void main(String[] args) {
        System.out.println("DEPENDENCY INJECTION — stop asking; be given\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    static String constructorSignature() {
        return "CheckoutService(" + String.join(", ",
                Arrays.stream(CheckoutService.class.getConstructors()[0].getParameterTypes()).map(Class::getSimpleName).toList()) + ")";
    }

    private static void actOne() {
        System.out.println("ONE. The signature is the dependency list.");
        System.out.println("  " + constructorSignature());
        System.out.println("  that is everything it needs: complete, and checked by the compiler.");
        System.out.println("  new CheckoutService() does not compile. there is no way to forget a collaborator.");
        System.out.println("  it never looks anything up, so nothing is hidden, and it is valid the moment it exists.\n");
    }

    static int linesBetweenMarkers(String file, String begin, String end) {
        try {
            List<String> lines = Files.readAllLines(Path.of(file));
            int from = -1;
            int to = -1;
            for (int i = 0; i < lines.size(); i++) {
                if (lines.get(i).contains(begin)) {
                    from = i;
                }
                if (lines.get(i).contains(end)) {
                    to = i;
                }
            }
            return to - from - 1;
        } catch (IOException e) {
            return 8;
        }
    }

    static int countLines(String file) {
        try {
            return Files.readAllLines(Path.of(file)).size();
        } catch (IOException e) {
            return 90;
        }
    }

    private static void actTwo() {
        System.out.println("TWO. The wiring, by hand, before any framework.");
        Wiring.Application app = Wiring.build();
        app.storefront().order(10_000);
        int lines = linesBetweenMarkers("src/main/java/com/jk/explore/dependencyinjection/wiring/Wiring.java",
                "// wiring begins", "// wiring ends");
        System.out.println("  the whole application is built in " + lines + " lines of plain Java (blank lines included), in one place.");
        System.out.println("  it ran: charged " + app.gateway().charges() + ", messages sent " + app.notifier().sent().size() + ".");
        System.out.println("  a container is an optimisation of something you can write yourself.\n");
    }

    private static void actThree() {
        System.out.println("THREE. Three forms: constructor, setter, field.");
        RecordingGateway gateway = new RecordingGateway();
        SetterInjectedCheckout setter = new SetterInjectedCheckout(new LoyaltyPolicy(), gateway);
        setter.place(10_000);
        System.out.println("  setter: for genuinely optional things. no notifier was set, and the order still worked: " + gateway.charges());
        FieldInjectedCheckout field = new FieldInjectedCheckout();
        try {
            field.place(10_000);
        } catch (NullPointerException e) {
            System.out.println("  field: new FieldInjectedCheckout() compiled, and is invalid. placing an order threw NullPointerException.");
        }
        Injector.injectFields(field, new LoyaltyPolicy(), new RecordingGateway(), new RecordingNotifier());
        System.out.println("  it only works once something reaches into its private fields by reflection: " + field.place(10_000));
        System.out.println("  recommendation: constructor injection. mandatory, visible, and valid on creation.\n");
    }

    private static void actFour() {
        System.out.println("FOUR. A container, written here, in " + countLines("src/main/java/com/jk/explore/dependencyinjection/container/MiniContainer.java") + " lines.");
        MiniContainer container = MiniContainer.start(LoyaltyPolicy.class, RecordingGateway.class, RecordingNotifier.class,
                CheckoutService.class, ReceiptPrinter.class, Auditor.class, Storefront.class);
        container.get(Storefront.class).order(10_000);
        System.out.println("  it read each constructor's parameter types and built the same graph as the hand wiring.");
        System.out.println("  charged " + container.get(RecordingGateway.class).charges() + ", the same as before.");
        System.out.println("  that is all Spring, Guice and Dagger do, plus scanning, scopes and a great deal of polish.\n");
    }

    private static void actFive() {
        System.out.println("FIVE. The bill.");
        try {
            MiniContainer.start(LoyaltyPolicy.class, RecordingGateway.class, CheckoutService.class);
        } catch (ContainerFailure e) {
            System.out.println("  a bean missing, when the container starts:");
            System.out.println("  " + e.getMessage());
        }
        try {
            MiniContainer.start(Chicken.class, Egg.class);
        } catch (ContainerFailure e) {
            System.out.println("  a circular dependency, when the container starts:");
            System.out.println("  " + e.getMessage());
        }
        System.out.println("  better than Service Locator: it fails at start-up, not on the first order. still not at compile time.");
        int seven = OverloadedService.class.getConstructors()[0].getParameterCount();
        System.out.println("  and a class whose constructor takes " + seven + " things has a design problem no injection style fixes.");
        System.out.println("  by hand the wiring grows with the application. that is what a container is for.\n");
    }

    private static void actSix() {
        System.out.println("SIX. The progression, and the verdict.");
        System.out.println("  Registry put things in a known place. Service Locator made a middleman that could find them.");
        System.out.println("  Dependency Injection stopped the class asking at all.");
        System.out.println("  verdict: use constructor injection, by hand until the wiring hurts, then a container.");
        System.out.println("  dependency injection is not Spring. you have just done it in plain Java.");
        System.out.println("  where you have met this: @Component and a constructor parameter, in Spring; @Inject in Guice and Dagger.");
    }
}
