package com.jk.explore.proxyspring;

public class AccessDenied extends RuntimeException {
    public AccessDenied(String message) {
        super(message);
    }
}
