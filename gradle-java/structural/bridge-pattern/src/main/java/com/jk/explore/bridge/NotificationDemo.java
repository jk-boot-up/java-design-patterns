package com.jk.explore.bridge;

import java.math.BigDecimal;

public final class NotificationDemo {

    public static void main(String[] args) {
        MessageChannel email = new EmailChannel();
        MessageChannel sms = new SmsChannel();
        MessageChannel push = new PushChannel();

        System.out.println("== Same notification, delivered through three different channels ==");
        new OrderConfirmationNotification(email, "ORD-1042", new BigDecimal("129.99")).send("alex@example.com");
        new OrderConfirmationNotification(sms, "ORD-1042", new BigDecimal("129.99")).send("+1-555-0142");
        new OrderConfirmationNotification(push, "ORD-1042", new BigDecimal("129.99")).send("device-9f31");
        System.out.println();

        System.out.println("== A different notification type, same channels, zero new channel code ==");
        new ShippingUpdateNotification(email, "ORD-1042", "out for delivery").send("alex@example.com");
        new ShippingUpdateNotification(sms, "ORD-1042", "out for delivery").send("+1-555-0142");
        System.out.println();

        System.out.println("== A brand-new notification type reuses every existing channel ==");
        new PasswordResetNotification(email, "384920").send("alex@example.com");
        System.out.println();

        System.out.println("== SMS truncates; Email does not -- channel behavior, isolated from notification code ==");
        String longStatus = "delayed at customs due to an incomplete declaration, expect an update within 2 business days";
        new ShippingUpdateNotification(email, "ORD-1099", longStatus).send("alex@example.com");
        new ShippingUpdateNotification(sms, "ORD-1099", longStatus).send("+1-555-0142");
        System.out.println();

        System.out.println("== The naive alternative, for comparison ==");
        new NaiveOrderConfirmationEmail("ORD-1042", new BigDecimal("129.99")).send("alex@example.com");
        new NaiveOrderConfirmationSms("ORD-1042", new BigDecimal("129.99")).send("+1-555-0142");
        new NaiveShippingUpdateEmail("ORD-1042", "out for delivery").send("alex@example.com");
        new NaiveShippingUpdateSms("ORD-1042", "out for delivery").send("+1-555-0142");
        System.out.println("Four classes just for two notification types across two channels --");
        System.out.println("adding Push would mean two more, and a third notification type three more.");
    }
}
