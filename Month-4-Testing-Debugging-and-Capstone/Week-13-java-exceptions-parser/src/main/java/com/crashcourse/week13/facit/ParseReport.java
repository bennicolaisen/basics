package com.crashcourse.week13.facit;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/** Facit, uppgift 4: en textrapport över ett BatchParseResult. */
public final class ParseReport {

    private ParseReport() {
        // utility class: no instances
    }

    /** Rapportens rader. Egen metod så att innehållet kan testas utan fil. */
    public static List<String> lines(BatchParseResult result) {
        List<String> lines = new ArrayList<>();
        lines.add("Parse report");
        lines.add("Records parsed: " + result.records().size());
        lines.add("Lines failed: " + result.errors().size());
        if (result.hasErrors()) {
            lines.add("Errors:");
            for (ParseError error : result.errors()) {
                lines.add("  " + error);
            }
        } else {
            lines.add("Errors: none");
        }
        return lines;
    }

    /** Skriver rapporten till filen. En befintlig fil skrivs över. */
    public static void write(BatchParseResult result, Path path) throws IOException {
        Files.write(path, lines(result), StandardCharsets.UTF_8);
    }
}
