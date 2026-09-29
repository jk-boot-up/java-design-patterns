package com.jk.explore.markerinterface;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: free-text tags, marker interfaces, the compiler checking, marks passed on, and the bill.
 */
public final class MarkerInterfaceDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. Care instructions as free-text tags.");
        List<TaggedProduct> tagged = List.of(
                new TaggedProduct("MILK-1", List.of("perishable")),
                new TaggedProduct("MILK-2", List.of("Perishable")),
                new TaggedProduct("CREAM-1", List.of("perishible")));
        tagged.forEach(t -> out.add("  " + t.pack() + "   tags " + t.tags()));
        out.add("  two of three dairy products shipped warm; nothing complained");

        out.add("");
        out.add("TWO. A marker interface: the type says it.");
        List<Products.Product> basket = List.of(new Products.Milk("MILK-1"), new Products.Mug("MUG-1"),
                new Products.Kettle("KETTLE-1"));
        basket.forEach(p -> out.add("  " + Packer.pack(p)));
        out.add("  Perishable has " + Markers.Perishable.class.getDeclaredMethods().length
                + " methods; a misspelt name would not compile");

        out.add("");
        out.add("THREE. The compiler checks who can use the chilled courier.");
        out.add("  " + Packer.sendChilled(new Products.Milk("MILK-1")));
        out.add("  Packer.sendChilled(kettle) does not compile: a kettle is not Perishable");

        out.add("");
        out.add("FOUR. The mark is passed on to subclasses.");
        Products.Yoghurt multipack = new Products.YoghurtMultipack("YOG-6");
        out.add("  " + Packer.pack(multipack) + "  (its team never wrote Perishable)");

        out.add("");
        out.add("FIVE. The bill: a marker says yes or no, nothing more.");
        out.add("  it cannot say how cold: that needs a method, or an annotation like @Chilled(maxC = 5)");
        out.add("  and a subclass cannot take the mark off: a dried yoghurt snack would still get ice packs");
        return out;
    }

    private MarkerInterfaceDemo() {
    }
}
