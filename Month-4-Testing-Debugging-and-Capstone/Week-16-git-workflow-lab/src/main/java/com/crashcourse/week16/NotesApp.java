package com.crashcourse.week16;

import java.io.IOException;
import java.nio.file.Path;
import java.util.Scanner;

/** A tiny console front end over {@link NoteStore}: add, list, search, delete, quit. */
public final class NotesApp {

    private static final Path STORAGE_PATH = Path.of("notes.txt");

    public static void main(String[] args) throws IOException {
        NoteStore store = NoteStore.load(STORAGE_PATH);
        Scanner scanner = new Scanner(System.in);

        System.out.println("NotesApp - commands: add, list, search, delete, quit");
        while (true) {
            System.out.print("> ");
            if (!scanner.hasNextLine()) {
                break;
            }
            String command = scanner.nextLine().trim();

            switch (command) {
                case "add" -> {
                    System.out.print("Text: ");
                    Note note = store.add(scanner.nextLine());
                    System.out.println("Added " + note);
                }
                case "list" -> store.list().forEach(System.out::println);
                case "search" -> {
                    System.out.print("Keyword: ");
                    store.search(scanner.nextLine()).forEach(System.out::println);
                }
                case "delete" -> {
                    System.out.print("Id: ");
                    int id = Integer.parseInt(scanner.nextLine().trim());
                    System.out.println(store.delete(id) ? "Deleted." : "No note with that id.");
                }
                case "quit" -> {
                    store.save(STORAGE_PATH);
                    System.out.println("Saved " + store.list().size() + " note(s). Bye.");
                    return;
                }
                default -> System.out.println("Unknown command: " + command);
            }
        }
    }
}
