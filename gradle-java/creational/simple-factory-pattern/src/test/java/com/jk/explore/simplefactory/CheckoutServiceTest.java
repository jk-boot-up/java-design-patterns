package com.jk.explore.simplefactory;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CheckoutServiceTest {

    private final PrintStream originalOut = System.out;
    private ByteArrayOutputStream captured;

    @BeforeEach
    void captureOutput() {
        captured = new ByteArrayOutputStream();
        System.setOut(new PrintStream(captured));
    }

    @AfterEach
    void restoreOutput() {
        System.setOut(originalOut);
    }

    @Test
    @DisplayName("the receipt reports the method the caller asked for")
    void receiptMatchesTheRequestedType() {
        PaymentReceipt receipt = new CheckoutService()
                .checkout(new PaymentRequest("ORD-1001", "CUST-001", 49.98), PaymentType.UPI);

        assertEquals("UPI", receipt.method());
        assertEquals(49.98, receipt.amount());
        assertTrue(receipt.transactionId().startsWith("UPI-"), receipt.transactionId());
    }

    @Test
    @DisplayName("switching the type switches the implementation, not the calling code")
    void sameCallSiteDifferentImplementation() {
        CheckoutService checkout = new CheckoutService();
        PaymentRequest request = new PaymentRequest("ORD-1001", "CUST-001", 49.98);

        assertEquals("Credit Card", checkout.checkout(request, PaymentType.CREDIT_CARD).method());
        assertEquals("PayPal", checkout.checkout(request, PaymentType.PAYPAL).method());
        assertEquals("Net Banking", checkout.checkout(request, PaymentType.NET_BANKING).method());
    }

    @Test
    @DisplayName("the chosen method actually runs")
    void delegatesToTheChosenMethod() {
        new CheckoutService().checkout(new PaymentRequest("ORD-1001", "CUST-001", 49.98),
                PaymentType.PAYPAL);

        String output = captured.toString();
        assertTrue(output.contains("PayPal: redirecting"), output);
        assertTrue(output.contains("Checkout: done"), output);
    }
}
