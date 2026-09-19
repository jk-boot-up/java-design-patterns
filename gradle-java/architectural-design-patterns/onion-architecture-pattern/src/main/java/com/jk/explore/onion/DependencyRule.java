package com.jk.explore.onion;

import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

/** Checks the one rule of the onion: a class may only refer to its own ring or to a ring further in. */
public class DependencyRule {

    private static final String BASE = "com.jk.explore.onion.";

    /** 0 is the centre. -1 means not one of ours, such as a Java library class. */
    public static int ring(Class<?> c) {
        String n = c.getName();
        if (n.equals(BASE + "naive.NaiveOrder") || n.startsWith(BASE + "domain.model.")) {
            return 0;
        }
        if (n.startsWith(BASE + "domain.service.")) {
            return 1;
        }
        if (n.startsWith(BASE + "application.")) {
            return 2;
        }
        if (n.startsWith(BASE + "infrastructure.") || n.startsWith(BASE + "ui.")) {
            return 3;
        }
        return -1;
    }

    public static Set<Class<?>> refersTo(Class<?> c) {
        Set<Class<?>> types = new LinkedHashSet<>();
        for (Field f : c.getDeclaredFields()) {
            types.add(f.getType());
        }
        for (Constructor<?> k : c.getDeclaredConstructors()) {
            types.addAll(List.of(k.getParameterTypes()));
        }
        for (Method m : c.getDeclaredMethods()) {
            types.add(m.getReturnType());
            types.addAll(List.of(m.getParameterTypes()));
        }
        return types;
    }

    public static List<String> violations(Class<?>... classes) {
        List<String> found = new ArrayList<>();
        for (Class<?> c : classes) {
            for (Class<?> t : refersTo(c)) {
                if (ring(t) > ring(c) && ring(c) >= 0) {
                    found.add(c.getSimpleName() + " (ring " + ring(c) + ") refers to " + t.getSimpleName() + " (ring " + ring(t) + ")");
                }
            }
        }
        return found;
    }
}
