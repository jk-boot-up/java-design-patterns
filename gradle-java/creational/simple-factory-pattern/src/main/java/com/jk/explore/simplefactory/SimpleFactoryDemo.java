package com.jk.explore.simplefactory;

public class SimpleFactoryDemo {

    public static void main(String[] args) {
        CheckoutService checkout = new CheckoutService();

        for (PaymentType type : PaymentType.values()) {
            PaymentRequest request = new PaymentRequest("ORD-1001", "CUST-001", 49.98);
            PaymentReceipt receipt = checkout.checkout(request, type);

            System.out.println("Receipt: " + receipt);
            System.out.println();
        }
    }
}
