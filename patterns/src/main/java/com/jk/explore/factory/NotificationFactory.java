package com.jk.explore.factory;

public class NotificationFactory {

    public NotificationFactory() {

    }

    public Notification createNotification(String channel) {

        if(channel == "Mail") {
            return new MailNotification();
        }
        if(channel == "SMS") {
            return new SMSNotification();
        }
        if(channel == "Voice") {
            return new VoiceCallNotification();
        }
        return null;
    }


}
