package com.jk.explore.dependencyinjection.container;

import java.lang.reflect.Constructor;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * <strong>A dependency-injection container, under a hundred lines.</strong> It does
 * exactly what the hand-written wiring did: for each class, look at the
 * constructor's parameter types, find or build something for each, and call
 * it. It builds everything when it starts, so a graph that cannot be built
 * fails immediately, which is better than at the first request, and still not
 * at compile time.
 */
public final class MiniContainer {

    private final List<Class<?>> beanClasses = new ArrayList<>();
    private final Map<Class<?>, Object> built = new HashMap<>();

    private MiniContainer() {
    }

    public static MiniContainer start(Class<?>... beans) {
        MiniContainer container = new MiniContainer();
        container.beanClasses.addAll(List.of(beans));
        for (Class<?> bean : beans) {
            container.build(bean, new ArrayDeque<>());
        }
        return container;
    }

    public <T> T get(Class<T> type) {
        for (Object bean : built.values()) {
            if (type.isInstance(bean)) {
                return type.cast(bean);
            }
        }
        throw new ContainerFailure("no bean for " + type.getSimpleName());
    }

    private Object build(Class<?> type, Deque<Class<?>> path) {
        Object existing = built.get(type);
        if (existing != null) {
            return existing;
        }
        if (path.contains(type)) {
            throw new ContainerFailure("circular dependency: " + describe(path, type));
        }
        path.push(type);
        Constructor<?> constructor = type.getConstructors()[0];
        Object[] arguments = new Object[constructor.getParameterCount()];
        Class<?>[] parameterTypes = constructor.getParameterTypes();
        for (int i = 0; i < arguments.length; i++) {
            arguments[i] = build(find(parameterTypes[i], type), path);
        }
        path.pop();
        try {
            Object made = constructor.newInstance(arguments);
            built.put(type, made);
            return made;
        } catch (ReflectiveOperationException e) {
            throw new ContainerFailure("could not construct " + type.getSimpleName() + ": " + e.getMessage());
        }
    }

    private Class<?> find(Class<?> wanted, Class<?> needer) {
        for (Class<?> candidate : beanClasses) {
            if (wanted.isAssignableFrom(candidate)) {
                return candidate;
            }
        }
        throw new ContainerFailure("could not construct " + needer.getSimpleName()
                + ": no bean for its parameter of type " + wanted.getSimpleName());
    }

    private static String describe(Deque<Class<?>> path, Class<?> again) {
        List<String> names = new ArrayList<>();
        path.descendingIterator().forEachRemaining(c -> names.add(c.getSimpleName()));
        names.add(again.getSimpleName());
        return String.join(" -> ", names);
    }
}
