

a = """12988
16187
18341
15191
22812
21943
17292
25197
21282
23023
39338
48652
51129
58805
68396
84515
81905
106568
112593
155020
156532
183415
198919
231558
279358"""

b = [int(c)*5/6 for c in a.split("\n")]
print(sum(b)/170/12)