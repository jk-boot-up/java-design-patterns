package com.jk.explore.retryr4j;

import org.junit.jupiter.api.Test;
import org.springframework.context.ConfigurableApplicationContext;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class RetryTest {

    @Test
    void aFlakyGatewayIsRetriedUntilItAnswers() {
        try (ConfigurableApplicationContext ctx = PaymentsApplication.builder().run()) {
            PaymentGateway g = ctx.getBean(PaymentGateway.class);
            g.timeOutBeforeCharging(2);
            assertEquals("R-1", ctx.getBean(PaymentsClient.class).charge("K", 100));
            assertEquals(3, g.calls());
        }
    }

    @Test
    void waitsDoubleBetweenAttempts() {
        try (ConfigurableApplicationContext ctx = PaymentsApplication.builder().run()) {
            List<Long> waits = PaymentsApplication.recordWaits(ctx, "payments");
            ctx.getBean(PaymentGateway.class).timeOutBeforeCharging(2);
            ctx.getBean(PaymentsClient.class).charge("K", 100);
            assertEquals(List.of(1L, 2L), waits);
        }
    }

    @Test
    void givesUpAfterThreeAttemptsAndRethrows() {
        try (ConfigurableApplicationContext ctx = PaymentsApplication.builder().run()) {
            PaymentGateway g = ctx.getBean(PaymentGateway.class);
            g.timeOutBeforeCharging(100);
            assertThrows(GatewayTimeout.class, () -> ctx.getBean(PaymentsClient.class).charge("K", 100));
            assertEquals(3, g.calls());
        }
    }

    @Test
    void aDeclinedCardIsRetriedOnlyWhenEverythingIsRetried() {
        try (ConfigurableApplicationContext ctx = PaymentsApplication.builder().run()) {
            PaymentGateway g = ctx.getBean(PaymentGateway.class);
            g.declineCards(true);
            assertThrows(CardDeclined.class, () -> ctx.getBean(PaymentsClient.class).charge("K", 100));
            assertEquals(1, g.calls());
            g.reset();
            g.declineCards(true);
            assertThrows(CardDeclined.class, () -> ctx.getBean(PaymentsClient.class).chargeRetryingEverything("K", 100));
            assertEquals(3, g.calls());
        }
    }

    @Test
    void aLostAnswerChargesTwiceWithoutAKeyAndOnceWithOne() {
        try (ConfigurableApplicationContext ctx = PaymentsApplication.builder().run()) {
            PaymentGateway g = ctx.getBean(PaymentGateway.class);
            PaymentsClient c = ctx.getBean(PaymentsClient.class);
            g.timeOutAfterCharging(1);
            c.charge(null, 4999);
            assertEquals(List.of(4999L, 4999L), g.charges());
            g.reset();
            g.timeOutAfterCharging(1);
            c.charge("K", 4999);
            assertEquals(List.of(4999L), g.charges());
        }
    }

    @Test
    void layeredRetriesMultiply() {
        try (ConfigurableApplicationContext ctx = PaymentsApplication.builder().run()) {
            PaymentGateway g = ctx.getBean(PaymentGateway.class);
            g.timeOutBeforeCharging(100);
            assertThrows(GatewayTimeout.class, () -> ctx.getBean(CheckoutService.class).pay("K", 100));
            assertEquals(9, g.calls());
        }
    }
}
