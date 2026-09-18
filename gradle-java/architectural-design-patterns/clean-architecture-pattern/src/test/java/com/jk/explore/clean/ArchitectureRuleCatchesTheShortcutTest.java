package com.jk.explore.clean;

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
 * A green test that has never been seen red is indistinguishable from a
 * test that asserts nothing. This one points the same rule at
 * {@code naive.usecases}, where {@code NaivePlaceOrderInteractor} names
 * three gateways directly, and asserts the rule <em>catches it</em>.
 */
class ArchitectureRuleCatchesTheShortcutTest {

    private final JavaClasses everything = new ClassFileImporter()
            .withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
            .importPackages("com.jk.explore.clean");

    @Test
    @DisplayName("widened to include naive, the rule goes red and names the class")
    void theRuleCatchesTheShortcut() {
        ArchRule rule = noClasses()
                .that().resideInAPackage("..usecases..")
                .should().dependOnClassesThat().resideInAPackage("..adapters..")
                .because("a use case may not depend on an adapter — control flows "
                        + "out through an interface the use case owns, never a "
                        + "dependency on the concrete class behind it");

        AssertionError failure = assertThrows(AssertionError.class, () -> rule.check(everything));

        assertTrue(failure.getMessage().contains("NaivePlaceOrderInteractor"),
                "the message must name the offending class, or nobody can act on it");
        assertTrue(failure.getMessage().contains("InMemoryOrderRepository")
                        || failure.getMessage().contains("InMemoryProductRepository")
                        || failure.getMessage().contains("InMemoryPaymentGateway"),
                "and it must name at least one gateway it reached for");

        System.out.println("---- the build going red, which is the point ----");
        System.out.println(failure.getMessage());
        System.out.println("------------------------------------------------");
    }
}
