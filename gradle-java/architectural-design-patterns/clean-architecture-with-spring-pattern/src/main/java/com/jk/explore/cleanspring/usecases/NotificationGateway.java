package com.jk.explore.cleanspring.usecases;

public interface NotificationGateway {

    void send(String to, String body);
}
