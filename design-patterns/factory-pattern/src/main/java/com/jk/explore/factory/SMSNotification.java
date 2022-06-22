package com.jk.explore.factory;

public class SMSNotification implements Notification {
    @Override
    public void notifyUser() {
        System.out.println("Notified user through SMS");
    }
}
