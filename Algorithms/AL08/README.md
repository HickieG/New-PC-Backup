# AL08: Workshop Access — Traversal and Restricted Routes

Name: [your name]
Partner(s): [names]
My contribution: [brief individual/modeling and shared-development notes]
Issued personal case: [A / B / C]

## Run

```powershell
py -3.14 main.py
py -3.14 test_assignment.py
```

Final settings: STAGE = 3 and TEST_STAGE = 3 if using the starter switches.

## Work Notes

- Model: [what rooms/connections represent, why direction matters, and one omission]
- Monday check: [one broken connection and how you repaired it]
- Traversal: [one useful queue/stack observation and why cycling stops]
- Personal restriction: [blocked room(s), expected/actual route or no route, and why]
- Collaboration: [one useful question/decision and your contribution]

- Model: rooms are nodes and permitted passages are two-way edges; distance, travel time, and capacity are not represented.
- Monday check: the declared Annex with an empty neighbor list is valid but unreachable; the validator checks declared nodes and reciprocal connections.
- Traversal: BFS marks rooms discovered when enqueuing them; DFS skips already-visited rooms when popped, so the cycle does not repeat visits.
- Personal restriction: complete this note after the instructor-issued case is known and the Thursday route work is complete.


## Monday's Model Check

AL08 uses an undirected graph where rooms are nodes and permitted passages are edges bidirectional. The model omits things like distance between rooms. The Annex is valid in the graph structure (a declared empty neighbor list) but unreachable from Entrance because no edge connects it to the main component. Validation ensures all references exist and all edges are reciprocal (undirected property). 

## Tuesday Traversal Workflow

- Used the supplied validation and snapshot helpers; implemented BFS with a queue and discovery-on-enqueue, then iterative DFS with a stack and visited-on-pop.
- Checked both traversals on a small cyclic graph and a disconnected start, then on the workshop graph: each reaches 11 rooms and examines 26 adjacency entries; Annex is unreachable.
- Tests verify visit order, no repeated processing, adjacency counts, and that traversal leaves the input graph unchanged.

## Assistance

[Identify supplied helpers and other help. For AI, justify the task/tool and what
you checked, changed, or rejected. No AI use is required.]

## Instructor Comments

[Reserved for instructor feedback.]