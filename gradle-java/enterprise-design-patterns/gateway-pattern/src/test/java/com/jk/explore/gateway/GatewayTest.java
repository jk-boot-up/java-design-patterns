package com.jk.explore.gateway;

import com.jk.explore.gateway.naive.NaiveCheckout;
import com.jk.explore.gateway.vendor.AcmeClient;
import com.jk.explore.gateway.vendor.BetaPayClient;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class GatewayTest {

    @Test
    void theAcmeGatewayTranslatesEveryCode() {
        AcmeClient acme = new AcmeClient();
        acme.script("00", "51", "91", "91");
        AcmeGateway g = new AcmeGateway(acme, new ArrayList<>());
        assertEquals(new PaymentResult(PaymentStatus.APPROVED, "AC-100"), g.charge(100, "t"));
        assertEquals(PaymentStatus.DECLINED, g.charge(100, "t").status());
        assertEquals(PaymentStatus.UNAVAILABLE, g.charge(100, "t").status());
    }

    @Test
    void aSingleTimeoutIsRetriedOnceInsideTheGateway() {
        AcmeClient acme = new AcmeClient();
        acme.script("91", "00");
        List<String> log = new ArrayList<>();
        assertTrue(new AcmeGateway(acme, log).charge(100, "t").approved());
        assertEquals(2, acme.requests().size());
        assertEquals(List.of("acme timed out on attempt 1"), log);
    }

    @Test
    void anUnknownCodeIsNotSilentlyTreatedAsAnything() {
        AcmeClient acme = new AcmeClient();
        acme.script("77");
        assertThrows(IllegalStateException.class, () -> new AcmeGateway(acme, new ArrayList<>()).charge(1, "t"));
    }

    @Test
    void theFakeNeverTouchesTheNetworkAndAnswersOnDemand() {
        AcmeClient.NETWORK_CALLS.set(0);
        FakeGateway fake = new FakeGateway().willAnswer(PaymentStatus.DECLINED);
        Checkout c = new Checkout(fake);
        assertEquals("card declined", c.pay(1));
        assertEquals("paid, receipt FAKE-2", c.pay(1));
        assertEquals(0, AcmeClient.NETWORK_CALLS.get());
        assertEquals(2, fake.calls());
    }

    @Test
    void theSameCheckoutWorksOnAnyGateway() {
        assertEquals("paid, receipt AC-4999", new Checkout(new AcmeGateway(new AcmeClient(), new ArrayList<>())).pay(4999));
        assertEquals("paid, receipt BP-4999", new Checkout(new BetaGateway(new BetaPayClient())).pay(4999));
        assertEquals("card declined", new Checkout(new BetaGateway(new BetaPayClient())).pay(150000));
    }

    @Test
    void theNaiveCallersEachBuildTheirOwnRequestAndOneForgotTheCurrency() {
        AcmeClient acme = new AcmeClient();
        NaiveCheckout n = new NaiveCheckout(acme);
        n.checkout(1);
        n.renewSubscription(1);
        n.topUpGiftCard(1);
        assertTrue(acme.requests().get(0).containsKey("ccy"));
        assertTrue(acme.requests().get(1).containsKey("ccy"));
        assertFalse(acme.requests().get(2).containsKey("ccy"));
    }

    @Test
    void theGatewayAlwaysSendsTheCurrency() {
        AcmeClient acme = new AcmeClient();
        new AcmeGateway(acme, new ArrayList<>()).charge(1, "t");
        assertEquals("GBP", acme.requests().get(0).get("ccy"));
    }
}
