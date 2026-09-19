package com.jk.explore.fluent;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;
import org.junit.jupiter.api.Test;

class FluentTest {

    @Test
    void theFluentAndPositionalCallsAgree() {
        assertEquals(Catalog.find("mugs", 2500, true, true, 10),
                Query.search().category("mugs").under(2500).inStock().cheapestFirst().first(10).run());
        assertEquals(List.of("Blue Mug", "Big Mug"), Query.search().category("mugs").under(2500).inStock().cheapestFirst().run());
    }

    @Test
    void swappedBooleansCompileAndChangeTheAnswer() {
        assertNotEquals(Catalog.find("mugs", 2500, true, true, 10), Catalog.find("mugs", 2500, false, true, 10));
    }

    @Test
    void optionalPartsCanComeInAnyOrder() {
        assertEquals(Query.search().category("mugs").under(2500).inStock().run(),
                Query.search().inStock().under(2500).category("mugs").run());
    }

    @Test
    void anUnchangingQueryCanBeReused() {
        Query mugs = Query.search().category("mugs");
        assertEquals(List.of("Blue Mug"), mugs.under(1000).run());
        assertEquals(List.of("Blue Mug", "Big Mug", "Gift Mug"), mugs.under(3000).run());
        assertEquals(4, mugs.run().size());
    }

    @Test
    void aSelfChangingQueryIsSpoiledBySharing() {
        MutableQuery base = new MutableQuery().category("mugs");
        MutableQuery cheap = base.under(1000);
        base.under(3000);
        assertSame(base, cheap);
        assertEquals(3, cheap.run().size());
    }

    @Test
    void guidedStepsOfferOnlyWhatMayComeNext() {
        assertEquals(List.of("category"), FluentDemo.methodNames(Steps.NeedsCategory.class));
        assertEquals(List.of("under"), FluentDemo.methodNames(Steps.NeedsMax.class));
        assertEquals(List.of("cheapestFirst", "inStock", "run"), FluentDemo.methodNames(Steps.Ready.class));
    }

    @Test
    void aBadValueIsOnlyFoundAtRun() {
        Query q = Query.search().under(-5);
        assertThrows(IllegalStateException.class, q::run);
    }
}
