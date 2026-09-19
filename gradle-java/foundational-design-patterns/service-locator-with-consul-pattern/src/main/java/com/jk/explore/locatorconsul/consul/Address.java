package com.jk.explore.locatorconsul.consul;

/** Where a service instance can be reached. */
public record Address(String host, int port) {

    public String hostAndPort() {
        return host + ":" + port;
    }
}
