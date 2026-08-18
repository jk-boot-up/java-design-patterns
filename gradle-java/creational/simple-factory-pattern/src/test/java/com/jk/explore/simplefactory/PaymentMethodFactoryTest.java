package com.jk.explore.simplefactory;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.EnumSource;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertThrows;

class PaymentMethodFactoryTest {

    @Test
    @DisplayName("each payment type maps to its own implementation")
    void createsTheRightImplementationForEachType() {
        assertAll(
                () -> assertInstanceOf(CreditCardPayment.class,
                        PaymentMethodFactory.create(PaymentType.CREDIT_CARD)),
                () -> assertInstanceOf(UpiPayment.class,
                        PaymentMethodFactory.create(PaymentType.UPI)),
                () -> assertInstanceOf(PayPalPayment.class,
                        PaymentMethodFactory.create(PaymentType.PAYPAL)),
                () -> assertInstanceOf(NetBankingPayment.class,
                        PaymentMethodFactory.create(PaymentType.NET_BANKING)));
    }

    @ParameterizedTest
    @EnumSource(PaymentType.class)
    @DisplayName("every declared type can be created")
    void everyTypeIsSupported(PaymentType type) {
        PaymentMethod method = PaymentMethodFactory.create(type);

        assertNotNull(method);
        assertNotNull(method.displayName());
    }

    @Test
    @DisplayName("each call returns a fresh instance")
    void returnsANewInstanceEachTime() {
        assertNotSame(PaymentMethodFactory.create(PaymentType.UPI),
                PaymentMethodFactory.create(PaymentType.UPI));
    }

    @ParameterizedTest
    @ValueSource(strings = {"credit_card", "CREDIT-CARD", " credit_card "})
    @DisplayName("the string overload is forgiving about case, dashes and spaces")
    void acceptsStringNames(String name) {
        assertInstanceOf(CreditCardPayment.class, PaymentMethodFactory.create(name));
    }

    @Test
    @DisplayName("an unknown name is rejected with a helpful message")
    void rejectsUnknownName() {
        IllegalArgumentException e = assertThrows(IllegalArgumentException.class,
                () -> PaymentMethodFactory.create("bitcoin"));

        assertEquals("Unsupported payment type: bitcoin", e.getMessage());
    }

    @Test
    @DisplayName("null and blank input are rejected")
    void rejectsMissingInput() {
        assertAll(
                () -> assertThrows(IllegalArgumentException.class,
                        () -> PaymentMethodFactory.create((PaymentType) null)),
                () -> assertThrows(IllegalArgumentException.class,
                        () -> PaymentMethodFactory.create((String) null)),
                () -> assertThrows(IllegalArgumentException.class,
                        () -> PaymentMethodFactory.create("   ")));
    }
}
