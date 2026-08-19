package com.jk.explore.staticfactory;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.params.provider.Arguments.arguments;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.util.stream.Stream;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

@DisplayName("CheckoutService — one client, five discounts, no branching")
class CheckoutServiceTest {

    private static final Order ORDER =
            new Order("ORD-4001", "CUST-001", Money.pounds(120.00), Money.pounds(4.99));

    private final PrintStream realOut = System.out;
    private ByteArrayOutputStream captured;

    @BeforeEach
    void captureStdout() {
        captured = new ByteArrayOutputStream();
        System.setOut(new PrintStream(captured));
    }

    @AfterEach
    void restoreStdout() {
        System.setOut(realOut);
    }

    static Stream<Arguments> checkouts() {
        return Stream.of(
                arguments(Discount.none(), "No discount", "£0.00", "£124.99"),
                arguments(Discount.percentage(10), "10% off", "£12.00", "£112.99"),
                arguments(Discount.amountOff(Money.pounds(5)), "£5.00 off", "£5.00", "£119.99"),
                arguments(Discount.freeShipping(), "Free shipping", "£4.99", "£120.00"),
                arguments(Discount.bestOf(Discount.percentage(10), Discount.amountOff(Money.pounds(5))),
                        "Best of: 10% off / £5.00 off", "£12.00", "£112.99"));
    }

    @ParameterizedTest(name = "{1}: saves {2}, total {3}")
    @MethodSource("checkouts")
    void identicalCodeAppliesEveryKindOfDiscount(Discount discount, String label,
                                                 String saving, String total) {
        // Only the discount differs between these five runs.
        Receipt receipt = new CheckoutService().checkout(ORDER, discount);

        assertAll(
                () -> assertEquals(label, receipt.discountLabel()),
                () -> assertEquals(saving, receipt.discountAmount().toString()),
                () -> assertEquals(total, receipt.total().toString()));
    }

    @Test
    @DisplayName("the printed run reads in order: order, saving, total")
    void outputOrderIsStable() {
        new CheckoutService().checkout(ORDER, Discount.forCoupon("SAVE10"));

        String[] lines = captured.toString().strip().split("\\R");

        assertAll(
                () -> assertEquals(3, lines.length),
                () -> assertEquals(
                        "Checkout: order ORD-4001 subtotal £120.00 + shipping £4.99", lines[0]),
                () -> assertEquals("Checkout: 10% off saves £12.00", lines[1]),
                () -> assertEquals("Checkout: total £112.99", lines[2]));
    }

    @Test
    @DisplayName("a discount can never make the total exceed the order")
    void discountNeverIncreasesTheTotal() {
        Money undiscounted = ORDER.subtotal().plus(ORDER.shipping());

        assertAll(checkouts()
                .map(args -> (Discount) args.get()[0])
                .map(discount -> () -> assertTrue(
                        new CheckoutService().checkout(ORDER, discount)
                                .total().compareTo(undiscounted) <= 0)));
    }

    @Test
    @DisplayName("the demo runs end to end and rejects the unknown coupon")
    void demoRuns() {
        StaticFactoryDemo.main(new String[0]);

        String out = captured.toString();

        assertAll(
                () -> assertTrue(out.contains("10% off"), out),
                () -> assertTrue(out.contains("Free shipping"), out),
                () -> assertTrue(out.contains("none() is shared: true"), out),
                () -> assertTrue(out.contains("Rejected:"), out));
    }
}
