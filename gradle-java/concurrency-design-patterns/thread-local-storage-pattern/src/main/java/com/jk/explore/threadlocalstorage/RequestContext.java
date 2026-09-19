package com.jk.explore.threadlocalstorage;

/** Who the current request is for. Each thread has its own, set at the door and read anywhere below it. */
public final class RequestContext {

    private static final ThreadLocal<String> CUSTOMER = new ThreadLocal<>();

    private RequestContext() {
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

    /** Runs the work with the context set, and always clears it afterwards, whatever happens. */
    public static <T> T with(String customer, java.util.function.Supplier<T> work) {
        set(customer);
        try {
            return work.get();
        } finally {
            clear();
        }
    }
}
