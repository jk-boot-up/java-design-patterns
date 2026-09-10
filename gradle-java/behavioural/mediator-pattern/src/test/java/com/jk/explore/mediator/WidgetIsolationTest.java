package com.jk.explore.mediator;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * The structural claim of the pattern, made into an assertion.
 *
 * <p>Everything else in this project can be believed by reading the code. This
 * test is here because the promise "a widget knows the mediator and nothing
 * else" is the sort of thing that quietly stops being true the first time
 * somebody is in a hurry, and a comment cannot stop that.
 */
class WidgetIsolationTest {

    @Test
    @DisplayName("no widget holds a reference to another widget")
    void widgetsOnlyKnowTheMediator() {
        CheckoutForm form = new CheckoutForm();
        List<FormWidget> widgets = List.of(
                form.country(), form.shipping(), form.giftWrap(),
                form.total(), form.placeOrder());

        List<String> offenders = new ArrayList<>();
        for (FormWidget widget : widgets) {
            for (Field field : allFieldsOf(widget.getClass())) {
                if (FormWidget.class.isAssignableFrom(field.getType())) {
                    offenders.add(widget.name() + "." + field.getName());
                }
            }
        }

        assertEquals(List.of(), offenders,
                "these fields point at another widget instead of at the mediator");
    }

    @Test
    @DisplayName("the tangled form, for contrast, is full of such references")
    void naiveWidgetsKnowEachOther() {
        long crossReferences = List.of(
                        NaiveCheckoutForm.NaiveCountry.class,
                        NaiveCheckoutForm.NaiveShipping.class,
                        NaiveCheckoutForm.NaiveGiftWrap.class).stream()
                .flatMap(type -> List.of(type.getDeclaredFields()).stream())
                .filter(field -> field.getType().getName().contains("Naive"))
                .count();

        // country -> 4, shipping -> 3, giftWrap -> 2.
        assertEquals(9, crossReferences);
        assertTrue(crossReferences > 0);
    }

    /** Walks up to FormWidget, whose own mediator field is the allowed one. */
    private static List<Field> allFieldsOf(Class<?> type) {
        List<Field> fields = new ArrayList<>();
        for (Class<?> c = type; c != null && c != Object.class; c = c.getSuperclass()) {
            fields.addAll(List.of(c.getDeclaredFields()));
        }
        return fields;
    }
}
