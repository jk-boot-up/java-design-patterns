package com.jk.explore.simplefactory;

public class CheckoutService {

    public PaymentReceipt checkout(PaymentRequest request, PaymentType type) {
        PaymentMethod method = PaymentMethodFactory.create(type);

        System.out.println("Checkout: paying for " + request.orderId() + " with " + method.displayName());
        PaymentReceipt receipt = method.pay(request);
        System.out.println("Checkout: done, transaction " + receipt.transactionId());

        return receipt;
    }
}
