package com.jk.explore.factory;

public class MailNotification implements Notification {
    @Override
    public void notifyUser() {
        System.out.println("Notified user through Mail");
    }
}
