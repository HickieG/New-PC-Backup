"""Optional AL09 test scaffold: complete focused checks as each stage is taught."""

from copy import deepcopy
from math import isclose
from main import shared_count, jaccard, weighted_similarity, rank_resources, catalog_digest
from resource_data import RESOURCES, PROFILE, WEIGHTS, LIMITATION_ID
from resource_support import tags_for
from resource_display import same_recommendations

TEST_STAGE = 2  # Nov 23: 1; Nov 24: 2; Nov 30: 3 after adding those checks.


def test_small_comparison():
    """Completed example: predict overlap and union independently of the code."""
    left = ["queues", "collections"]
    right = ["queues", "stacks"]
    assert shared_count(left, right) == 1
    assert isclose(jaccard(left, right), 1 / 3)


def test_stage_1_boundaries():
    """Check repeated, missing, nonmatching and empty tags without changing inputs."""
    # Repeated tags should count only once.
    repeated = ["queues", "queues", "stacks"]
    identical = ["queues", "stacks"]

    assert shared_count(repeated, identical) == 2
    assert isclose(jaccard(repeated, identical), 1.0)

    # Collections with no shared tags should score zero.
    assert shared_count(["queues"], ["stacks"]) == 0
    assert isclose(jaccard(["queues"], ["stacks"]), 0.0)

    # Two empty collections should score zero.
    assert shared_count([], []) == 0
    assert isclose(jaccard([], []), 0.0)

    # Missing tags and tags=None should be treated as empty sets.
    missing_tags = {}
    none_tags = {"tags": None}
    assert tags_for(missing_tags) == set()
    assert tags_for(none_tags) == set()
    assert shared_count(tags_for(missing_tags), PROFILE) == 0
    assert shared_count(tags_for(none_tags), PROFILE) == 0

    # The functions should not change the original inputs.
    left = ["queues", "queues", "collections"]
    right = ["queues", "stacks"]
    left_before = deepcopy(left)
    right_before = deepcopy(right)
    shared_count(left, right)
    jaccard(left, right)
    assert left == left_before
    assert right == right_before


def test_stage_2_rankings():
    """Check independent scores, the exact cutoff tie and changed preferences."""
    # Equal weights and k=2: expect LR013 then LR002.
    equal_results = rank_resources(RESOURCES, PROFILE, {}, 2)
    assert equal_results[0]["id"] == "LR013"
    assert equal_results[1]["id"] == "LR002"

    # Queue weight 4 and k=2: expect LR013 then LR003.
    weighted_results = rank_resources(RESOURCES, PROFILE, WEIGHTS, 2)
    assert weighted_results[0]["id"] == "LR013"
    assert weighted_results[1]["id"] == "LR003"

    # Independently check LR003.
    lr003 = None
    for result in weighted_results:
        if result["id"] == "LR003":
            lr003 = result
            break
    assert lr003 is not None
    assert lr003["contributions"] == {"queues": 4}
    assert lr003["union_weight"] == 6
    assert isclose(lr003["score"], 4 / 6)

    # With k=3 and equal weights, LR002 precedes the tied LR003.
    top_three = rank_resources(RESOURCES, PROFILE, {}, 3)
    assert top_three[0]["id"] == "LR013"
    assert top_three[1]["id"] == "LR002"
    assert top_three[2]["id"] == "LR003"

    # Reversing the input order shoudl not change the ranking.
    reversed_resources = deepcopy(RESOURCES)
    reversed_resources.reverse()
    reversed_results = rank_resources(reversed_resources, PROFILE, {}, 3)
    assert [result["id"] for result in reversed_results] == [result["id"] for result in top_three]

    # All one weights shoudl produce the same scores as Jaccard similarity.
    all_one_weights = {}
    for resource in RESOURCES:
        tags = tags_for(resource)
        expected_score = jaccard(tags, PROFILE)
        score, contributions, union_weight = weighted_similarity(tags, PROFILE, all_one_weights)
        assert isclose(score, expected_score)


def test_stage_2_boundaries():
    """Check limits, tag policies, zero weight and independent result records."""
    # k=0 should return no result.
    assert rank_resources(RESOURCES, PROFILE, {}, 0) == []

    # An empty catalog shoudl return no results.
    assert rank_resources([], PROFILE, {}, 2) == []

    # A large k shoudl return all available resources.
    all_results = rank_resources(RESOURCES, PROFILE, {}, 100)
    assert len(all_results) == len(RESOURCES)

    # Missing and None tags shoudl be treated as empty sets.
    missing_resource = {
        "id": "TEST1",
        "title": "Missing tags",
        "url": "https://example.com/missing"
    }

    none_resource = {
        "id": "TEST2",
        "title": "None tags",
        "url": "https://example.com/none",
        "tags": None
    }

    missing_results = rank_resources(
        [missing_resource, none_resource], PROFILE, {}, 2)
    assert isclose(missing_results[0]["score"], 0.0)
    assert isclose(missing_results[1]["score"], 0.0)

    # Repeated tags shoudl count only once.
    repeated_tags = ["queues", "queues", "collections"]
    score, contributions, union_weight = weighted_similarity(repeated_tags, PROFILE, {})
    assert isclose(score, 1 / 3)
    assert contributions == {"queues": 1}
    assert union_weight == 3

    # An empty union should have a score of zero.
    score, contributions, union_weight = weighted_similarity([], [], {})
    assert isclose(score, 0.0)
    assert contributions == {}
    assert union_weight == 0

    # An all zero weight union should also have a score of zero.
    score, contributions, union_weight = weighted_similarity(["queues"], ["queues"], {"queues": 0})
    assert isclose(score, 0.0)
    assert contributions == {"queues": 0}
    assert union_weight == 0

    # Preserve the original inputs.
    resources_before = deepcopy(RESOURCES)
    profile_before = deepcopy(PROFILE)
    weights_before = deepcopy(WEIGHTS)

    results = rank_resources(RESOURCES, PROFILE, WEIGHTS, 2)
    assert RESOURCES == resources_before
    assert PROFILE == profile_before
    assert WEIGHTS == weights_before

    # Each result should contain the required fields. 
    required_fields = {"id", "title", "url", "score", "matched", "contributions", "union_weight",}
    for result in results:
        assert set(result.keys()) >= required_fields

    # Changing a returned result should not change the source resource.
    first_id = results[0]["id"]
    original_title = None
    for resource in RESOURCES:
        if resource["id"] == first_id:
            original_title = resource["title"]
            break
    results[0]["title"] = "Changed Title"
    for resource in RESOURCES:
        if resource["id"] == first_id:
            assert resource["title"] == original_title


def test_stage_3_controlled_changes():
    """Check separate missing-tag and title-only edits against independent expectations."""
    # Begin from independent deepcopy copies of RESOURCES for EACH experiment.
    # Remove tags only from LIMITATION_ID: expect equal-weight IDs LR002, LR003.
    # Check the original catalog remains unchanged and its original top two remain.
    # In a fresh copy, change only a title: the digest changes but recommendation
    # IDs, order and scores stay the same; same_recommendations compares those.
    # Reverse records and tag order in another copy: the digest stays the same.
    # The runner demonstrates these changes; add your own assertions here.
    raise NotImplementedError("Add stage 3 snapshot and recommendation checks.")


def main():
    """Run only the checks completed for the selected instructional stage."""
    if TEST_STAGE not in (1, 2, 3):
        raise ValueError("TEST_STAGE must be 1, 2, or 3")
    test_small_comparison()
    test_stage_1_boundaries()
    if TEST_STAGE >= 2:
        test_stage_2_rankings()
        test_stage_2_boundaries()
    if TEST_STAGE >= 3:
        test_stage_3_controlled_changes()
    print("Selected-stage checks passed; complete all three stages before submission.")


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Run tests without Python optimization (-O).")
    main()
