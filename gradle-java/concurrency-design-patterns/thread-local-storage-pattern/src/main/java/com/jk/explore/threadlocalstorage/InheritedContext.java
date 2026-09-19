package com.jk.explore.threadlocalstorage;

/** As RequestContext, but a thread created by a thread that has a value starts with a copy of it. */
public final class InheritedContext {

    private static final InheritableThreadLocal<String> CUSTOMER = new InheritableThreadLocal<>();

    private InheritedContext() {
    }

    public static void set(String customer) {
        CUSTOMER.set(customer);
    }

    public static String customer() {
        return CUSTOMER.get();
    }

    public static void clear() {
        CUSTOMER.remove();
    }
}
