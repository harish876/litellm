## optimizing pre-processing 
 - `_should_check_db`: Correctness bug but doesnt solve performance


## optimizing guardrails function
 - 	Baseline: 
     -  Median: 240
     -  RPS: 304.9
     - ``POST	/v1/chat/completions	28561	0	240	1300	3100	389.02	2	4585	443.46	304.9	0``

 - Fix-1 (Early Return)
     -  Median: 270
     -  RPS: 300.1
     - ``POST	/v1/chat/completions	28472	0	270	1300	3100	416.99	1	4653	443.41	300.1	0``

 - Fix-2 (Early Return but comment out rest of flow control)
     -  Median: 240
     -  RPS: 226.8
     - ``POST	/v1/chat/completions	29360	0	240	1400	3300	415.65	2	4583	443.36	226.8	0`

--- NETWORK MOCKED ---

 - **Fix-3** get_llm_provider -> Baseline
    - Median: 260
    - RPS: 298.5
    - ``POST	/v1/chat/completions	24928	0	270	1300	3400	423.26	1	4798	443.43	304.8	0``

 - **Fix-3** get_llm_provider -> Optimized
    - Median: 93
    - RPS: 354
    - ``POST	/v1/chat/completions	26921	0	98	740	2000	199.23	1	4641	354.56	320.8	0``