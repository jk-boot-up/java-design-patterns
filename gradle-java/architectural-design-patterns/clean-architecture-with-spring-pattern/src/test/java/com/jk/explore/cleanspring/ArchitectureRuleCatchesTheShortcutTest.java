package com.jk.explore.cleanspring;

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.lang.ArchRule;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** Same shortcut, same catch, as {@code clean-architecture-pattern}. */
class ArchitectureRuleCatchesTheShortcutTest {

    private final JavaClasses everything = new ClassFileImporter()
            .withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
            .importPackages("com.jk.explore.cleanspring");

    @Test
    @DisplayName("widened to include naive, the rule goes red and names the class")
    void theRuleCatchesTheShortcut() {
        ArchRule rule = noClasses()
                .that().resideInAPackage("..usecases..")
                .should().dependOnClassesThat().resideInAPackage("..adapters..")
                .because("a use case may not depend on an adapter");

        AssertionError failure = assertThrows(AssertionError.class, () -> rule.check(everything));

        assertTrue(failure.getMessage().contains("NaivePlaceOrderInteractor"));
        assertTrue(failure.getMessage().contains("InMemoryOrderRepository")
                || failure.getMessage().contains("InMemoryProductRepository")
                || failure.getMessage().contains("InMemoryPaymentGateway"));
    }
}
