package com.jk.explore.mvpmvvm;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.Test;

class MvpMvvmTest {

    @Test
    void theFatScreenNeedsAWindow() {
        Window.reset();
        new FatCartScreen().onAddClicked(1600);
        assertEquals(1, Window.opened());
    }

    @Test
    void presenterTellsTheViewWithoutAWindow() {
        Window.reset();
        RecordingView view = new RecordingView();
        CartPresenter p = new CartPresenter(new Cart(), view);
        view.clear();
        p.onAdd(1600);
        assertEquals(List.of("showTotal £16.00", "showCount 1", "enableCheckout true"), view.told());
        assertEquals(0, Window.opened());
    }

    @Test
    void presenterDisablesCheckoutWhenEmptied() {
        RecordingView view = new RecordingView();
        CartPresenter p = new CartPresenter(new Cart(), view);
        p.onAdd(100);
        p.onRemoveLast();
        List<String> told = view.told();
        assertEquals("enableCheckout false", told.get(told.size() - 1));
    }

    @Test
    void boundScreenFollowsTheViewModel() {
        CartViewModel vm = new CartViewModel(new Cart());
        BoundScreen s = new BoundScreen(vm, false);
        assertEquals("£0.00 | 0 items | checkout off", s.drawn());
        vm.add(1600);
        vm.add(950);
        assertEquals("£25.50 | 2 items | checkout on", s.drawn());
    }

    @Test
    void twoScreensShareOneViewModel() {
        CartViewModel vm = new CartViewModel(new Cart());
        BoundScreen a = new BoundScreen(vm, false);
        BoundScreen b = new BoundScreen(vm, false);
        vm.add(500);
        assertEquals(a.drawn(), b.drawn());
    }

    @Test
    void aForgottenBindingIsSilentlyWrong() {
        CartViewModel vm = new CartViewModel(new Cart());
        BoundScreen s = new BoundScreen(vm, true);
        vm.add(1600);
        assertTrue(s.drawn().startsWith("? |"));
    }

    @Test
    void observableOnlyNotifiesOnChange() {
        Observable<Integer> o = new Observable<>(1);
        int[] calls = {0};
        o.bind(v -> calls[0]++);
        o.set(1);
        o.set(2);
        assertEquals(2, calls[0]);
    }
}
