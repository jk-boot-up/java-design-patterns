package com.jk.explore.cleanspring;

import com.jk.explore.cleanspring.config.AppConfig;
import com.jk.explore.cleanspring.config.BrokenAppConfig;
import com.jk.explore.cleanspring.usecases.PlaceOrderInputBoundary;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.UnsatisfiedDependencyException;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * This project's one owned contrast, proven rather than narrated:
 * hand-wiring fails at compile time, container wiring fails at startup.
 *
 * <p>{@code BrokenAppConfig} is deliberately not exercised by trying to
 * compile a hand-wired equivalent missing an argument — that failure is
 * demonstrated in {@code clean-architecture-pattern} itself, at edit time,
 * and cannot be captured as a passing test here. What this test proves is
 * the other half: that the identical mistake, expressed as a missing
 * {@code @Bean}, compiles perfectly and only fails once a context is
 * actually built.
 */
class WiringContrastTest {

    @Test
    void theRealConfigWiresEveryBean() {
        AnnotationConfigApplicationContext context =
                new AnnotationConfigApplicationContext(AppConfig.class);

        assertNotNull(context.getBean(PlaceOrderInputBoundary.class));

        context.close();
    }

    @Test
    void theBrokenConfigCompilesCleanlyAndFailsOnlyAtStartup() {
        UnsatisfiedDependencyException failure = assertThrows(
                UnsatisfiedDependencyException.class,
                () -> new AnnotationConfigApplicationContext(BrokenAppConfig.class));

        assertTrue(failure.getMessage().contains("NotificationGateway"),
                "the failure must name the missing bean's type, or nobody can act on it");
    }
}
