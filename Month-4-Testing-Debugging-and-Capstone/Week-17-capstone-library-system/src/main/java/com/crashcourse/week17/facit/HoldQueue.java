package com.crashcourse.week17.facit;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.List;

/**
 * Facit, uppgift 3: kön av reservationer för <em>ett</em> exemplar.
 *
 * <p>Klassen äger två saker: vilka som väntar, i turordning, och vem
 * exemplaret just nu ligger reserverat för (den som stod först när det
 * lämnades tillbaka). Den vet ingenting om lånegränser eller om exemplaret
 * är utlånat; det samordnar Library, precis som för vanliga lån.
 */
public final class HoldQueue {

    private final Deque<Member> waiting = new ArrayDeque<>();
    private Member reservedFor;

    /** Ställer medlemmen sist i kön. En medlem kan bara stå i kön en gång. */
    public void place(Member member) {
        if (member == null) {
            throw new IllegalArgumentException("Member must not be null");
        }
        if (waiting.contains(member) || member == reservedFor) {
            throw new IllegalStateException("Member " + member.id() + " already has a hold on this item");
        }
        waiting.addLast(member);
    }

    /** Exemplaret har lämnats tillbaka: reservera det för den som står först. */
    void itemReturned() {
        reservedFor = waiting.pollFirst();
    }

    /** Medlemmen har hämtat ut sin reservation. */
    void pickedUpBy(Member member) {
        if (member == reservedFor) {
            reservedFor = null;
        }
    }

    public boolean isReservedForSomeoneOtherThan(Member member) {
        return reservedFor != null && reservedFor != member;
    }

    public Member reservedFor() {
        return reservedFor;
    }

    public boolean hasWaiting() {
        return !waiting.isEmpty();
    }

    public List<Member> waiting() {
        return List.copyOf(waiting);
    }
}
