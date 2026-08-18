package com.jk.explore.facade;

public class FacadeDemo {

    public static void main(String[] args) {
        OrderFacade orderFacade = new OrderFacade();
        OrderRequest request = new OrderRequest("CUST-001", "SKU-1234", 2, 49.98, "221B Baker Street, London");

        OrderConfirmation confirmation = orderFacade.placeOrder(request);

        System.out.println("Order placed: " + confirmation);
    }
}
