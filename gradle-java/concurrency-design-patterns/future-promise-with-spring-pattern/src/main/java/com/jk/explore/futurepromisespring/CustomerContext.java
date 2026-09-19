package com.jk.explore.futurepromisespring;

/** "Whose order is this?" held in a ThreadLocal, the way security and request context are held. */
public final class CustomerContext {

    private static final ThreadLocal<Integer> CURRENT = new ThreadLocal<>();

    private CustomerContext() {
    }

    public static void set(Integer customerId) {
        CURRENT.set(customerId);
    }

    public static Integer get() {
        return CURRENT.get();
    }

    public static void clear() {
        CURRENT.remove();
    }
}
