package com.jk.explore.command;

/**
 * Runnable walkthrough: {@code ./gradlew run}.
 *
 * <p>Five sections. The first shows hand-rolled undo getting the
 * interesting case wrong; the rest show the same edits as commands, undone
 * and redone, and the audit trail that falls out of having reified them.
 */
public final class CartCommandsDemo {

    private static final Money HEADPHONES = Money.pounds(89.99);
    private static final Money CABLE = Money.pounds(7.50);
    private static final Money CASE = Money.pounds(24.00);

    private CartCommandsDemo() {
    }

    public static void main(String[] args) {
        theTrap();
        theCommands();
        undoAndRedo();
        theHardUndo();
        theAuditTrail();
    }

    private static void theTrap() {
        heading("1. The trap: undo notes that record the request, not the cart");

        Cart cart = new Cart();
        NaiveCartEditor editor = new NaiveCartEditor(cart);

        editor.addItem("H-100", "Wireless headphones", HEADPHONES, 3);
        editor.applyCoupon(new Coupon("WELCOME10", 10));
        System.out.println("  The customer has 3 headphones and a 10% code:");
        System.out.print(cart.describe());

        editor.addItem("H-100", "Wireless headphones", HEADPHONES, 2);
        editor.applyCoupon(new Coupon("BLACKFRIDAY", 25));
        System.out.println("\n  They add 2 more and try a better code:");
        System.out.print(cart.describe());

        editor.undo();
        editor.undo();
        System.out.println("\n  Two undos later, they expected to be back where they started:");
        System.out.print(cart.describe());
        System.out.println("  The 3 headphones are gone, and so is WELCOME10.");
    }

    private static void theCommands() {
        heading("2. The same edits, as objects");

        Cart cart = new Cart();
        CartHistory history = new CartHistory(cart);

        history.execute(new AddItemCommand("H-100", "Wireless headphones", HEADPHONES, 3));
        history.execute(new AddItemCommand("C-220", "USB-C cable", CABLE, 1));
        history.execute(new ApplyCouponCommand(new Coupon("WELCOME10", 10)));
        System.out.print(cart.describe());
        System.out.println("  " + history.undoDepth() + " edits recorded, all of them undoable.");
    }

    private static void undoAndRedo() {
        heading("3. Undo, then redo");

        Cart cart = new Cart();
        CartHistory history = new CartHistory(cart);
        history.execute(new AddItemCommand("H-100", "Wireless headphones", HEADPHONES, 1));
        history.execute(new AddItemCommand("C-220", "USB-C cable", CABLE, 2));
        history.execute(new AddItemCommand("K-330", "Carry case", CASE, 1));

        System.out.println("  Three lines, then the customer removes the middle one:");
        history.execute(new RemoveItemCommand("C-220"));
        System.out.print(cart.describe());

        System.out.println("\n  history.undo() -- and the cable goes back where it was:");
        history.undo();
        System.out.print(cart.describe());

        System.out.println("\n  history.redo() -- removed again:");
        history.redo();
        System.out.print(cart.describe());
    }

    private static void theHardUndo() {
        heading("4. The two edits the naive version got wrong");

        Cart cart = new Cart();
        CartHistory history = new CartHistory(cart);

        history.execute(new AddItemCommand("H-100", "Wireless headphones", HEADPHONES, 3));
        history.execute(new ApplyCouponCommand(new Coupon("WELCOME10", 10)));
        history.execute(new AddItemCommand("H-100", "Wireless headphones", HEADPHONES, 2));
        history.execute(new ApplyCouponCommand(new Coupon("BLACKFRIDAY", 25)));
        System.out.println("  5 headphones and the better code:");
        System.out.print(cart.describe());

        history.undo();
        history.undo();
        System.out.println("\n  Two undos later:");
        System.out.print(cart.describe());
        System.out.println("  3 headphones, and WELCOME10 is back.");
    }

    private static void theAuditTrail() {
        heading("5. What you get for free once an edit is an object");

        Cart cart = new Cart();
        CartHistory history = new CartHistory(cart);
        history.execute(new AddItemCommand("H-100", "Wireless headphones", HEADPHONES, 1));
        history.execute(new ChangeQuantityCommand("H-100", 4));
        history.execute(new ApplyCouponCommand(new Coupon("WELCOME10", 10)));
        history.execute(new AddItemCommand("K-330", "Carry case", CASE, 1));
        history.undo();

        System.out.println("  history.log():");
        for (String entry : history.log()) {
            System.out.println("    " + entry);
        }
        System.out.println("\n  CartHistory does not contain the words coupon, quantity or SKU.");
        System.out.println("  A fifth kind of edit is a new class and nothing else.");
    }

    private static void heading(String text) {
        System.out.println("\n=== " + text + " ===\n");
    }
}
