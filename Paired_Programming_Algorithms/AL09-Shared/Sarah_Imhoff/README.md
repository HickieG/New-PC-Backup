# AL09: Explainable Resource Ranking and Integrity

Name: Sarah Imhoff
Partner(s): None
My contribution: I completed the Stage 1 similarity functions and tests and the Stage 2 weighted scoring, ranking, tie-breaking, and boundary tests.

## Run

```powershell
py -3.14 main.py
py -3.14 test_assignment.py
```

## Work Notes

- Representation: Resource tags represent the topics associated with each learning resource, while the profile represents the topics being reviewed. This representation does not measure the quality of a resource or include all details about its contents.

- Scoring/ranking: I first used sets to count distinct shared tags and calculate Jaccard similarity. For ["queues", "collections"] and ["queues", "stacks"], the shared count is 1 and the union count is 3, so the Jaccard score is 1 / 3, or approximately 0.333.  With equal weights, LR002 and LR003 both score `0.333`, so the ascending-ID tie rule laces LR002 before LR003. When queues is given weight 4, LR003 has a matched weight of 4 and a untion weight of 6, giving it a score of `4 / 6`, or approximately `0.667`. This changes the top two from LR013 and LR002 to LR013 and LR003. 

- Limits/integrity: Missing tags and tags=None are treated as empty sets. Empty or all zero weight untion receive a scoare of 0.0 to avoid division by zero. I also tested k=0, an empty catalog, a limit larger than the catalog, repeated tags, and preservation of the original inputs. The metadata integrity portion will be completed during Stage 3.

- Learning/debugging: I learned that converting the inputs to sets prevents repeated tags from being counted more than once. I also added an empty-union check before dividing and verified that the functions do not modify their original inputs. 

I learned how weighting can change ranking results even when the underlying resource tags stay the same. I also learned why the ranking needs an explicit tie-breakign rule instead of relying on the original catalog order. While testing, I corrected an empty-union test so that both collections were actually empty and tehn verified that all Stage 2 tests passed.

- Collaboration: I worked independently.  I used the supplied program output and test scaffold to verify the expected scores, ranking order, cutoff tie, weighted preference change, and boundary cases.


## Assistance

I used the supplied app_runner.py, resource_data.py, resource_display.py and resource_support.py modules for the catalog data, missing-tag policy, and console output. I used AI to help interpret the Stage 1 and Stage 2 instructions, and help develop the boundary tests.  I reviewed the code, entered it myself, compared the displayed results with the hand calculations, corrected a test when its inputs did not represent an empty union and ran test_assignment.py to confirm that all selected Stage 2 checks passed. 

## Instructor Comments

[Reserved for instructor feedback.]
