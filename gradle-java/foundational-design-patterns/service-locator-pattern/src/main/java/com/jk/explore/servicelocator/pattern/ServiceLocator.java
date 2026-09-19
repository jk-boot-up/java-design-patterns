package com.jk.explore.servicelocator.pattern;

import java.util.HashMap;
import java.util.Map;
import java.util.function.Supplier;

/**
 * <strong>A middleman that knows how to find or create what you ask for.</strong>
 * Unlike a registry, which is a bag of things someone remembered to put in, a
 * locator holds <em>recipes</em>: it can create lazily, decide how long a thing
 * lives, and be reconfigured for a test. That is the genuine advance.
 *
 * <p>It is still a static, and every class that uses it still <em>asks</em>.
 */
public final class ServiceLocator {

    private record Recipe(Supplier<?> factory, boolean shared) {
    }

    private static final Map<Class<?>, Recipe> RECIPES = new HashMap<>();
    private static final Map<Class<?>, Object> SHARED = new HashMap<>();

    private ServiceLocator() {
    }

    /** One instance, created the first time it is asked for. */
    public static <T> void singleton(Class<T> type, Supplier<? extends T> factory) {
        RECIPES.put(type, new Recipe(factory, true));
        SHARED.remove(type);
    }

    /** A new instance every time it is asked for. */
    public static <T> void prototype(Class<T> type, Supplier<? extends T> factory) {
        RECIPES.put(type, new Recipe(factory, false));
        SHARED.remove(type);
    }

    public static <T> T find(Class<T> type) {
        Recipe recipe = RECIPES.get(type);
        if (recipe == null) {
            throw new IllegalStateException("no service is configured for " + type.getSimpleName());
        }
        if (!recipe.shared()) {
            return type.cast(recipe.factory().get());
        }
        return type.cast(SHARED.computeIfAbsent(type, t -> recipe.factory().get()));
    }

    public static void reset() {
        RECIPES.clear();
        SHARED.clear();
    }

    public static boolean isConfigured(Class<?> type) {
        return RECIPES.containsKey(type);
    }
}
