package com.jk.explore.hexagonal;

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.lang.ArchRule;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;

/**
 * <strong>This file is the architecture.</strong>
 *
 * <p>Not a diagram of an inward-pointing arrow — the arrow itself, in a form
 * a build can check. The core must not depend on any adapter. If the core
 * needs a name, the core declares it, in {@code core.port}; an adapter's job
 * is to reach up and be one, never the other way round.
 *
 * <p>{@code naive} is deliberately outside this test's scope — it holds the
 * version this project argues against, where the core's own use case names
 * three concrete adapters. {@link ArchitectureRuleCatchesTheShortcutTest}
 * runs the same rule over it and asserts it goes red.
 */
class ArchitectureTest {

    private static final String CORE = "com.jk.explore.hexagonal.core";
    private static final String ADAPTER = "com.jk.explore.hexagonal.adapter";
    private static final String DOMAIN = "com.jk.explore.hexagonal.core.domain";
    private static final String PORT = "com.jk.explore.hexagonal.core.port";

    private final JavaClasses everything = new ClassFileImporter()
            .withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
            .importPackages(CORE, ADAPTER);

    @Test
    @DisplayName("the core may not depend on any adapter")
    void coreDoesNotDependOnAdapters() {
        ArchRule rule = noClasses()
                .that().resideInAPackage(CORE + "..")
                .should().dependOnClassesThat().resideInAPackage(ADAPTER + "..")
                .because("a port is defined by the core so an adapter can implement "
                        + "it or call it — the core naming an adapter back would "
                        + "make the dependency point both ways at once");

        rule.check(everything);
    }

    @Test
    @DisplayName("the domain knows nothing about ports, adapters, or the use case")
    void domainDependsOnNothingElse() {
        ArchRule rule = noClasses()
                .that().resideInAPackage(DOMAIN)
                .should().dependOnClassesThat()
                .resideInAnyPackage(PORT, ADAPTER + "..", CORE)
                .because("an order, a price and a line total are true whether or "
                        + "not anything is storing them, charging for them, or "
                        + "calling them from anywhere");

        rule.check(everything);
    }
}
