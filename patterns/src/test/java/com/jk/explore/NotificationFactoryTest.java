package com.jk.explore;

import com.jk.explore.factory.Notification;
import com.jk.explore.factory.NotificationFactory;
import com.jk.explore.factory.SMSNotification;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class NotificationFactoryTest {

    @Test
    public void createNotification() {
        NotificationFactory factory = new NotificationFactory();
        Notification notification = factory.createNotification("SMS");
        Assertions.assertTrue(notification instanceof SMSNotification);
    }

}
