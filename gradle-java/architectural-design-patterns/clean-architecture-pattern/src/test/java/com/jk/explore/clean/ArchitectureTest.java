package com.jk.explore.clean;

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.library.Architectures;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * <strong>This file is the architecture.</strong>
 *
 * <p>Not three separate rules bolted together — one sentence, expressed in
 * ArchUnit's own purpose-built API for exactly this shape:
 * {@code Architectures.layeredArchitecture()}. Three layers, one rule
 * repeated between each adjacent pair: <em>source code dependencies point
 * only inward.</em> Entities may be reached by use cases and adapters, but
 * reach neither. Use cases may be reached by adapters, but reach only
 * entities.
 *
 * <p>{@code naive} is deliberately outside this test's scope — it holds the
 * version this project argues against, where a class calling itself a use
 * case reaches straight through the adapters layer.
 * {@link ArchitectureRuleCatchesTheShortcutTest} runs the same shape of
 * rule over it and asserts it goes red.
 */
class ArchitectureTest {

    private final JavaClasses classes = new ClassFileImporter()
            .withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
            .importPackages("com.jk.explore.clean.entities",
                    "com.jk.explore.clean.usecases", "com.jk.explore.clean.adapters");

    @Test
    @DisplayName("source code dependencies point only inward")
    void dependenciesPointOnlyInward() {
        Architectures.layeredArchitecture()
                .consideringOnlyDependenciesInLayers()
                .layer("Entities").definedBy("com.jk.explore.clean.entities..")
                .layer("UseCases").definedBy("com.jk.explore.clean.usecases..")
                .layer("Adapters").definedBy("com.jk.explore.clean.adapters..")
                .whereLayer("Entities").mayOnlyBeAccessedByLayers("UseCases", "Adapters")
                .whereLayer("UseCases").mayOnlyBeAccessedByLayers("Adapters")
                .because("control may flow outward through an interface, but the "
                        + "source code dependency it creates must point inward, "
                        + "toward the layer that declared the interface")
                .check(classes);
    }
}
