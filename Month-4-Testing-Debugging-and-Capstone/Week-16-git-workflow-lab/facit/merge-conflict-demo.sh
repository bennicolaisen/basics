#!/usr/bin/env bash
# Facit vecka 16: kör hela konfliktövningen automatiskt i en tillfällig
# mapp, så att du kan jämföra med det du såg när du gjorde den för hand.
#
#   bash facit/merge-conflict-demo.sh
#
# Ditt eget repo rörs inte. Allt händer i en kopia som tas bort efteråt.
set -euo pipefail

WEEK_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

NOTE=src/main/java/com/crashcourse/week16/Note.java
FACIT_NOTE="$WEEK_DIR/src/main/java/com/crashcourse/week16/facit/Note.java"

git_() { git -c user.name="Demo" -c user.email="demo@example.com" -c init.defaultBranch=main "$@"; }
step() { printf '\n=== %s\n' "$1"; }

cp -r "$WEEK_DIR/src" "$WEEK_DIR/pom.xml" "$WORK/"
rm -rf "$WORK/src/main/java/com/crashcourse/week16/facit" "$WORK/src/test/java/com/crashcourse/week16/facit"
cd "$WORK"
git_ init -q
git_ add .
git_ commit -q -m "Start"

step "1. git checkout -b feature/add-tag"
git_ checkout -q -b feature/add-tag

step "2. Lägg till tag i Note, med toString som behåller tidsstämpeln"
# Facits Note har redan taggen; byt bara tillbaka toString till grenens version.
sed -e 's/^package com.crashcourse.week16.facit;/package com.crashcourse.week16;/' "$FACIT_NOTE" \
  | python3 -c '
import sys
s = sys.stdin.read()
s = s.replace("""            ? "[%d] %s".formatted(id, text)
            : "[%d] (%s) %s".formatted(id, tag, text);""",
"""            ? "[%d] %s - %s".formatted(id, createdAt, text)
            : "[%d] (%s) %s - %s".formatted(id, tag, createdAt, text);""")
sys.stdout.write(s)' > "$NOTE"
git_ commit -q -am "Add optional tag field to Note"
git_ log --oneline -1

step "3. Tillbaka till main: ta bort tidsstämpeln ur toString"
git_ checkout -q main
python3 - "$NOTE" <<'PY'
import sys
path = sys.argv[1]
s = open(path).read()
s = s.replace('return "[%d] %s - %s".formatted(id, createdAt, text);', 'return "[%d] %s".formatted(id, text);')
open(path, "w").write(s)
PY
git_ commit -q -am "Simplify Note's toString to omit the timestamp"
git_ log --oneline -1

step "4. git merge feature/add-tag"
if git_ merge feature/add-tag; then
  echo "Oväntat: ingen konflikt." >&2
  exit 1
fi

step "Konfliktmarkeringarna i Note.java"
sed -n '/<<<<<<< /,/>>>>>>> /p' "$NOTE"

step "5. Lös konflikten: båda avsikterna, inga markeringar"
sed -e 's/^package com.crashcourse.week16.facit;/package com.crashcourse.week16;/' "$FACIT_NOTE" > "$NOTE"
if grep -qE '^(<<<<<<<|=======|>>>>>>>)' "$NOTE"; then
  echo "Markeringar finns kvar!" >&2
  exit 1
fi
sed -n '/public String toString/,/^    }/p' "$NOTE"

step "6. git add + git commit"
git_ add "$NOTE"
git_ commit -q --no-edit
git_ log --oneline --graph -5

step "7. Kontrollera att koden kompilerar"
if command -v mvn >/dev/null; then
  mvn -q -B compile && echo "Kompilerar."
else
  echo "(mvn saknas, hoppar över)"
fi
