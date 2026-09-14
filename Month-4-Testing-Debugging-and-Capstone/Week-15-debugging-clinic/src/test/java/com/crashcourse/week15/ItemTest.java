package com.crashcourse.week15;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ItemTest {

    @Test
    @DisplayName("constructs successfully with valid fields")
    void constructsWithValidFields() {
        Item item = new Item("SKU-1", "Widget", 9.99);

        assertEquals("SKU-1", item.id());
        assertEquals("Widget", item.name());
        assertEquals(9.99, item.basePrice());
    }

    @Test
    @DisplayName("rejects a blank id")
    void rejectsBlankId() {
        assertThrows(IllegalArgumentException.class, () -> new Item("  ", "Widget", 9.99));
    }

    @Test
    @DisplayName("rejects a blank name")
    void rejectsBlankName() {
        assertThrows(IllegalArgumentException.class, () -> new Item("SKU-1", " ", 9.99));
    }

    @Test
    @DisplayName("rejects a negative base price")
    void rejectsNegativeBasePrice() {
        assertThrows(IllegalArgumentException.class, () -> new Item("SKU-1", "Widget", -1.0));
    }
}
