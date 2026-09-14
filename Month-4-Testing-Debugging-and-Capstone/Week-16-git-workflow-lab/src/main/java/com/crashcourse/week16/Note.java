package com.crashcourse.week16;

import java.time.Instant;

/** An immutable, single-line note with a positive id and a creation time. */
public final class Note {

    private final int id;
    private final Instant createdAt;
    private final String text;

    public Note(int id, Instant createdAt, String text) {
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

    @Override
    public String toString() {
        return "[%d] %s - %s".formatted(id, createdAt, text);
    }
}
