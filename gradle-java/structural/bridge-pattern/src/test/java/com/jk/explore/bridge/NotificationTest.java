package com.jk.explore.bridge;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;

class NotificationTest {

    private final RecordingChannel channel = new RecordingChannel();

    @Test
    void orderConfirmationComposesSubjectAndBody() {
        new OrderConfirmationNotification(channel, "ORD-1042", new BigDecimal("129.99")).send("alex@example.com");

        assertEquals("alex@example.com", channel.recipient);
        assertEquals("Order ORD-1042 confirmed", channel.subject);
        assertEquals("Your order ORD-1042 totalling $129.99 has been confirmed.", channel.body);
    }

    @Test
    void shippingUpdateComposesSubjectAndBody() {
        new ShippingUpdateNotification(channel, "ORD-1042", "out for delivery").send("alex@example.com");

        assertEquals("Shipping update for order ORD-1042", channel.subject);
        assertEquals("Order ORD-1042 is now: out for delivery", channel.body);
    }

    @Test
    void passwordResetComposesSubjectAndBody() {
        new PasswordResetNotification(channel, "384920").send("alex@example.com");

        assertEquals("Password reset requested", channel.subject);
        assertEquals("Use code 384920 to reset your password. It expires in 15 minutes.", channel.body);
    }

    @Test
    void differentNotificationTypesShareTheSameChannelInstance() {
        Notification confirmation = new OrderConfirmationNotification(channel, "ORD-1", BigDecimal.TEN);
        Notification shipping = new ShippingUpdateNotification(channel, "ORD-1", "shipped");

        assertEquals("Recording", confirmation.channelName());
        assertEquals("Recording", shipping.channelName());
    }
}
