package com.crashcourse.week16.facit;

import java.time.Instant;

/**
 * Facit: Note som den ser ut efter sammanslagningen i steg 6, med både
 * taggen från feature/add-tag och den kortare toString från main.
 */
public final class Note {

    private final int id;
    private final Instant createdAt;
    private final String text;
    private final String tag;

    public Note(int id, Instant createdAt, String text) {
        this(id, createdAt, text, null);
    }

    public Note(int id, Instant createdAt, String text, String tag) {
        if (id <= 0) {
            throw new IllegalArgumentException("Note id must be positive, got " + id);
        }
        if (createdAt == null) {
            throw new IllegalArgumentException("createdAt must not be null");
        }
        if (text == null || text.isBlank()) {
            throw new IllegalArgumentException("Note text must not be blank");
        }
        if (text.contains("\n")) {
            throw new IllegalArgumentException("Note text must not contain newlines");
        }
        this.id = id;
        this.createdAt = createdAt;
        this.text = text;
        this.tag = tag;
    }

    public int id() {
        return id;
    }

    public Instant createdAt() {
        return createdAt;
    }

    public String text() {
        return text;
    }

    public String tag() {
        return tag;
    }

    @Override
    public String toString() {
        return tag == null
            ? "[%d] %s".formatted(id, text)
            : "[%d] (%s) %s".formatted(id, tag, text);
    }
}
