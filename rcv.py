from random import gauss
from math import floor


def ranked_choice_voting(N=100000, seats=3, n=10):
    threshold = N//(seats + 1) + 1

    print(f"Need {threshold} votes to win")
    ballots = hold_election(N, n)

    tallies = tally(ballots, n)
    print(tallies, end="\n\n")

    winners = dict()
    eliminated = set()

    while len(winners) < seats:
        num_winners = len(winners)

        find_winners(tallies, threshold, winners)
        print(winners)
        print(tallies, end="\n\n")

        while len(winners) > num_winners and len(winners) < seats:
            num_winners = len(winners)
            reallocate(ballots, threshold, winners)
            tallies = tally(ballots)

            find_winners(tallies, threshold, winners)
            print(winners)
            print(tallies)

        for i in winners:
            tallies[i] = threshold
        print("current tally: ", tallies, end="\n\n")

        if len(winners) == seats:
            break

        eliminate(tallies, winners, eliminated)
        print("eliminated: ", eliminated)
        reallocate(ballots, threshold, winners, eliminated)
        tallies = tally(ballots)

        print(tallies, end="\n\n")

    print(winners)


def find_winners(tallies, threshold, winners=None):
    new_winners = {tallies.index(
        count): count for count in tallies if count > threshold}
    if winners is None:
        winners = new_winners
    else:
        winners.update(new_winners)


def reallocate(ballots, threshold, winners: dict, eliminated=None):
    if eliminated is None:
        eliminated = set()
    decided = set(winners.keys()).union(eliminated)

    for ballot in ballots:
        rankings, rank, _ = ballot

        if rankings[rank] in winners:
            ballot[2] = (winners[rankings[rank]] - threshold) / \
                winners[rankings[rank]]

        while ballot[1] < len(rankings) and rankings[ballot[1]] in decided:
            ballot[1] += 1


def eliminate(tallies, winners=None, eliminated=None):
    if eliminated is None:
        eliminated = set()
    if winners is None:
        winners = dict()

    eliminated.add(
            min([(count, idx) for idx, count in enumerate(
                tallies) if idx not in eliminated], key=lambda x: x[0])[1]
        )

    # print(f"{[a for a in eliminated]} have been eliminated")


def runoff(ballots, eliminated):
    for ballot in ballots:
        while ballot[1] < len(ballot[0]) and ballot[0][ballot[1]] in eliminated:
            ballot[1] += 1
        # print(ballot)


def tally(ballots, n=None):
    if n is None:
        n = len(ballots[0][0])
    tallies = [0]*n

    for ranking, pos, value in ballots:
        if pos == n:
            continue
        tallies[ranking[pos]] += value

    return [round(x, 2) for x in tallies]


def hold_election(N, n):
    candidates = [False]*n
    rankings = []
    offset = n / 2

    for _ in range(N):
        ranking = [choice(0, offset)]

        while len(ranking) < n - 1:
            candidates[ranking[-1]] = True
            next_choice = choice(ranking[-1] - offset, offset)
            while candidates[next_choice]:
                next_choice = choice(ranking[-1] - offset, offset)

            ranking.append(next_choice)

        candidates[ranking[-1]] = True
        ranking.append(candidates.index(False))
        candidates = [False]*n

        rankings.append(ranking)

    return [[rank, 0, 1] for rank in rankings]


def choice(center=0, offset=3):
    score = gauss(center, 1)
    return floor(offset + score) % int(offset * 2)


if __name__ == "__main__":
    ranked_choice_voting()
