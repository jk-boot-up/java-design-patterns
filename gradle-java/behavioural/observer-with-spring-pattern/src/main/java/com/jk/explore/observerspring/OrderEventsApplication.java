package com.jk.explore.observerspring;

import org.springframework.boot.WebApplicationType;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.scheduling.annotation.EnableAsync;

@SpringBootApplication
@EnableAsync
public class OrderEventsApplication {

    static SpringApplicationBuilder builder() {
        return new SpringApplicationBuilder(OrderEventsApplication.class).web(WebApplicationType.NONE);
    }

    public static void main(String[] args) throws Exception {
        try (ConfigurableApplicationContext ctx = builder().run()) {
            Journal journal = ctx.getBean(Journal.class);
            OrderService orders = ctx.getBean(OrderService.class);
            EmailListener email = ctx.getBean(EmailListener.class);
            AuditListener audit = ctx.getBean(AuditListener.class);

            System.out.println("ONE. The subject knows nobody.");
            orders.ship("ORD-000001");
            journal.lines().forEach(l -> System.out.println("  " + l));

            System.out.println("TWO. On the caller's thread.");
            System.out.println("  the caller is " + Thread.currentThread().getName() + ", and every listener above ran on it.");

            System.out.println("THREE. One listener fails.");
            journal.clear();
            email.mailServerDown(true);
            String outcome;
            try {
                orders.ship("ORD-000002");
                outcome = "the caller saw no error";
            } catch (IllegalStateException e) {
                outcome = "the caller got: " + e.getMessage();
            }
            System.out.println("  " + outcome + ".");
            System.out.println("  order shipped: " + orders.isShipped("ORD-000002") + ".");
            journal.lines().forEach(l -> System.out.println("  " + l));
            System.out.println("  analytics and the warehouse feed never heard about ORD-000002.");
            email.mailServerDown(false);

            System.out.println("FOUR. A listener on another thread.");
            journal.clear();
            audit.hold();
            orders.cancel("ORD-000003");
            System.out.println("  cancel() has returned. journal so far: " + journal.lines() + ".");
            audit.release();
            audit.done().await();
            System.out.println("  after the gate opened: " + journal.lines().stream().filter(l -> l.startsWith("audit")).count() + " audit line, on a thread named "
                    + threadOf(journal, "audit") + ".");

            System.out.println("FIVE. A listener that filters.");
            journal.clear();
            orders.ship("ORD-000004");
            System.out.println("  shipped: the warehouse feed heard: " + journal.lines().stream().anyMatch(l -> l.startsWith("warehouse")) + ".");
            journal.clear();
            audit.hold();
            audit.release();
            orders.cancel("ORD-000005");
            audit.done().await();
            System.out.println("  cancelled: the warehouse feed heard: " + journal.lines().stream().anyMatch(l -> l.startsWith("warehouse")) + ".");

            System.out.println("SIX. An event nobody listens to.");
            journal.clear();
            orders.refund("ORD-000006");
            System.out.println("  refund published. listeners that ran: " + journal.lines().size() + ". errors: 0.");
            System.out.println("  a publisher cannot tell whether anyone is listening.");
        }
    }

    private static String threadOf(Journal journal, String prefix) {
        String line = journal.lines().stream().filter(l -> l.startsWith(prefix)).findFirst().orElse("");
        return line.substring(line.lastIndexOf(" on ") + 4);
    }
}
