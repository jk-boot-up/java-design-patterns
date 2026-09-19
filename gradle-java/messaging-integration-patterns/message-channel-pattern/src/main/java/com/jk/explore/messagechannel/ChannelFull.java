package com.jk.explore.messagechannel;

public class ChannelFull extends RuntimeException {
    public ChannelFull(String channel) {
        super("channel " + channel + " is full");
    }
}
