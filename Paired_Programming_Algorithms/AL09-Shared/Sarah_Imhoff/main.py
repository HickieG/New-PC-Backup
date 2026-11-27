"""Optional AL09 starter: compare topics, rank resources, then check metadata."""

import hashlib
from resource_support import tags_for, validate_weights, require_limit, canonical_bytes
from app_runner import run

STAGE = 2


# STAGE 1 - MONDAY, NOVEMBER 23: What do the represented topics share?
def shared_count(left, right):
    """Return the number of distinct tags shared by two collections."""
    left_tags= set(left)
    right_tags = set(right)
    shared_tags = left_tags & right_tags
    return len(shared_tags)


def jaccard(left, right):
    """Return shared-tag count divided by union size, or zero for an empty union."""
    left_tags = set(left)
    right_tags = set(right)
    shared_tags = left_tags & right_tags
    union_tags = left_tags | right_tags
    if not union_tags: 
        return 0.0
    return len(shared_tags) / len(union_tags)


# STAGE 2 - TUESDAY, NOVEMBER 24: Which references fit, and why?
def weighted_similarity(tags, profile, weights):
    """Return score, matching-tag contributions and total union weight."""
    validate_weights(weights)
    tag_set = set(tags)
    profile_set = set(profile)
    matching_tags = tag_set & profile_set
    union_tags = tag_set | profile_set
    contributions = {}
    matched_weight = 0
    for tag in matching_tags:
        weight = weights.get(tag, 1)
        contributions[tag] = weight
        matched_weight += weight
    union_weight = 0
    for tag in union_tags:
        union_weight += weights.get(tag, 1)
    if union_weight == 0:
        score = 0.0
    else:
        score = matched_weight / union_weight
    return score, contributions, union_weight


def ranking_key(result):
    """Provide descending-score and ascending-ID ordering for an exact tie."""
    return -result["score"], result["id"]


def rank_resources(resources, profile, weights, k):
    """Return up to k new result records after scoring and ordering all candidates."""
    require_limit(k)
    validate_weights(weights)
    results = []
    for resource in resources:
        tags = tags_for(resource)
        score, contributions, union_weight = weighted_similarity(tags, profile, weights)
        matched = sorted(tags & set(profile))
        result = {
            "id": resource["id"],
            "title": resource["title"],
            "url": resource["url"],
            "score": score,
            "matched": matched,
            "contributions": contributions,
            "union_weight": union_weight
        }
        results.append(result)
    results.sort(key=ranking_key)
    return results[:k]


# STAGE 3 - MONDAY, NOVEMBER 30: Did the represented metadata change?
# No class Thursday, November 26; continue the same project after the holiday.
def catalog_digest(resources):
    """Return a SHA-256 hexadecimal fingerprint of the declared metadata snapshot."""
    # Use canonical_bytes(resources) for the supplied consistent serialization.
    # Pass those bytes to hashlib's SHA-256 implementation.
    # Return its hexadecimal digest; do not write another serializer or hash.
    raise NotImplementedError("Complete the library-based metadata fingerprint.")


def main():
    """Use the supplied presentation to run only the selected completed stages."""
    if STAGE == 1:
        run(1, shared_count, jaccard)
    elif STAGE == 2:
        run(2, shared_count, jaccard, rank_resources)
    else:
        run(STAGE, shared_count, jaccard, rank_resources, catalog_digest)


if __name__ == "__main__":
    main()
