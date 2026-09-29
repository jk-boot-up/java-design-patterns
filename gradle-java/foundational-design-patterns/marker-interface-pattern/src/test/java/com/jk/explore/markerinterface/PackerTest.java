package com.jk.explore.markerinterface;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;

import java.util.List;
import org.junit.jupiter.api.Test;

class PackerTest {

    @Test
    void perishableGetsIce() {
        assertEquals("M: ice packs", Packer.pack(new Products.Milk("M")));
    }

    @Test
    void fragileGetsWrap() {
        assertEquals("G: bubble wrap", Packer.pack(new Products.Mug("G")));
    }

    @Test
    void unmarkedGetsPlainBox() {
        assertEquals("K: plain box", Packer.pack(new Products.Kettle("K")));
    }

    @Test
    void markIsInherited() {
        assertInstanceOf(Markers.Perishable.class, new Products.YoghurtMultipack("Y"));
    }

    @Test
    void tagsOnlyMatchExactSpelling() {
        assertEquals("C: plain box", new TaggedProduct("C", List.of("Perishable")).pack());
    }

    @Test
    void markersAreEmpty() {
        assertEquals(0, Markers.Perishable.class.getDeclaredMethods().length);
        assertEquals(0, Markers.Fragile.class.getDeclaredMethods().length);
    }
}
