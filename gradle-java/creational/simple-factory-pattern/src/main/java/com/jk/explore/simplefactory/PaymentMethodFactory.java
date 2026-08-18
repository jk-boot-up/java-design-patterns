package com.jk.explore.simplefactory;

public class PaymentMethodFactory {

    public static PaymentMethod create(PaymentType type) {
        if (type == null) {
            throw new IllegalArgumentException("Payment type must not be null");
        }
        return switch (type) {
            case CREDIT_CARD -> new CreditCardPayment();
            case UPI -> new UpiPayment();
            case PAYPAL -> new PayPalPayment();
            case NET_BANKING -> new NetBankingPayment();
        };
    }

    public static PaymentMethod create(String type) {
        if (type == null || type.isBlank()) {
            throw new IllegalArgumentException("Payment type must not be blank");
        }
        try {
            return create(PaymentType.valueOf(type.trim().toUpperCase().replace('-', '_')));
        } catch (IllegalArgumentException e) {
            throw new IllegalArgumentException("Unsupported payment type: " + type, e);
        }
    }
}
