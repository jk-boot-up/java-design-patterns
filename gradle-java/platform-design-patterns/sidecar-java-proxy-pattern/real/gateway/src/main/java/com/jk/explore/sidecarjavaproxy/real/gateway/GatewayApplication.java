package com.jk.explore.sidecarjavaproxy.real.gateway;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * The payment provider, standing in for the thing at the other end of the wire.
 *
 * <p>It is here for two reasons. The obvious one is that a demo needs something
 * to fail: this gateway can be told to decline the first few attempts at a
 * payment, which is what makes a retry policy observable. The less obvious one
 * is that it is the only honest place to count from. Every attempt figure this
 * project quotes is taken from the gateway's own tally rather than from the
 * caller's, because the caller cannot see the attempts a proxy made on its
 * behalf -- that invisibility is the whole point of the pattern, and a project
 * that counted from the caller would be quoting a number the caller does not
 * have.
 *
 * <p>It listens on HTTPS, with TLS 1.3 only. That is not decoration. In Tier 1
 * the transport profile is one of the four concerns that got copied into four
 * services; here it is a concern that the payments service genuinely never
 * learns about, because the payments service speaks plain HTTP to localhost and
 * the proxy beside it is what presents a certificate to the outside world.
 */
@SpringBootApplication
public class GatewayApplication {

    public static void main(String[] args) {
        SpringApplication.run(GatewayApplication.class, args);
    }
}
