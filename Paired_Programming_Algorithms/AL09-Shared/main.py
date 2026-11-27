"""Optional AL09 starter: compare topics, rank resources, then check metadata."""

import hashlib
from resource_support import tags_for, validate_weights, require_limit, canonical_bytes
from app_runner import run

STAGE = 1  # Nov 23: 1; Nov 24: 2; Nov 30: 3 after completing that stage.


# STAGE 1 - MONDAY, NOVEMBER 23: What do the represented topics share?
def shared_count(left, right):
    """Return the number of distinct tags shared by two collections."""
    left_tags = set(left)
    right_tags = set(right)
    matched = left_tags & right_tags
    return len(matched)


def jaccard(left, right):
    """Return shared-tag count divided by union size, or zero for an empty union."""
    # In simpler words: Calculates a proportion of shared tags over all unique tags.
    left_tags = set(left)
    right_tags = set(right)
    matched = left_tags & right_tags
    union = left_tags | right_tags
    if not union:
        return 0.0
    return len(matched) / len(union)


# STAGE 2 - TUESDAY, NOVEMBER 24: Which references fit, and why?
def weighted_similarity(tags, profile, weights):
    """Return score, matching-tag contributions and total union weight."""
    validate_weights(weights)
    # Use sets for resource tags and the profile, then identify overlap and union.
    resource_tags = set(tags)
    profile_tags = set(profile)
    matched = resource_tags & profile_tags
    union = resource_tags | profile_tags

    # Begin an empty contributions dictionary and a matched-weight total.
    contributions = {}
    matched_weight = 0

    # For each matching tag, record its weight and add it to the total.
    # Use a default weight of 1 when the tag is absent from weights.
    for tag in matched:
        weight = weights.get(tag, 1)
        contributions[tag] = weight
        matched_weight += weight

    # Separately total the weights of every distinct union tag.
    union_weight = 0
    for tag in union:
        union_weight += weights.get(tag, 1)

    # A zero union-weight total gives score zero; otherwise divide the totals.
    if union_weight == 0:
        score = 0.0
    else:
        score = matched_weight / union_weight

    # Return the score, contributions dictionary and union-weight total together.
    return score, contributions, union_weight


def ranking_key(result):
    """Provide descending-score and ascending-ID ordering for an exact tie."""
    # Return a two-part sorting key: negative score first, then the resource ID.
    # This lets ordinary ascending sorting place larger scores first.
    return -result["score"], result["id"]


def rank_resources(resources, profile, weights, k):
    """Return up to k new result records after scoring and ordering all candidates."""
    require_limit(k)
    validate_weights(weights)
    # Begin a new result list and consider every supplied resource.
    results = []
    profile_tags = set(profile)
    for resource in resources:
        # Use tags_for(resource) to apply the supplied missing/None-tag policy.
        tags = tags_for(resource)
        # Ask weighted_similarity for the score, contributions and union weight.
        score, contributions, union_weight = weighted_similarity(tags, profile_tags, weights)
        matched = tags & profile_tags
        union = tags | profile_tags
        # Build a new result dictionary with id, title, url, score, matched,
        # contributions and union_weight; matched is a sorted list of matching tags.
        results.append({
            "id": resource["id"],
            "title": resource["title"],
            "url": resource["url"],
            "score": score,
            "matched": sorted(matched),
            "contributions": contributions,
            "union_weight": union_weight,
            "union": len(union),
        })

    # Sort the complete list using ranking_key, then take at most k entries.
    # Preserve all source records, their tags, the profile and weights.
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