package com.jk.explore.servicelayer;

import com.jk.explore.servicelayer.domain.CartLine;
import com.jk.explore.servicelayer.domain.EmailService;
import com.jk.explore.servicelayer.domain.Order;
import com.jk.explore.servicelayer.domain.OrderRequest;
import com.jk.explore.servicelayer.domain.PaymentGateway;
import com.jk.explore.servicelayer.domain.Product;
import com.jk.explore.servicelayer.domain.Shop;
import com.jk.explore.servicelayer.naive.ControllerLogic;
import com.jk.explore.servicelayer.naive.CopiedInTheCli;
import com.jk.explore.servicelayer.naive.SelfPlacingOrder;
import com.jk.explore.servicelayer.pattern.AnemicOrder;
import com.jk.explore.servicelayer.pattern.OrderService;
import com.jk.explore.servicelayer.pattern.SupportCli;
import com.jk.explore.servicelayer.pattern.WebController;
import com.jk.explore.servicelayer.toydb.Database;

import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.List;

/**
 * Six acts. One order request throughout. Mice have only 3 in stock, and the
 * request asks for 5, so the order must be refused.
 */
public final class PlaceOrderDemo {

    /** Five mice, when there are only three. */
    static OrderRequest tooManyMice() {
        return new OrderRequest(7, List.of(new CartLine(2, 5)));
    }

    static OrderRequest fineOrder() {
        return new OrderRequest(7, List.of(new CartLine(1, 2), new CartLine(3, 1)));
    }

    public static void main(String[] args) {
        System.out.println("SERVICE LAYER — where does \"place an order\" live?\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    private static void actOne() {
        System.out.println("ONE. The logic in the controller — with one door, it works.");
        PaymentGateway payments = new PaymentGateway();
        EmailService email = new EmailService();
        ControllerLogic web = new ControllerLogic(Shop.seeded(), Shop.products(), payments, email);
        System.out.println("  a good order:   " + web.placeOrder(fineOrder()));
        System.out.println("  charged: " + payments.totalChargedPence() + " pence, emails sent: " + email.sentCount());
        System.out.println("  for one entry point this is fine. then support asks for a command line.\n");
    }

    private static void actTwo() {
        System.out.println("TWO. A second door — the logic is copied, and it drifts.");
        PaymentGateway webPayments = new PaymentGateway();
        ControllerLogic web = new ControllerLogic(Shop.seeded(), Shop.products(), webPayments, new EmailService());
        PaymentGateway cliPayments = new PaymentGateway();
        CopiedInTheCli cli = new CopiedInTheCli(Shop.seeded(), Shop.products(), cliPayments, new EmailService());
        System.out.println("  the same request, 5 mice when 3 are in stock:");
        System.out.println("  through the web:  " + web.placeOrder(tooManyMice()) + ", charged " + webPayments.totalChargedPence());
        System.out.println("  through the CLI:  " + cli.placeOrder(tooManyMice()) + ", charged " + cliPayments.totalChargedPence());
        System.out.println("  the web door was fixed to reserve stock first. the copy was not.");
        System.out.println("  a customer is charged or not, depending on which door they came through.\n");
    }

    private static void actThree() {
        System.out.println("THREE. The other version — put it all in the domain object.");
        int parameters = SelfPlacingOrder.class.getConstructors()[0].getParameterCount();
        System.out.println("  Order.place() needs a payment gateway, an email service, a database and the products.");
        System.out.println("  its constructor takes " + parameters + " things.");
        System.out.println("  it is no longer a domain object.\n");
    }

    private static void actFour() {
        System.out.println("FOUR. The pattern — one placeOrder, two doors.");
        PaymentGateway payments = new PaymentGateway();
        OrderService service = new OrderService(Shop.seeded(), Shop.products(), payments, new EmailService());
        WebController web = new WebController(service);
        SupportCli cli = new SupportCli(service);
        System.out.println("  through the web:  " + web.placeOrder(tooManyMice()) + ", charged " + payments.totalChargedPence());
        System.out.println("  through the CLI:  " + cli.placeOrder(tooManyMice()) + ", charged " + payments.totalChargedPence());
        System.out.println("  the same answer, because there is one placeOrder.");
        System.out.println("  the service owns the order of the steps and the transaction.");
        System.out.println("  the domain owns the rules: stock cannot go below zero.\n");
    }

    private static void actFive() {
        System.out.println("FIVE. The bill — the anemic domain model.");
        List<String> ownMethods = Arrays.stream(AnemicOrder.class.getDeclaredMethods()).map(Method::getName).sorted().toList();
        boolean allAccessors = ownMethods.stream().allMatch(m -> m.startsWith("get") || m.startsWith("set"));
        System.out.println("  AnemicOrder has " + ownMethods.size() + " methods. all getters and setters: " + allAccessors);
        System.out.println("  Order, this project's domain object, carries rules: from() rejects an empty cart or a");
        System.out.println("  zero quantity, and deliveryIsFree() decides delivery. Product.reserve() refuses to go below zero.");
        System.out.println("  push every rule into services and the domain becomes a bag of fields.");
        System.out.println("  the honest line: business rules in the domain, orchestration in the service.\n");
    }

    private static void actSix() {
        System.out.println("SIX. The line is hard to draw.");
        Order big = Order.from(1, new OrderRequest(7, List.of(new CartLine(3, 1))), Shop.products());
        System.out.println("  \"free delivery over 50 pounds\": is that a rule about the order, or about shipping?");
        System.out.println("  here it is on Order: deliveryIsFree() for a 150 pound order is " + big.deliveryIsFree() + ".");
        System.out.println("  another team could put it in a ShippingService, and be just as right.");
        System.out.println("  where you have met this: a @Service class, with @Transactional on placeOrder.");
    }
}
