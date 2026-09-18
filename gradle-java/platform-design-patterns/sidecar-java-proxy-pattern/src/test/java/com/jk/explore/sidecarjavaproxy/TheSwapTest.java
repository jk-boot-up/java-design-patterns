package com.jk.explore.sidecarjavaproxy;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * The project's one claim, pinned down: the proxy changes and the service does not.
 *
 * <p>Every test here is written against the same service instance before and after a
 * swap, and the assertions are deliberately about identity rather than about behaviour.
 * A service that merely behaved the same afterwards would be a service that had been
 * carefully rebuilt; a service that is the same object is a service nobody touched.
 */
class TheSwapTest {

    private final PaymentGateway provider = new PaymentGateway();
    private final ProxyPolicy policy = ProxyPolicy.agreedWithTheProvider();
    private final NginxProxy nginx = new NginxProxy(PaymentsService.NAME, provider, policy);
    private final JavaProxy java = new JavaProxy(PaymentsService.NAME, provider, policy);

    @Test
    @DisplayName("the service is the same object, with the same fields, after the swap")
    void theServiceIsUntouched() {
        LocalPort port = new LocalPort(nginx);
        PaymentsService checkout = new PaymentsService(PaymentsService.NAME, port);
        int startNumberBefore = checkout.startNumber();
        String endpointBefore = checkout.configuredEndpoint();
        LocalPort portBefore = checkout.port();

        port.install(java);

        assertSame(portBefore, checkout.port());
        assertEquals(startNumberBefore, checkout.startNumber());
        assertEquals(endpointBefore, checkout.configuredEndpoint());
    }

    @Test
    @DisplayName("the swap changes what is listening, and only that")
    void theProxyIsTheOnlyThingThatChanged() {
        LocalPort port = new LocalPort(nginx);

        assertSame(nginx, port.occupant());
        port.install(java);
        assertSame(java, port.occupant());
        assertEquals(1, port.swaps());
    }

    @Test
    @DisplayName("the two proxies are written in different languages")
    void theTwoProxiesDisagreeAboutLanguage() {
        assertNotEquals(nginx.language(), java.language());
    }

    @Test
    @DisplayName("the service pays through whichever proxy is on the port at the time")
    void thePaymentGoesThroughWhoeverIsListening() {
        provider.behave();
        LocalPort port = new LocalPort(nginx);
        PaymentsService checkout = new PaymentsService(PaymentsService.NAME, port);

        assertEquals("pay_ORD-1", checkout.pay(Payment.of("ORD-1", 100)).providerRef());
        port.install(java);
        assertEquals("pay_ORD-2", checkout.pay(Payment.of("ORD-2", 100)).providerRef());
    }

    @Test
    @DisplayName("a swap can be undone by putting the old proxy back")
    void theSwapGoesBothWays() {
        LocalPort port = new LocalPort(nginx);

        port.install(java);
        port.install(nginx);

        assertSame(nginx, port.occupant());
        assertEquals(2, port.swaps());
    }

    @Test
    @DisplayName("mid-swap the port is empty and the service has nothing to fall back on")
    void theWindowInTheMiddleIsRealAndCostsPayments() {
        provider.behave();
        LocalPort port = new LocalPort(nginx);
        PaymentsService checkout = new PaymentsService(PaymentsService.NAME, port);
        port.vacate();

        PaymentFailed failed = assertThrows(PaymentFailed.class,
                () -> checkout.pay(Payment.of("ORD-3", 100)));

        assertEquals(PaymentFailed.Reason.NOTHING_LISTENING, failed.reason());
        // A healthy provider that never heard about it, which is the sharp part.
        assertEquals(0, provider.callLog().total());
    }
}
