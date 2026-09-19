package com.jk.explore.mvpmvvm;

/** MVP: a view that only does what it is told. It makes no decisions. */
public interface CartView {

    void showTotal(String text);

    void showCount(int count);

    void enableCheckout(boolean enabled);
}
