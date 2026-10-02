# Facit vecka 16 — konfliktövningen

Övningen beskriver varje steg i detalj, så facit handlar om tre saker:
hur resultatet ska se ut, testerna som steg 7 ber om, och ett skript som
kör hela övningen automatiskt så att du kan jämföra.

- [`src/main/java/.../facit/Note.java`](src/main/java/com/crashcourse/week16/facit/Note.java)
  — `Note.java` som den ska se ut efter steg 6.
- [`src/test/java/.../facit/FacitTest.java`](src/test/java/com/crashcourse/week16/facit/FacitTest.java)
  — de nya testerna från steg 7 (`mvn -q test`).
- [`facit/merge-conflict-demo.sh`](facit/merge-conflict-demo.sh) — kör
  steg 1–7 i en tillfällig mapp. Ditt eget repo rörs inte.

```bash
bash facit/merge-conflict-demo.sh
```

## Vad du ska se

**Steg 4**, `git merge feature/add-tag`:

```
Auto-merging src/main/java/com/crashcourse/week16/Note.java
CONFLICT (content): Merge conflict in src/main/java/com/crashcourse/week16/Note.java
Automatic merge failed; fix conflicts and then commit the result.
```

I `Note.java` finns nu bara **en** konflikt, i `toString`:

```java
<<<<<<< HEAD
        return "[%d] %s".formatted(id, text);
=======
        return tag == null
            ? "[%d] %s - %s".formatted(id, createdAt, text)
            : "[%d] (%s) %s - %s".formatted(id, tag, createdAt, text);
>>>>>>> feature/add-tag
```

- Mellan `<<<<<<< HEAD` och `=======` står versionen från grenen du står
  på (`main`).
- Mellan `=======` och `>>>>>>> feature/add-tag` står versionen från grenen
  du slår ihop med.

Fältet `tag`, den nya konstruktorn och `tag()` kom med automatiskt, för
`main` hade inte ändrat de raderna.

`git status` säger under tiden att filen är "both modified", och att du
ska köra `git add` när konflikten är löst.

**Steg 5**, efter lösningen:

```java
@Override
public String toString() {
    return tag == null
        ? "[%d] %s".formatted(id, text)
        : "[%d] (%s) %s".formatted(id, tag, text);
}
```

Kontrollera att **alla tre** markeringsrader är borta. En kvarglömd
`=======` är ett vanligt misstag, och koden kompilerar då inte. Sök efter
`<<<<<<<` i filen innan du kör `git add`.

**Steg 6**, `git log --oneline --graph` efter sammanslagningen:

```
*   5e05851 Merge branch 'feature/add-tag'
|\
| * 598edd1 Add optional tag field to Note
* | 57482e4 Simplify Note's toString to omit the timestamp
|/
* 756287f Start
```

(Dina commit-id:n blir andra.) Sammanslagnings-commiten har två
föräldrar, en från varje gren. Det är det som gör den till en merge.

## Steg 7: nya tester

```java
@Test
void taggedConstructorStoresTheTag() {
    Note note = new Note(1, WHEN, "Buy milk", "shopping");
    assertEquals("shopping", note.tag());
}

@Test
void threeArgumentConstructorStillWorksAndHasNoTag() {
    assertNull(new Note(2, WHEN, "Call mum").tag());
}

@Test
void toStringWithoutTagHasNoTimestamp() {
    assertEquals("[2] Call mum", new Note(2, WHEN, "Call mum").toString());
}

@Test
void toStringWithTagShowsTagButNoTimestamp() {
    assertEquals("[1] (shopping) Buy milk", new Note(1, WHEN, "Buy milk", "shopping").toString());
}
```

Testerna använder en fast tidpunkt (`WHEN`) i stället för `Instant.now()`,
så att de ger samma resultat varje gång. Ett femte test kontrollerar att
den nya konstruktorn validerar precis som den gamla.

De två `toString`-testerna är de viktigaste. De låser fast **det beslut du
fattade när du löste konflikten**. Om någon senare råkar ta tillbaka
tidsstämpeln faller testet, och beslutet syns.

## Värt att lägga märke till

`NoteStore.save` skriver fortfarande `id|createdAt|text`, så taggen
sparas inte till fil, och `NoteStore.add` kan inte skapa en taggad
anteckning. Sammanslagningen gick igenom utan konflikt i de filerna,
eftersom ingen hade ändrat dem. Git kontrollerar att *raderna* går ihop,
inte att *programmet* hänger ihop. Det är därför steg 7 kör testerna efter
varje merge, och därför en pull request granskas av en människa.
