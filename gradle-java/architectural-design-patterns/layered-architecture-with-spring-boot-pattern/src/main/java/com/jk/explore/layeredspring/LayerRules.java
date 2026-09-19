package com.jk.explore.layeredspring;

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.lang.EvaluationResult;
import com.tngtech.archunit.library.Architectures;

/**
 * The layering rule, written down where a machine can check it. Spring does not enforce it:
 * a controller may inject a repository and the application starts.
 */
public final class LayerRules {

    private static final String ROOT = "com.jk.explore.layeredspring";

    private LayerRules() {
    }

    public static Architectures.LayeredArchitecture rule() {
        return Architectures.layeredArchitecture().consideringOnlyDependenciesInLayers()
                .layer("Presentation").definedBy(ROOT + ".presentation..", ROOT + ".naive..")
                .layer("Application").definedBy(ROOT + ".application..")
                .layer("Infrastructure").definedBy(ROOT + ".infrastructure..")
                .layer("Domain").definedBy(ROOT + ".domain..")
                .whereLayer("Presentation").mayNotBeAccessedByAnyLayer()
                .whereLayer("Application").mayOnlyBeAccessedByLayers("Presentation")
                .whereLayer("Infrastructure").mayOnlyBeAccessedByLayers("Application")
                .whereLayer("Domain").mayOnlyBeAccessedByLayers("Presentation", "Application", "Infrastructure");
    }

    /** Checks every class in the project, the shortcut included, and returns the rule's verdict. */
    public static EvaluationResult check() {
        JavaClasses classes = new ClassFileImporter()
                .withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
                .importPackages(ROOT);
        return rule().evaluate(classes);
    }
}
