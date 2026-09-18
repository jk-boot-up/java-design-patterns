package com.jk.explore.hexagonal;

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.lang.ArchRule;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * A green test that has never been seen red is indistinguishable from a test
 * that asserts nothing. This one points the same rule at {@code naive},
 * where {@code NaivePlaceOrderService} names three adapters directly, and
 * asserts the rule <em>catches it</em>.
 */
class ArchitectureRuleCatchesTheShortcutTest {

    private final JavaClasses everything = new ClassFileImporter()
            .withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
            .importPackages("com.jk.explore.hexagonal");

    @Test
    @DisplayName("widened to include naive, the rule goes red and names the class")
    void theRuleCatchesTheShortcut() {
        ArchRule rule = noClasses()
                .that().resideInAPackage("..core..")
                .should().dependOnClassesThat().resideInAPackage("..adapter..")
                .because("a port is defined by the core so an adapter can implement "
                        + "it or call it — the core naming an adapter back would "
                        + "make the dependency point both ways at once");

        AssertionError failure = assertThrows(AssertionError.class, () -> rule.check(everything));

        assertTrue(failure.getMessage().contains("NaivePlaceOrderService"),
                "the message must name the offending class, or nobody can act on it");
        assertTrue(failure.getMessage().contains("InMemoryOrderStore")
                        || failure.getMessage().contains("InMemoryProductCatalog")
                        || failure.getMessage().contains("InMemoryPaymentGateway"),
                "and it must name at least one adapter it reached for");

        System.out.println("---- the build going red, which is the point ----");
        System.out.println(failure.getMessage());
        System.out.println("------------------------------------------------");
    }
}
