package com.jk.explore.dependencyinjection.container;

import java.lang.reflect.Field;

/** What a field-injecting framework does: reach into private fields by reflection. */
public final class Injector {

    private Injector() {
    }

    public static void injectFields(Object target, Object... dependencies) {
        for (Field field : target.getClass().getDeclaredFields()) {
            for (Object dependency : dependencies) {
                if (field.getType().isInstance(dependency)) {
                    try {
                        field.setAccessible(true);
                        field.set(target, dependency);
                    } catch (IllegalAccessException e) {
                        throw new IllegalStateException(e);
                    }
                }
            }
        }
    }
}
