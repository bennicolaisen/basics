package com.crashcourse.week16;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.IOException;
import java.nio.file.Path;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class NoteStoreTest {

    private NoteStore store;

    @BeforeEach
    void setUp() {
        store = new NoteStore();
    }

    @Test
    @DisplayName("add assigns increasing ids starting at 1")
    void addAssignsIncreasingIds() {
        Note first = store.add("First note");
        Note second = store.add("Second note");

        assertEquals(1, first.id());
        assertEquals(2, second.id());
    }

    @Test
    @DisplayName("list returns every added note, in insertion order")
    void listReturnsAllNotesInOrder() {
        store.add("First");
        store.add("Second");

        List<Note> notes = store.list();

        assertEquals(List.of("First", "Second"),
            notes.stream().map(Note::text).toList());
    }

    @Test
    @DisplayName("search is case-insensitive and matches on substring")
    void searchIsCaseInsensitiveSubstringMatch() {
        store.add("Buy milk");
        store.add("Walk the dog");
        store.add("Buy bread");

        List<Note> results = store.search("BUY");

        assertEquals(List.of("Buy milk", "Buy bread"),
            results.stream().map(Note::text).toList());
    }

    @Test
    @DisplayName("search rejects a blank keyword")
    void searchRejectsBlankKeyword() {
        assertThrows(IllegalArgumentException.class, () -> store.search("  "));
    }

    @Test
    @DisplayName("delete removes the note with a matching id and reports success")
    void deleteRemovesMatchingNote() {
        Note note = store.add("Buy milk");

        boolean deleted = store.delete(note.id());

        assertTrue(deleted);
        assertTrue(store.list().isEmpty());
    }

    @Test
    @DisplayName("delete reports no removal for an id that doesn't exist")
    void deleteReportsFalseForMissingId() {
        store.add("Buy milk");

        assertFalse(store.delete(999));
        assertEquals(1, store.list().size());
    }

    @Test
    @DisplayName("save then load round-trips every note, including ids and text")
    void saveThenLoadRoundTrips(@TempDir Path tempDir) throws IOException {
        store.add("Buy milk");
        store.add("Walk the dog");
        Path file = tempDir.resolve("notes.txt");

        store.save(file);
        NoteStore reloaded = NoteStore.load(file);

        assertEquals(List.of("Buy milk", "Walk the dog"),
            reloaded.list().stream().map(Note::text).toList());
    }

    @Test
    @DisplayName("loading a file that doesn't exist yet yields an empty store")
    void loadMissingFileYieldsEmptyStore(@TempDir Path tempDir) throws IOException {
        Path file = tempDir.resolve("does-not-exist.txt");

        NoteStore loaded = NoteStore.load(file);

        assertTrue(loaded.list().isEmpty());
    }

    @Test
    @DisplayName("after loading, a new note continues the id sequence rather than colliding")
    void loadContinuesIdSequence(@TempDir Path tempDir) throws IOException {
        store.add("Buy milk");
        store.add("Walk the dog");
        Path file = tempDir.resolve("notes.txt");
        store.save(file);

        NoteStore reloaded = NoteStore.load(file);
        Note third = reloaded.add("Third note");

        assertEquals(3, third.id());
    }
}
