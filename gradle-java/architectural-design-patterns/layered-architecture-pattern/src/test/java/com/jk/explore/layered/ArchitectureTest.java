package com.jk.explore.layered;

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
 * <p>Not a diagram of it, not a description of it — the thing itself, in a form
 * a build can check. Everything else in this project is an arrangement of
 * classes that happens to satisfy these three sentences, and the day somebody
 * stops satisfying them, this test says so by name.
 *
 * <p>That is the difference between a layered architecture and four folders
 * with layered names. The folders are free and decay quietly. These three rules
 * cost about thirty lines and fail loudly.
 *
 * <p>The rules are scoped to the four real layer packages. The {@code naive}
 * packages are deliberately outside that scope, because they hold the versions
 * this project argues against — including one that breaks the first rule on
 * purpose. {@link ArchitectureRuleCatchesTheShortcutTest} runs the same rule
 * over them and asserts it goes red.
 */
class ArchitectureTest {

    private static final String PRESENTATION = "com.jk.explore.layered.presentation";
    private static final String APPLICATION = "com.jk.explore.layered.application";
    private static final String DOMAIN = "com.jk.explore.layered.domain";
    private static final String INFRASTRUCTURE = "com.jk.explore.layered.infrastructure";

    private final JavaClasses layers = new ClassFileImporter()
            .withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
            .importPackages(PRESENTATION, APPLICATION, DOMAIN, INFRASTRUCTURE);

    @Test
    @DisplayName("the screen may not reach past the application layer into storage")
    void presentationMayNotTouchInfrastructure() {
        ArchRule rule = noClasses()
                .that().resideInAPackage(PRESENTATION)
                .should().dependOnClassesThat().resideInAPackage(INFRASTRUCTURE)
                .because("a screen that reads storage directly is a screen that has to be "
                        + "opened every time storage changes, and nothing warns you");

        rule.check(layers);
    }

    @Test
    @DisplayName("the domain knows nothing above it, and nothing below it either")
    void domainDependsOnNoOtherLayer() {
        ArchRule rule = noClasses()
                .that().resideInAPackage(DOMAIN)
                .should().dependOnClassesThat()
                .resideInAnyPackage(PRESENTATION, APPLICATION, INFRASTRUCTURE)
                .because("an order, a price and a line total are true whether or not "
                        + "anybody is storing them or showing them to anyone");

        rule.check(layers);
    }

    @Test
    @DisplayName("storage does not know there is a use case or a screen")
    void infrastructureDependsOnNothingAboveIt() {
        ArchRule rule = noClasses()
                .that().resideInAPackage(INFRASTRUCTURE)
                .should().dependOnClassesThat().resideInAnyPackage(PRESENTATION, APPLICATION)
                .because("the bottom layer is the one most likely to be replaced, and a "
                        + "replacement that has to re-implement the use case is not a "
                        + "replacement");

        rule.check(layers);
    }
}
