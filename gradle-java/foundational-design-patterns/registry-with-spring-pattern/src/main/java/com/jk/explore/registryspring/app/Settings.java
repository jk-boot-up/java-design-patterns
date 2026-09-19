package com.jk.explore.registryspring.app;

import org.springframework.beans.factory.annotation.Value;

/** Reads a property with {@code @Value}. Not a component: created only in the act that needs it. */
public class Settings {

    @Value("${checkout.curency}")
    private String currency;

    public String currency() {
        return currency;
    }
}
