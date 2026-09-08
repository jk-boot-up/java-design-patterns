package com.jk.explore.bridge;

import java.util.Objects;

/**
 * A refined Abstraction added after the fact. It needed zero new channel
 * code -- Email, SMS and Push already know how to deliver a subject and a
 * body, whatever notification type they came from.
 */
public final class PasswordResetNotification extends Notification {

    private final String resetCode;

    public PasswordResetNotification(MessageChannel channel, String resetCode) {
        super(channel);
        this.resetCode = Objects.requireNonNull(resetCode);
    }

    @Override
    protected String subject() {
        return "Password reset requested";
    }

    @Override
    protected String body() {
        return "Use code " + resetCode + " to reset your password. It expires in 15 minutes.";
    }
}
