package com.jk.explore.retryr4j;

public class GatewayTimeout extends RuntimeException {
    public GatewayTimeout() {
        super("payment gateway timed out");
    }
}
