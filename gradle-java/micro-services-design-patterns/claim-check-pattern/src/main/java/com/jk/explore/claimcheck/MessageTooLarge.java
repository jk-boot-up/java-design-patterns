package com.jk.explore.claimcheck;

public class MessageTooLarge extends RuntimeException {
    public MessageTooLarge(int size, int limit) {
        super("message of " + size + " bytes is over the broker's limit of " + limit);
    }
}
