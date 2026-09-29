package com.jk.explore.testdouble;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;
import org.junit.jupiter.api.Test;

/** Checkout tested the way the video teaches: one kind of double per question. */
class CheckoutTest {

    @Test
    void anEmptyBasketNeverCallsTheProvider() {
        // A dummy fails if touched, so passing proves the provider was not called.
        assertEquals("refused: the basket is empty", new Checkout(new DummyGateway()).placeOrder("O", 0));
    }

    @Test
    void theDummyReallyFailsIfUsed() {
        assertThrows(AssertionError.class, () -> new Checkout(new DummyGateway()).placeOrder("O", 100));
    }

    @Test
    void aDeclineIsReportedToTheCustomer() {
        var stub = new StubGateway(PaymentGateway.Result.declined("insufficient funds"));
        assertEquals("not paid: insufficient funds", new Checkout(stub).placeOrder("O", 6344));
    }

    @Test
    void checkoutChargesTheExactTotalInPenceAndRefundsTheReceipt() {
        var spy = new SpyGateway();
        var checkout = new Checkout(spy);
        checkout.placeOrder("ORD-7", 6344);
        checkout.cancel("spy-1");
        assertEquals(List.of("charge(ORD-7, 6344)", "refund(spy-1)"), spy.calls());
    }

    @Test
    void aMockFailsAtTheFirstUnexpectedCall() {
        var mock = new MockGateway().expectCharge("ORD-8", 6344);
        var checkout = new Checkout(mock);
        checkout.placeOrder("ORD-8", 6344);
        mock.verify();
        var e = assertThrows(AssertionError.class, () -> checkout.placeOrder("ORD-8", 6344));
        assertEquals("unexpected call: charge(ORD-8, 6344), no more charges were expected", e.getMessage());
    }

    @Test
    void aMockFailsIfAnExpectedCallNeverCame() {
        var mock = new MockGateway().expectCharge("ORD-9", 100);
        assertThrows(AssertionError.class, mock::verify);
    }

    @Test
    void aFakeRunsAWholeJourney() {
        var fake = new FakeGateway(10000);
        var checkout = new Checkout(fake);
        assertEquals("paid, receipt fake-1", checkout.placeOrder("A", 6344));
        assertEquals("not paid: over the card limit", checkout.placeOrder("B", 5000));
        checkout.cancel("fake-1");
        assertEquals(0, fake.balancePence());
        assertEquals("paid, receipt fake-2", checkout.placeOrder("C", 5000));
        assertEquals(5000, fake.balancePence());
    }

    @Test
    void aStubCannotSeeTheWrongAmountButASpyCan() {
        var stubbed = Checkout.withPenceBug(new StubGateway(PaymentGateway.Result.approved("s")));
        assertEquals("paid, receipt s", stubbed.placeOrder("O", 6344));    // passes: the bug is invisible
        var spy = new SpyGateway();
        Checkout.withPenceBug(spy).placeOrder("O", 6344);
        assertEquals(List.of("charge(O, 63)"), spy.calls());               // the spy shows 63, not 6344
    }

    @Test
    void theRealProviderCostsTimeMoneyAndTheNetwork() {
        var real = new RealGateway();
        var checkout = new Checkout(real);
        checkout.placeOrder("A", 6344);
        checkout.placeOrder("B", 1999);
        checkout.placeOrder("C", 499);
        assertEquals(2400, real.elapsedMillis());
        assertEquals(8842, real.realPenceCharged());
        real.goOffline();
        assertThrows(IllegalStateException.class, () -> checkout.placeOrder("D", 1));
    }
}
