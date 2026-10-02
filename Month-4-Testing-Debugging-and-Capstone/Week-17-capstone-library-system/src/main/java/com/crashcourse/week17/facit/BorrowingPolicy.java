package com.crashcourse.week17.facit;

import java.util.HashMap;
import java.util.Map;
import java.util.OptionalInt;

/**
 * Facit, uppgift 5: bibliotekets regler för hur många exemplar av varje
 * sort en medlem får låna samtidigt, till exempel högst 1 DVD.
 *
 * <p>Gränserna är nycklade på klassen (DVD.class, Book.class, ...), så det
 * behövs ingen if-kedja med instanceof, och en ny sort som AudioBook har
 * helt enkelt ingen egen gräns förrän någon sätter en.
 */
public final class BorrowingPolicy {

    private final Map<Class<? extends LibraryItem>, Integer> limits = new HashMap<>();

    public BorrowingPolicy limit(Class<? extends LibraryItem> type, int maxAtOnce) {
        if (type == null) {
            throw new IllegalArgumentException("Type must not be null");
        }
        if (maxAtOnce <= 0) {
            throw new IllegalArgumentException("Limit must be positive, got " + maxAtOnce);
        }
        limits.put(type, maxAtOnce);
        return this;
    }

    public OptionalInt limitFor(Class<? extends LibraryItem> type) {
        Integer limit = limits.get(type);
        return limit == null ? OptionalInt.empty() : OptionalInt.of(limit);
    }
}
