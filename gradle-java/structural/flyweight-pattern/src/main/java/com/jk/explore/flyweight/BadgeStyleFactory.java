package com.jk.explore.flyweight;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * The flyweight factory. Every call to {@link #styleFor(BadgeType)} for the
 * same type returns the exact same {@link BadgeStyle} instance, no matter
 * how many listings — or how many threads — ask for it.
 *
 * <p>{@link #instancesCreated()} exists only so the demo and the tests can
 * prove that: it counts real constructions, not lookups, so it should stop
 * climbing after the first call for each of the four badge types.
 */
public final class BadgeStyleFactory {

    private static final Map<BadgeType, BadgeStyle> CACHE = new ConcurrentHashMap<>();
    private static final AtomicInteger INSTANCES_CREATED = new AtomicInteger();

    private BadgeStyleFactory() {
    }

    public static BadgeStyle styleFor(BadgeType type) {
        return CACHE.computeIfAbsent(type, BadgeStyleFactory::build);
    }

    public static int instancesCreated() {
        return INSTANCES_CREATED.get();
    }

    private static BadgeStyle build(BadgeType type) {
        INSTANCES_CREATED.incrementAndGet();
        return switch (type) {
            case NEW -> new BadgeStyle(type, "✨", "#2563EB", "#FFFFFF", false);
            case SALE -> new BadgeStyle(type, "★", "#DC2626", "#FFFFFF", true);
            case BESTSELLER -> new BadgeStyle(type, "👑", "#D97706", "#111827", true);
            case LOW_STOCK -> new BadgeStyle(type, "⚠", "#6B7280", "#FFFFFF", false);
        };
    }
}
