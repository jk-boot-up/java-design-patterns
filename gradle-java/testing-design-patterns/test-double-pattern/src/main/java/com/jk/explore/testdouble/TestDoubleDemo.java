package com.jk.explore.testdouble;

import java.util.ArrayList;
import java.util.List;

/**
 * The six acts: the real provider, then a dummy and a stub, a spy, a mock, a fake, and the bill.
 */
public final class TestDoubleDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. Testing checkout against the real provider.");
        RealGateway real = new RealGateway();
        Checkout withReal = new Checkout(real);
        withReal.placeOrder("ORD-1", 6344);
        withReal.placeOrder("ORD-2", 1999);
        withReal.placeOrder("ORD-3", 499);
        out.add("  3 tests passed, taking " + real.elapsedMillis() + " ms of network calls");
        out.add("  real money charged to the test card: £" + pounds(real.realPenceCharged()));
        real.goOffline();
        try {
            withReal.placeOrder("ORD-4", 6344);
        } catch (IllegalStateException e) {
            out.add("  4th test, on a train with no signal: FAILED, " + e.getMessage());
            out.add("  checkout was not broken: the test failed for a reason outside the code");
        }

        out.add("");
        out.add("TWO. A dummy and a stub.");
        String empty = new Checkout(new DummyGateway()).placeOrder("ORD-5", 0);
        out.add("  empty basket, with a dummy that fails if touched: " + empty);
        String declined = new Checkout(new StubGateway(PaymentGateway.Result.declined("insufficient funds")))
                .placeOrder("ORD-6", 6344);
        out.add("  a stub that always declines: " + declined);
        out.add("  both ran in 0 ms and charged nothing");

        out.add("");
        out.add("THREE. A spy writes down every call.");
        SpyGateway spy = new SpyGateway();
        Checkout withSpy = new Checkout(spy);
        withSpy.placeOrder("ORD-7", 6344);
        withSpy.cancel("spy-1");
        out.add("  place ORD-7 for £63.44, then cancel it");
        out.add("  the spy recorded: " + spy.calls());

        out.add("");
        out.add("FOUR. A mock expects exact calls, and complains at once.");
        MockGateway mock = new MockGateway().expectCharge("ORD-8", 6344);
        Checkout withMock = new Checkout(mock);
        out.add("  expected charge(ORD-8, 6344): " + withMock.placeOrder("ORD-8", 6344));
        mock.verify();
        out.add("  verify(): every expected call happened");
        try {
            withMock.placeOrder("ORD-8", 6344);
        } catch (AssertionError e) {
            out.add("  a double click charges again: FAILED at once, " + e.getMessage());
        }

        out.add("");
        out.add("FIVE. A fake: a small working provider, in memory.");
        FakeGateway fake = new FakeGateway(10000);
        Checkout withFake = new Checkout(fake);
        String first = withFake.placeOrder("ORD-9", 6344);
        out.add("  card limit £100.00; pay £63.44: " + first);
        out.add("  pay another £50.00: " + withFake.placeOrder("ORD-10", 5000));
        withFake.cancel("fake-1");
        out.add("  cancel the first order; balance now £" + pounds(fake.balancePence()));
        out.add("  pay £50.00 again: " + withFake.placeOrder("ORD-11", 5000)
                + "; balance £" + pounds(fake.balancePence()));

        out.add("");
        out.add("SIX. The bill: a double only checks what you told it to.");
        String stubbed = Checkout.withPenceBug(new StubGateway(PaymentGateway.Result.approved("stub-1")))
                .placeOrder("ORD-12", 6344);
        out.add("  a checkout that sends pounds instead of pence, tested with a stub: " + stubbed + ", PASSED");
        SpyGateway spy2 = new SpyGateway();
        Checkout.withPenceBug(spy2).placeOrder("ORD-12", 6344);
        out.add("  the same bug with a spy: recorded " + spy2.calls() + ", not charge(ORD-12, 6344): FAILED");
        out.add("  and no double can tell you the real provider still works: keep one test against it");
        return out;
    }

    static String pounds(long pence) {
        return String.format("%d.%02d", pence / 100, pence % 100);
    }

    private TestDoubleDemo() {
    }
}
