package com.jk.explore.typeobject;

import com.jk.explore.typeobject.naive.Book;
import com.jk.explore.typeobject.naive.Grocery;
import com.jk.explore.typeobject.naive.KindProduct;
import com.jk.explore.typeobject.naive.Laptop;
import java.util.List;

public class TypeObjectDemo {

    static TypeRegistry shopTypes() {
        TypeRegistry types = new TypeRegistry();
        types.define("book", 0, 30, 300);
        types.define("laptop", 20, 14, 0).requireSerial();
        types.define("grocery", 5, 0, 200);
        return types;
    }

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. A class for each kind.");
        List<Class<? extends KindProduct>> kinds = List.of(Book.class, Laptop.class, Grocery.class);
        System.out.println("  " + kinds.size() + " kinds, " + kinds.size() + " classes, and they differ only in three numbers. a novel: " + new Book(1000).totalCents() + ".");
        System.out.println("  a gift card is a fourth kind. that is a fourth class, a new build and a release.");
    }

    private static void two() {
        System.out.println("TWO. A type that is data.");
        TypeRegistry types = shopTypes();
        Product novel = new Product("Novel", 1000, types.of("book"));
        Product laptop = new Product("Laptop", 80000, types.of("laptop"));
        Product tea = new Product("Tea", 400, types.of("grocery"));
        System.out.println("  one Product class. novel " + novel.totalCents() + ", laptop " + laptop.totalCents() + ", tea " + tea.totalCents() + ".");
        System.out.println("  laptops can be returned after 10 days: " + laptop.canReturn(10) + ". after 20 days: " + laptop.canReturn(20) + ".");
    }

    private static void three() {
        System.out.println("THREE. A new kind at run time.");
        TypeRegistry types = shopTypes();
        int before = types.count();
        types.define("gift-card", 0, 0, 0);
        Product card = new Product("25 pound card", 2500, types.of("gift-card"));
        System.out.println("  types before " + before + ", after " + types.count() + ". classes added: 0. a 25 pound card totals " + card.totalCents() + ", and can be returned after 1 day: " + card.canReturn(1) + ".");
    }

    private static void four() {
        System.out.println("FOUR. Change the type, change every product.");
        TypeRegistry types = shopTypes();
        Product tea = new Product("Tea", 400, types.of("grocery"));
        Product coffee = new Product("Coffee", 800, types.of("grocery"));
        System.out.println("  tax on tea " + tea.taxCents() + ", on coffee " + coffee.taxCents() + ".");
        types.of("grocery").setTaxPercent(10);
        System.out.println("  grocery tax raised to 10 percent, in one place. tea " + tea.taxCents() + ", coffee " + coffee.taxCents() + ".");
    }

    private static void five() {
        System.out.println("FIVE. A type that inherits.");
        TypeRegistry types = shopTypes();
        types.derive("ebook", "book", null, null, 0);
        ProductType ebook = types.of("ebook");
        System.out.println("  ebook states only its shipping: " + ebook.shippingCents() + ". tax " + ebook.taxPercent() + " and return days " + ebook.returnDays() + " come from book.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        TypeRegistry types = shopTypes();
        try {
            types.of("bok");
        } catch (IllegalArgumentException e) {
            System.out.println("  a typo, \"bok\": " + e.getMessage() + ", found when it runs. with a class for each kind, the typo would not compile.");
        }
        System.out.println("  laptops need a serial number checked, and a type holds data, not steps. the flag says so: requiresSerial " + types.of("laptop").requiresSerial() + ". the code that checks it is still somewhere else.");
        System.out.println("  every new difference between kinds is a new field, and every field is a thing the code must remember to read. the type has " + ProductType.class.getDeclaredFields().length + " fields already.");
    }
}
