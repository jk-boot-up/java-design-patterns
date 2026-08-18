package com.jk.explore.abstractfactory;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
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
import org.junit.jupiter.params.provider.MethodSource;

@DisplayName("CheckoutService — one client, three markets, no branching")
class CheckoutServiceTest {

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

    static Stream<org.junit.jupiter.params.provider.Arguments> quotes() {
        return Stream.of(
                arguments(new UkMarketFactory(), "EH1 1YZ",
                        "United Kingdom", "VAT", "£120.00", "£24.00", "£144.00"),
                arguments(new UsMarketFactory(), "10001",
                        "United States", "Sales Tax", "$120.00", "$10.65", "$130.65"),
                arguments(new IndiaMarketFactory(), "560001",
                        "India", "GST", "₹120.00", "₹21.60", "₹141.60"));
    }

    @ParameterizedTest(name = "{2}: {5} tax on {4}")
    @MethodSource("quotes")
    void identicalCodeProducesAMarketCorrectQuote(MarketFactory factory, String postcode,
                                                  String market, String taxLabel,
                                                  String subtotal, String tax, String total) {
        // Only the factory differs between these three runs.
        Quote quote = new CheckoutService(factory)
                .quote(new Order("ORD-3001", "CUST-001", 120.00, postcode));

        assertAll(
                () -> assertEquals(market, quote.market()),
                () -> assertEquals(taxLabel, quote.taxLabel()),
                () -> assertEquals(subtotal, quote.subtotal()),
                () -> assertEquals(tax, quote.tax()),
                () -> assertEquals(total, quote.total()));
    }

    @Test
    @DisplayName("a postcode from another market is rejected, by name")
    void foreignPostcodeIsRejected() {
        CheckoutService us = new CheckoutService(new UsMarketFactory());

        IllegalArgumentException e = assertThrows(IllegalArgumentException.class,
                () -> us.quote(new Order("ORD-3002", "CUST-002", 120.00, "EH1 1YZ")));

        assertAll(
                () -> assertTrue(e.getMessage().contains("EH1 1YZ"), e.getMessage()),
                () -> assertTrue(e.getMessage().contains("United States"), e.getMessage()),
                () -> assertTrue(e.getMessage().contains("ZIP code"), e.getMessage()));
    }

    @Test
    @DisplayName("the rejection message names each market's own address label")
    void rejectionUsesTheMarketsOwnVocabulary() {
        assertAll(
                () -> assertTrue(rejectionFor(new UkMarketFactory(), "10001").contains("postcode")),
                () -> assertTrue(rejectionFor(new UsMarketFactory(), "EH1 1YZ").contains("ZIP code")),
                () -> assertTrue(rejectionFor(new IndiaMarketFactory(), "EH1 1YZ")
                        .contains("PIN code")));
    }

    private String rejectionFor(MarketFactory factory, String postcode) {
        CheckoutService checkout = new CheckoutService(factory);
        return assertThrows(IllegalArgumentException.class,
                () -> checkout.quote(new Order("ORD-X", "CUST-X", 50.00, postcode)))
                .getMessage();
    }

    @Test
    @DisplayName("nothing is printed when the address is rejected")
    void rejectedOrderPrintsNothing() {
        CheckoutService uk = new CheckoutService(new UkMarketFactory());

        assertThrows(IllegalArgumentException.class,
                () -> uk.quote(new Order("ORD-3003", "CUST-003", 80.00, "99999")));

        assertEquals("", captured.toString());
    }

    @Test
    @DisplayName("the printed run reads in order: address, tax, total")
    void outputOrderIsStable() {
        new CheckoutService(new IndiaMarketFactory())
                .quote(new Order("ORD-3004", "CUST-004", 120.00, "560001"));

        String[] lines = captured.toString().strip().split("\\R");

        assertAll(
                () -> assertEquals(3, lines.length),
                () -> assertEquals("Checkout: India order ORD-3004 to PIN code 560001", lines[0]),
                () -> assertEquals("Checkout: GST of ₹21.60 on ₹120.00", lines[1]),
                () -> assertEquals("Checkout: total ₹141.60 INR", lines[2]));
    }

    @Test
    @DisplayName("the demo runs end to end and rejects the mismatched order")
    void demoRuns() {
        AbstractFactoryDemo.main(new String[0]);

        String out = captured.toString();

        assertAll(
                () -> assertTrue(out.contains("United Kingdom"), out),
                () -> assertTrue(out.contains("United States"), out),
                () -> assertTrue(out.contains("India"), out),
                () -> assertTrue(out.contains("Rejected:"), out));
    }
}
