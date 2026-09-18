package com.jk.explore.sidecarjavaproxy;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * The reason to swap, measured from the provider's end.
 *
 * <p>These tests are the ones to read first, because they are the argument. Both proxies
 * are allowed three attempts and both take three; the tests that matter are about
 * <em>when</em> those three arrive, and they use the provider's own recorded arrival
 * times rather than anything the proxies report about themselves.
 *
 * <p>Notice that none of the nginx tests is a failing test waiting to be fixed. They all
 * pass, and they pin down a boundary rather than a defect: the proxy does exactly what
 * its configuration language can express, and the payment still fails.
 */
class TheSpacingTest {

    private final PaymentGateway provider = new PaymentGateway();
    private final ProxyPolicy policy = ProxyPolicy.agreedWithTheProvider();
    private final Payment payment = Payment.of("ORD-4418", 4799);

    @Test
    @DisplayName("nginx makes all three attempts inside the first three milliseconds")
    void nginxRetriesWithoutWaiting() {
        provider.beginWobble();
        NginxProxy nginx = new NginxProxy(PaymentsService.NAME, provider, policy);

        assertThrows(PaymentFailed.class, () -> nginx.forward(payment));

        assertEquals(3, provider.callLog().total());
        assertEquals(List.of(1L, 2L, 3L), arrivalTimes());
        assertTrue(provider.callLog().spanMillis() < PaymentGateway.RECOVERS_AT_MILLIS);
    }

    @Test
    @DisplayName("the java proxy makes the same three attempts, spread over 602ms")
    void theJavaProxyWaitsAndDoubles() {
        provider.beginWobble();
        JavaProxy java = new JavaProxy(PaymentsService.NAME, provider, policy);

        Receipt receipt = java.forward(payment);

        assertEquals(3, receipt.attempts());
        assertEquals(603, receipt.waitedMillis());
        assertEquals(List.of(1L, 202L, 603L), arrivalTimes());
        assertEquals(602, provider.callLog().spanMillis());
    }

    @Test
    @DisplayName("the same allowance, spent differently, is the whole difference")
    void bothSpendThreeAttemptsAndOnlyOneGetsPaid() {
        provider.beginWobble();
        NginxProxy nginx = new NginxProxy(PaymentsService.NAME, provider, policy);
        assertThrows(PaymentFailed.class, () -> nginx.forward(payment));
        int nginxAttempts = provider.callLog().total();

        provider.beginWobble();
        JavaProxy java = new JavaProxy(PaymentsService.NAME, provider, policy);
        Receipt receipt = java.forward(payment);

        assertEquals(nginxAttempts, receipt.attempts());
        assertEquals("pay_ORD-4418", receipt.providerRef());
    }

    @Test
    @DisplayName("neither proxy retries a refusal, because retrying one makes it worse")
    void neitherProxyRetriesARateLimit() {
        provider.refuseEverything();

        for (Proxy proxy : List.of(new NginxProxy(PaymentsService.NAME, provider, policy),
                new JavaProxy(PaymentsService.NAME, provider, policy))) {
            provider.refuseEverything();
            PaymentFailed failed = assertThrows(PaymentFailed.class,
                    () -> proxy.forward(payment));

            assertEquals(PaymentFailed.Reason.RATE_LIMITED, failed.reason());
            // One attempt, not three. A refusal is not a decline.
            assertEquals(1, provider.callLog().total());
        }
    }

    @Test
    @DisplayName("a healthy provider costs one attempt through either proxy")
    void aHealthyProviderNeedsNoRetries() {
        provider.behave();

        assertEquals(1, new NginxProxy(PaymentsService.NAME, provider, policy)
                .forward(payment).attempts());
        assertEquals(1, new JavaProxy(PaymentsService.NAME, provider, policy)
                .forward(payment).attempts());
    }

    @Test
    @DisplayName("only one of the two can state the whole agreed policy")
    void onlyOneOfThemCanSayTheWholeThing() {
        assertEquals(1, new NginxProxy(PaymentsService.NAME, provider, policy)
                .cannotExpress().size());
        assertTrue(new JavaProxy(PaymentsService.NAME, provider, policy)
                .cannotExpress().isEmpty());
    }

    private List<Long> arrivalTimes() {
        return provider.callLog().attempts().stream()
                .map(CallLog.Attempt::atMillis)
                .toList();
    }
}
