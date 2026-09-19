package com.jk.explore.mvpmvvm;

import java.util.ArrayList;
import java.util.List;

/** A view for tests and demos: it writes down what it was told, and draws nothing. */
public class RecordingView implements CartView {

    private final List<String> told = new ArrayList<>();

    @Override
    public void showTotal(String text) {
        told.add("showTotal " + text);
    }

    @Override
    public void showCount(int count) {
        told.add("showCount " + count);
    }

    @Override
    public void enableCheckout(boolean enabled) {
        told.add("enableCheckout " + enabled);
    }

    public List<String> told() {
        return List.copyOf(told);
    }

    public void clear() {
        told.clear();
    }
}
