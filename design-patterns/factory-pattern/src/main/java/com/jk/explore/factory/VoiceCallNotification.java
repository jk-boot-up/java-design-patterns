package com.jk.explore.factory;

public class VoiceCallNotification implements Notification {
    @Override
    public void notifyUser() {
        System.out.println("Notified through Voice call");
    }
}
