package com.jk.explore.layered;

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
 * that asserts nothing.
 *
 * <p>So this one points the same rule at {@code naive.presentation}, where
 * {@code OrderHistoryScreen} reaches straight into storage, and asserts that
 * the rule <em>catches it</em>. The failure message is printed, because that
 * message is the whole product: it names the class, names what it reached for,
 * and gives the line number.
 *
 * <p>A reader who takes one thing from this project should take this: "the
 * screen does not touch the database" stopped being something a team promises
 * at a whiteboard and forgets within a month, and became something that fails a
 * build in under a second.
 */
class ArchitectureRuleCatchesTheShortcutTest {

    private final JavaClasses everything = new ClassFileImporter()
            .withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
            .importPackages("com.jk.explore.layered");

    @Test
    @DisplayName("widened to every presentation package, the rule goes red and names the class")
    void theRuleCatchesTheShortcut() {
        // The same sentence as in ArchitectureTest, with one character changed:
        // ".." in front of the package name, so it matches the naive screen too.
        ArchRule rule = noClasses()
                .that().resideInAPackage("..presentation..")
                .should().dependOnClassesThat().resideInAPackage("..infrastructure..")
                .because("a screen that reads storage directly is a screen that has to be "
                        + "opened every time storage changes, and nothing warns you");

        AssertionError failure = assertThrows(AssertionError.class, () -> rule.check(everything));

        assertTrue(failure.getMessage().contains("OrderHistoryScreen"),
                "the message must name the offending class, or nobody can act on it");
        assertTrue(failure.getMessage().contains("InMemoryOrderTable"),
                "and it must name what that class reached for");

        System.out.println("---- the build going red, which is the point ----");
        System.out.println(failure.getMessage());
        System.out.println("------------------------------------------------");
    }
}
