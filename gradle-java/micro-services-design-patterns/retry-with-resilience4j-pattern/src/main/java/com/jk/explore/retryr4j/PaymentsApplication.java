package com.jk.explore.retryr4j;

import io.github.resilience4j.retry.RetryRegistry;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

import java.util.ArrayList;
import java.util.List;

@SpringBootApplication
public class PaymentsApplication {

    static SpringApplicationBuilder builder() {
        return new SpringApplicationBuilder(PaymentsApplication.class).web(WebApplicationType.NONE);
    }

    /** Records the wait Resilience4j chose before each retry. */
    static List<Long> recordWaits(ConfigurableApplicationContext ctx, String name) {
        List<Long> waits = new ArrayList<>();
        ctx.getBean(RetryRegistry.class).retry(name).getEventPublisher()
                .onRetry(event -> waits.add(event.getWaitInterval().toMillis()));
        return waits;
    }

    public static void main(String[] args) {
        try (ConfigurableApplicationContext ctx = builder().run()) {
            PaymentGateway gateway = ctx.getBean(PaymentGateway.class);
            PaymentsClient client = ctx.getBean(PaymentsClient.class);

            System.out.println("ONE. A flaky call, retried.");
            gateway.timeOutBeforeCharging(2);
            System.out.println("  the gateway times out twice. the caller gets: " + client.charge("K-1", 4999) + ". gateway calls: " + gateway.calls() + ".");

            System.out.println("TWO. Backoff.");
            gateway.reset();
            List<Long> waits = recordWaits(ctx, "payments");
            gateway.timeOutBeforeCharging(2);
            client.charge("K-2", 4999);
            System.out.println("  waits before each retry, in milliseconds: " + waits + ".");
            System.out.println("  each wait is twice the one before, so a struggling gateway is given room.");

            System.out.println("THREE. Giving up.");
            gateway.reset();
            gateway.timeOutBeforeCharging(100);
            try {
                client.charge("K-3", 4999);
            } catch (GatewayTimeout e) {
                System.out.println("  the gateway never answers. after " + gateway.calls() + " attempts the caller gets: " + e.getClass().getSimpleName() + ".");
            }

            System.out.println("FOUR. Not everything is worth retrying.");
            gateway.reset();
            gateway.declineCards(true);
            try {
                client.charge("K-4", 4999);
            } catch (CardDeclined e) {
                System.out.println("  a declined card, retried only on timeouts: " + gateway.calls() + " attempt.");
            }
            gateway.reset();
            gateway.declineCards(true);
            try {
                client.chargeRetryingEverything("K-4", 4999);
            } catch (CardDeclined e) {
                System.out.println("  the same card, retrying everything: " + gateway.calls() + " attempts against a card that will decline again.");
            }

            System.out.println("FIVE. A retry can charge twice.");
            gateway.reset();
            gateway.timeOutAfterCharging(1);
            client.charge(null, 4999);
            System.out.println("  the charge went through but the answer was lost. no idempotency key. charges made: " + gateway.charges() + ".");
            gateway.reset();
            gateway.timeOutAfterCharging(1);
            client.charge("K-5", 4999);
            System.out.println("  the same failure, with an idempotency key. charges made: " + gateway.charges() + ".");

            System.out.println("SIX. Retries multiply.");
            gateway.reset();
            gateway.timeOutBeforeCharging(100);
            try {
                ctx.getBean(CheckoutService.class).pay("K-6", 4999);
            } catch (GatewayTimeout e) {
                System.out.println("  checkout retries three times, and each of those retries the gateway three times.");
                System.out.println("  one dead gateway, one customer: " + gateway.calls() + " calls.");
            }
        }
    }
}
