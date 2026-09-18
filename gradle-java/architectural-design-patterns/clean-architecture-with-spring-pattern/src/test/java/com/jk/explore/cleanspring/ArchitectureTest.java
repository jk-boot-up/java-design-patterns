package com.jk.explore.cleanspring;

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.library.Architectures;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * <strong>The same rule as {@code clean-architecture-pattern}, because
 * {@code entities}, {@code usecases} and {@code adapters} here are the
 * identical files.</strong> Spring appears only in {@code config} and in
 * {@link Application} — deliberately excluded from this scan, exactly as
 * the composition root was excluded from the hand-wired project's own
 * architecture test.
 */
class ArchitectureTest {

    private final JavaClasses classes = new ClassFileImporter()
            .withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
            .importPackages("com.jk.explore.cleanspring.entities",
                    "com.jk.explore.cleanspring.usecases", "com.jk.explore.cleanspring.adapters");

    @Test
    @DisplayName("source code dependencies point only inward")
    void dependenciesPointOnlyInward() {
        Architectures.layeredArchitecture()
                .consideringOnlyDependenciesInLayers()
                .layer("Entities").definedBy("com.jk.explore.cleanspring.entities..")
                .layer("UseCases").definedBy("com.jk.explore.cleanspring.usecases..")
                .layer("Adapters").definedBy("com.jk.explore.cleanspring.adapters..")
                .whereLayer("Entities").mayOnlyBeAccessedByLayers("UseCases", "Adapters")
                .whereLayer("UseCases").mayOnlyBeAccessedByLayers("Adapters")
                .because("control may flow outward through an interface, but the "
                        + "source code dependency it creates must point inward, "
                        + "toward the layer that declared the interface")
                .check(classes);
    }

    @Test
    @DisplayName("Spring appears nowhere in entities, use cases or adapters")
    void springAppearsOnlyInConfig() {
        com.tngtech.archunit.lang.ArchRule rule =
                com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses()
                .should().dependOnClassesThat().resideInAPackage("org.springframework..")
                .because("§66's entities, use cases and adapters are copied "
                        + "unchanged; if any of them needed a Spring import to "
                        + "compile, they would no longer be the same files");

        rule.check(classes);
    }
}
