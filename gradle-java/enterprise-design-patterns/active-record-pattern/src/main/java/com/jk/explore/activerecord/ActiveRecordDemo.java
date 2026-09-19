package com.jk.explore.activerecord;

import java.util.List;

public class ActiveRecordDemo {

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void reset() {
        Customer.TABLE.resetCount();
        Order.TABLE.resetCount();
    }

    static int operations() {
        return Customer.TABLE.operations() + Order.TABLE.operations();
    }

    private static void one() {
        System.out.println("ONE. A record that saves itself.");
        Customer ada = new Customer("ada").save();
        Order order = new Order(ada.id());
        order.addLine(800, 2);
        order.save();
        Order again = Order.find(order.id());
        System.out.println("  saved order " + again.id() + " for customer " + again.customerId() + ", " + again.totalPence() + " pence, " + again.status() + ".");
        System.out.println("  three lines: new, save, find. no repository, no mapper.");
    }

    private static void two() {
        System.out.println("TWO. Finders on the class.");
        Customer ben = new Customer("ben").save();
        for (int i = 1; i <= 3; i++) {
            Order o = new Order(ben.id());
            o.addLine(500, i);
            o.save();
        }
        List<Order> orders = Order.forCustomer(ben.id());
        System.out.println("  Order.forCustomer(" + ben.id() + "): " + orders.size() + " orders, totals " + orders.stream().map(Order::totalPence).toList() + ".");
    }

    private static void three() {
        System.out.println("THREE. The rules are on the record.");
        Order order = new Order(1);
        order.addLine(800, 2);
        order.place();
        try {
            order.addLine(800, 1);
        } catch (IllegalStateException e) {
            System.out.println("  " + e.getMessage() + ".");
        }
        try {
            new Order(1).place();
        } catch (IllegalStateException e) {
            System.out.println("  " + e.getMessage() + ".");
        }
        System.out.println("  what an order may do sits beside what an order is.");
    }

    private static void four() {
        System.out.println("FOUR. The bill: a rule that needs the table.");
        Customer c = new Customer("cy").save();
        Order order = new Order(c.id());
        order.addLine(3000, 2);
        reset();
        boolean free = order.qualifiesForFreeDelivery(5000);
        System.out.println("  is a 60.00 order eligible for free delivery? " + free + ". table operations to find out: " + operations() + ".");
        reset();
        boolean pure = PureDiscount.qualifiesForFreeDelivery(order.totalPence(), 5000);
        System.out.println("  the same rule on two numbers: " + pure + ". table operations: " + operations() + ".");
        System.out.println("  to test the rule on the record, the customers table has to exist and hold a customer.");
    }

    private static void five() {
        System.out.println("FIVE. The bill: the class is the table.");
        Order saved = new Order(1);
        saved.addLine(800, 1);
        saved.save();
        Order.TABLE.renameColumn("total_pence", "grand_total");
        try {
            Order.find(saved.id());
        } catch (IllegalStateException e) {
            System.out.println("  a column was renamed. loading an order: " + e.getMessage() + ".");
        }
        System.out.println("  the fields of the class are the columns of the table. one cannot change without the other.");
        Order.TABLE.renameColumn("grand_total", "total_pence");
    }

    private static void six() {
        System.out.println("SIX. The bill: queries you cannot see.");
        Customer c = new Customer("di").save();
        for (int i = 0; i < 5; i++) {
            Order o = new Order(c.id());
            o.addLine(3000, 2);
            o.save();
        }
        List<Order> orders = Order.forCustomer(c.id());
        reset();
        int eligible = 0;
        for (Order o : orders) {
            if (o.qualifiesForFreeDelivery(5000)) {
                eligible++;
            }
        }
        System.out.println("  checking " + orders.size() + " orders for free delivery, " + eligible + " eligible: " + operations() + " table operations.");
        System.out.println("  each call looked innocent. each one loaded the customer again.");
    }
}
