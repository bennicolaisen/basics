package com.crashcourse.week16;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/**
 * Holds the current set of notes in memory and persists them to a plain
 * text file, one note per line, as {@code id|createdAt|text}.
 */
public final class NoteStore {

    private final List<Note> notes = new ArrayList<>();
    private int nextId = 1;

    public Note add(String text) {
        Note note = new Note(nextId, Instant.now(), text);
        notes.add(note);
        nextId++;
        return note;
    }

    public List<Note> list() {
        return List.copyOf(notes);
    }

    public List<Note> search(String keyword) {
        if (keyword == null || keyword.isBlank()) {
            throw new IllegalArgumentException("Search keyword must not be blank");
        }
        String needle = keyword.toLowerCase(Locale.ROOT);
        return notes.stream()
            .filter(note -> note.text().toLowerCase(Locale.ROOT).contains(needle))
            .toList();
    }

    /** Removes the note with the given id, if present. Returns whether one was removed. */
    public boolean delete(int id) {
        return notes.removeIf(note -> note.id() == id);
    }

    public void save(Path path) throws IOException {
        List<String> lines = notes.stream()
            .map(note -> "%d|%s|%s".formatted(note.id(), note.createdAt(), note.text()))
            .toList();
        Files.write(path, lines);
    }

    /** Loads notes from {@code path}, or returns an empty store if it doesn't exist yet. */
    public static NoteStore load(Path path) throws IOException {
        NoteStore store = new NoteStore();
        if (!Files.exists(path)) {
            return store;
        }
        for (String line : Files.readAllLines(path)) {
            if (line.isBlank()) {
                continue;
            }
            // limit=3 keeps the rest of the line intact as the text field,
            // even if the note's own text happens to contain "|".
            String[] parts = line.split("\\|", 3);
            if (parts.length != 3) {
                continue; // skip a corrupted line rather than fail the whole load
            }
            int id = Integer.parseInt(parts[0]);
            Instant createdAt = Instant.parse(parts[1]);
            String text = parts[2];
            store.notes.add(new Note(id, createdAt, text));
            if (id >= store.nextId) {
                store.nextId = id + 1;
            }
        }
        return store;
    }
}
