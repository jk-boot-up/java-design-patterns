package com.jk.explore.authzspring;

import java.util.Map;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Component;

/**
 * The part of the policy that needs the shop's own data: who owns which order. Rules call it by name.
 */
@Component("orderPolicy")
public class OrderPolicy {

    static final Map<String, String> OWNER = Map.of("ORD-7", "ben", "ORD-8", "ana");

    public boolean owns(Authentication user, String orderId) {
        return user.getName().equals(OWNER.get(orderId));
    }
}
