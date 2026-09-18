package com.jk.explore.mvc;

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
 * that asserts nothing. This one points the same rule at
 * {@code naive.view}, where {@code RoundedEmailView} reaches straight into
 * the catalogue, and asserts the rule <em>catches it</em>.
 */
class ArchitectureRuleCatchesTheShortcutTest {

    private final JavaClasses everything = new ClassFileImporter()
            .withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
            .importPackages("com.jk.explore.mvc");

    @Test
    @DisplayName("widened to every view package, the rule goes red and names the class")
    void theRuleCatchesTheShortcut() {
        ArchRule rule = noClasses()
                .that().resideInAPackage("..view..")
                .should().dependOnClassesThat().resideInAPackage("..infrastructure..")
                .because("a view that reads the catalogue or storage directly can "
                        + "compute a number the model never agreed to, and nothing "
                        + "would keep two views' numbers the same");

        AssertionError failure = assertThrows(AssertionError.class, () -> rule.check(everything));

        assertTrue(failure.getMessage().contains("RoundedEmailView"),
                "the message must name the offending class, or nobody can act on it");
        assertTrue(failure.getMessage().contains("ProductTable"),
                "and it must name what that class reached for");

        System.out.println("---- the build going red, which is the point ----");
        System.out.println(failure.getMessage());
        System.out.println("------------------------------------------------");
    }
}
