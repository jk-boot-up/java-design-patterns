package com.jk.explore.clean.usecases;

public interface NotificationGateway {

    void send(String to, String body);
}
