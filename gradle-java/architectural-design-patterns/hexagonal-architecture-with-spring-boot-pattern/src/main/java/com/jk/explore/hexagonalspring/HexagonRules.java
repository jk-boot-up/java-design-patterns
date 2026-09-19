package com.jk.explore.hexagonalspring;

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.lang.EvaluationResult;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;

/** The rule that makes the hexagon a hexagon: what is inside may not know about the framework, or about the adapters. */
public final class HexagonRules {

    private static final String ROOT = "com.jk.explore.hexagonalspring";

    private HexagonRules() {
    }

    /** Checks every class in the project, treating the shortcut as if it lived in the core. */
    public static EvaluationResult checkInsideKnowsNoFramework() {
        JavaClasses classes = new ClassFileImporter()
                .withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
                .importPackages(ROOT);
        return noClasses().that().resideInAnyPackage(ROOT + ".core..", ROOT + ".naive..")
                .should().dependOnClassesThat().resideInAnyPackage("org.springframework..", ROOT + ".adapter..", ROOT + ".config..")
                .evaluate(classes);
    }
}
