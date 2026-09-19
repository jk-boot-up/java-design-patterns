package com.jk.explore.chainspring;

import org.springframework.boot.WebApplicationType;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@SpringBootApplication
public class ScreeningApplication {

    static final CheckoutRequest GOOD = new CheckoutRequest("asha", true, true, 10, 4_999);
    static final CheckoutRequest NO_STOCK = new CheckoutRequest("ben", true, false, 10, 4_999);
    static final CheckoutRequest RISKY = new CheckoutRequest("carol", true, true, 90, 4_999);
    static final CheckoutRequest BIG = new CheckoutRequest("dev", true, true, 10, 250_000);
    static final CheckoutRequest NO_ADDRESS = new CheckoutRequest("erin", false, true, 10, 4_999);
    static final List<CheckoutRequest> ALL = List.of(GOOD, NO_ADDRESS, NO_STOCK, RISKY, BIG);

    static SpringApplicationBuilder builder() {
        return new SpringApplicationBuilder(ScreeningApplication.class).web(WebApplicationType.NONE);
    }

    static String show(CheckoutRequest r, Decision d) {
        return String.format("  %-6s %-9s by %-14s %s", r.customer(), d.outcome(), d.by(), d.reason());
    }

    public static void main(String[] args) {
        System.out.println("ONE. Spring builds the chain.");
        try (ConfigurableApplicationContext ctx = builder().run()) {
            ScreeningChain chain = ctx.getBean(ScreeningChain.class);
            System.out.println("  order: " + chain.order() + ".");
            System.out.println("  the order comes from @Order numbers on four different classes.");

            System.out.println("TWO. Five requests.");
            for (CheckoutRequest r : ALL) {
                Decision d = chain.screen(r);
                System.out.println(show(r, d));
                if (!d.notRun().isEmpty()) {
                    System.out.println("         never ran: " + d.notRun());
                }
            }

            System.out.println("THREE. The order is the cost.");
            FraudScoreCheck.CALLS.set(0);
            ALL.forEach(chain::screen);
            int inOrder = FraudScoreCheck.CALLS.get();
            List<ScreeningCheck> fraudFirst = new ArrayList<>(ctx.getBeansOfType(ScreeningCheck.class).values());
            fraudFirst.sort((a, b) -> Integer.compare(rank(a), rank(b)));
            fraudFirst.sort((a, b) -> Boolean.compare(!a.name().equals("fraud"), !b.name().equals("fraud")));
            ScreeningChain costly = new ScreeningChain(fraudFirst, Outcome.APPROVED);
            FraudScoreCheck.CALLS.set(0);
            ALL.forEach(costly::screen);
            System.out.println("  paid fraud-service calls for five requests, cheap checks first, as @Order has it: " + inOrder + ".");
            System.out.println("  the same checks with the paid one first " + costly.order() + ": " + FraudScoreCheck.CALLS.get() + ".");

            System.out.println("FOUR. A link that throws.");
            ctx.getBean(FraudScoreCheck.class).serviceDown(true);
            Decision d = chain.screen(GOOD);
            System.out.println(show(GOOD, d));
            System.out.println("  the chain turned an exception into a referral, and the caller saw no error.");
            ctx.getBean(FraudScoreCheck.class).serviceDown(false);
        }

        System.out.println("FIVE. Switched off by a property.");
        try (ConfigurableApplicationContext ctx = builder().properties("screening.fraud.enabled=false").run()) {
            ScreeningChain chain = ctx.getBean(ScreeningChain.class);
            System.out.println("  order: " + chain.order() + ".");
            System.out.println(show(RISKY, chain.screen(RISKY)));
            System.out.println("  no code changed, and the risky customer is no longer stopped.");
        }

        System.out.println("SIX. Nobody answers.");
        try (ConfigurableApplicationContext ctx = builder().run()) {
            System.out.println(show(GOOD, ctx.getBean(ScreeningChain.class).screen(GOOD)));
        }
        try (ConfigurableApplicationContext ctx = builder().properties("screening.fallback=REFERRED").run()) {
            System.out.println(show(GOOD, ctx.getBean(ScreeningChain.class).screen(GOOD)));
            System.out.println("  the fallback is a named setting, screening.fallback, not an accident.");
        }
    }

    private static int rank(ScreeningCheck check) {
        return switch (check.name()) {
            case "address" -> 10;
            case "stock" -> 20;
            case "fraud" -> 30;
            default -> 40;
        };
    }
}
