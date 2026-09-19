package com.jk.explore.typeobject;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.jk.explore.typeobject.naive.Book;
import org.junit.jupiter.api.Test;

class TypeObjectTest {

    @Test
    void theSubclassAndTheTypeObjectAgree() {
        TypeRegistry types = TypeObjectDemo.shopTypes();
        assertEquals(new Book(1000).totalCents(), new Product("Novel", 1000, types.of("book")).totalCents());
    }

    @Test
    void oneClassGivesDifferentResultsByType() {
        TypeRegistry types = TypeObjectDemo.shopTypes();
        assertEquals(1300, new Product("Novel", 1000, types.of("book")).totalCents());
        assertEquals(96000, new Product("Laptop", 80000, types.of("laptop")).totalCents());
        assertEquals(620, new Product("Tea", 400, types.of("grocery")).totalCents());
    }

    @Test
    void returnWindowsComeFromTheType() {
        TypeRegistry types = TypeObjectDemo.shopTypes();
        Product laptop = new Product("Laptop", 80000, types.of("laptop"));
        assertTrue(laptop.canReturn(10));
        assertFalse(laptop.canReturn(20));
    }

    @Test
    void aNewTypeNeedsNoNewClass() {
        TypeRegistry types = TypeObjectDemo.shopTypes();
        types.define("gift-card", 0, 0, 0);
        Product card = new Product("card", 2500, types.of("gift-card"));
        assertEquals(2500, card.totalCents());
        assertFalse(card.canReturn(1));
    }

    @Test
    void changingATypeChangesEveryProductOfIt() {
        TypeRegistry types = TypeObjectDemo.shopTypes();
        Product tea = new Product("Tea", 400, types.of("grocery"));
        Product coffee = new Product("Coffee", 800, types.of("grocery"));
        types.of("grocery").setTaxPercent(10);
        assertEquals(40, tea.taxCents());
        assertEquals(80, coffee.taxCents());
    }

    @Test
    void aDerivedTypeInheritsWhatItDoesNotState() {
        TypeRegistry types = TypeObjectDemo.shopTypes();
        types.derive("ebook", "book", null, null, 0);
        ProductType ebook = types.of("ebook");
        assertEquals(0, ebook.shippingCents());
        assertEquals(30, ebook.returnDays());
        assertEquals(0, ebook.taxPercent());
    }

    @Test
    void anUnknownTypeIsRefusedAtRunTime() {
        assertThrows(IllegalArgumentException.class, () -> TypeObjectDemo.shopTypes().of("bok"));
    }
}
