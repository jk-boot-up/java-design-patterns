package com.jk.explore.mvpmvvm;

public class MvpMvvmDemo {

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. The screen decides.");
        Window.reset();
        FatCartScreen screen = new FatCartScreen();
        screen.onAddClicked(1600);
        System.out.println("  to check the total and the checkout rule, a screen was needed. windows opened: " + Window.opened() + ".");
        System.out.println("  total label: " + screen.totalLabel() + ", checkout enabled: " + screen.checkoutEnabled() + ". the rules are welded to the widgets.");
    }

    private static void two() {
        System.out.println("TWO. MVP: a presenter tells a passive view.");
        Window.reset();
        RecordingView view = new RecordingView();
        CartPresenter presenter = new CartPresenter(new Cart(), view);
        view.clear();
        presenter.onAdd(1600);
        presenter.onAdd(950);
        System.out.println("  after two adds the view was told: " + view.told().subList(view.told().size() - 3, view.told().size()) + ".");
        System.out.println("  windows opened: " + Window.opened() + ". the rules were checked with no screen.");
    }

    private static void three() {
        System.out.println("THREE. MVP: the view makes no decisions.");
        RecordingView view = new RecordingView();
        CartPresenter presenter = new CartPresenter(new Cart(), view);
        System.out.println("  an empty cart: " + view.told() + ".");
        view.clear();
        presenter.onAdd(1600);
        presenter.onRemoveLast();
        System.out.println("  add then remove: the last three calls were " + view.told().subList(view.told().size() - 3, view.told().size()) + ".");
        System.out.println("  the presenter decides checkout is off again. the view just obeys.");
    }

    private static void four() {
        System.out.println("FOUR. MVVM: the view binds to state.");
        Cart cart = new Cart();
        CartViewModel vm = new CartViewModel(cart);
        BoundScreen screen = new BoundScreen(vm, false);
        System.out.println("  drawn at the start: " + screen.drawn() + ".");
        vm.add(1600);
        vm.add(950);
        System.out.println("  after two adds: " + screen.drawn() + ".");
        System.out.println("  nobody told the screen. it bound once. the view model holds no reference to any view.");
    }

    private static void five() {
        System.out.println("FIVE. Many views, one view model.");
        CartViewModel vm = new CartViewModel(new Cart());
        BoundScreen phone = new BoundScreen(vm, false);
        BoundScreen watch = new BoundScreen(vm, false);
        vm.add(1600);
        System.out.println("  phone: " + phone.drawn() + ".");
        System.out.println("  watch: " + watch.drawn() + ".");
        System.out.println("  a second screen cost no change to the view model.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        CartViewModel vm = new CartViewModel(new Cart());
        BoundScreen forgetful = new BoundScreen(vm, true);
        vm.add(1600);
        System.out.println("  MVVM: a screen that forgot to bind the total draws: " + forgetful.drawn() + ". nothing failed. it is just wrong.");
        System.out.println("  MVP: the view interface has " + CartView.class.getDeclaredMethods().length + " methods. each new thing on the screen adds one to the interface, the presenter and every view.");
        System.out.println("  MVVM hides the wiring in the binding. MVP spells it out, and gets long.");
    }
}
