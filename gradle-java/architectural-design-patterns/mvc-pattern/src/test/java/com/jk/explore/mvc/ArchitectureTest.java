package com.jk.explore.mvc;

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
 * <p>The MVC separation is not the three package names; it is the rule that a
 * view may only ever be handed a finished {@code OrderSummaryModel}. Written
 * as an assertion: no class in the view package may depend on the
 * infrastructure package, because the moment it can, it can reconstruct a
 * price for itself instead of reading the one the model already computed.
 *
 * <p>The {@code naive} package is deliberately outside this test's scope —
 * it holds the version this project argues against, including one view that
 * breaks the rule on purpose. {@link ArchitectureRuleCatchesTheShortcutTest}
 * runs the same rule over it and asserts it goes red.
 */
class ArchitectureTest {

    private static final String VIEW = "com.jk.explore.mvc.view";
    private static final String CONTROLLER = "com.jk.explore.mvc.controller";
    private static final String MODEL = "com.jk.explore.mvc.model";
    private static final String APPLICATION = "com.jk.explore.mvc.application";
    private static final String DOMAIN = "com.jk.explore.mvc.domain";
    private static final String INFRASTRUCTURE = "com.jk.explore.mvc.infrastructure";

    private final JavaClasses layers = new ClassFileImporter()
            .withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
            .importPackages(VIEW, CONTROLLER, MODEL, APPLICATION, DOMAIN, INFRASTRUCTURE);

    @Test
    @DisplayName("a view may not reach past the model into infrastructure")
    void viewMayNotTouchInfrastructure() {
        ArchRule rule = noClasses()
                .that().resideInAPackage(VIEW)
                .should().dependOnClassesThat().resideInAPackage(INFRASTRUCTURE)
                .because("a view that reads the catalogue or storage directly can "
                        + "compute a number the model never agreed to, and nothing "
                        + "would keep two views' numbers the same");

        rule.check(layers);
    }

    @Test
    @DisplayName("the model knows nothing about how it is displayed")
    void modelDoesNotDependOnViewOrController() {
        ArchRule rule = noClasses()
                .that().resideInAPackage(MODEL)
                .should().dependOnClassesThat().resideInAnyPackage(VIEW, CONTROLLER)
                .because("the same model must be renderable by a screen, an email, "
                        + "or anything not yet written, so it cannot know about any "
                        + "of them");

        rule.check(layers);
    }

    @Test
    @DisplayName("the domain knows nothing above it, and nothing below it either")
    void domainDependsOnNoOtherLayer() {
        ArchRule rule = noClasses()
                .that().resideInAPackage(DOMAIN)
                .should().dependOnClassesThat()
                .resideInAnyPackage(VIEW, CONTROLLER, MODEL, APPLICATION, INFRASTRUCTURE)
                .because("an order, a price and a line total are true whether or "
                        + "not anybody is displaying them or storing them");

        rule.check(layers);
    }
}
