## With 1 tag per request

**Before Fix**

```
litellm=# select
  calls,
  left(query, 50) as query_prefix
from pg_stat_statements
where query ilike 'insert%'
order by calls desc
limit 5;
 calls |                    query_prefix                    
-------+----------------------------------------------------
    52 | INSERT INTO "public"."LiteLLM_DailyTagSpend" ("id"
    25 | INSERT INTO "public"."LiteLLM_DailyTeamSpend" ("id
    25 | INSERT INTO "public"."LiteLLM_DailyUserSpend" ("id
     1 | INSERT INTO "public"."LiteLLM_SpendLogs" ("model_i
     1 | INSERT INTO "public"."LiteLLM_SpendLogs" ("call_ty
(5 rows)

litellm=# SELECT
    left(query, 25) AS query_prefix,
    calls / NULLIF(
        EXTRACT(EPOCH FROM (now() - (
            SELECT stats_reset
            FROM pg_stat_statements_info
        ))),
        0
    ) AS avg_qps_since_reset
FROM pg_stat_statements
WHERE query LIKE 'INSERT INTO "public"."LiteLLM_DailyTagSpend" ("id"%'
ORDER BY calls DESC
LIMIT 10;
       query_prefix        |  avg_qps_since_reset   
---------------------------+------------------------
 INSERT INTO "public"."Lit | 0.31182049273784314215
(1 row)
```

Using Redis Transaction Buffer
```
litellm=# select
  calls,                            
  left(query, 50) as query_prefix
from pg_stat_statements
where query ilike 'insert%'
order by calls desc
limit 15;
 calls |                    query_prefix                    
-------+----------------------------------------------------
    50 | INSERT INTO "public"."LiteLLM_DailyTagSpend" ("id"
    25 | INSERT INTO "public"."LiteLLM_DailyUserSpend" ("id
    25 | INSERT INTO "public"."LiteLLM_DailyTeamSpend" ("id
(15 rows)

litellm=# SELECT
    left(query, 25) AS query_prefix,
    calls / NULLIF(
        EXTRACT(EPOCH FROM (now() - (
            SELECT stats_reset
            FROM pg_stat_statements_info
        ))),
        0
    ) AS avg_qps_since_reset
FROM pg_stat_statements
WHERE query LIKE 'INSERT INTO "public"."LiteLLM_DailyTagSpend" ("id"%'
ORDER BY calls DESC
LIMIT 10;
       query_prefix        |  avg_qps_since_reset   
---------------------------+------------------------
 INSERT INTO "public"."Lit | 0.32670871516733775359
(1 row)
```

**With Adjusted Batch Interval Fix**
```
litellm=# select
  calls,
  left(query, 50) as query_prefix
from pg_stat_statements
where query ilike 'insert%'
order by calls desc
limit 5;
 calls |                    query_prefix                    
-------+----------------------------------------------------
    53 | INSERT INTO "public"."LiteLLM_DailyUserSpend" ("id
    53 | INSERT INTO "public"."LiteLLM_DailyTeamSpend" ("id
    52 | INSERT INTO "public"."LiteLLM_DailyTagSpend" ("id"
     1 | INSERT INTO "public"."LiteLLM_SpendLogs" ("respons
     1 | INSERT INTO "public"."LiteLLM_SpendLogs" ("mcp_nam
(5 rows)

litellm=# SELECT
    left(query, 25) AS query_prefix,
    calls / NULLIF(
        EXTRACT(EPOCH FROM (now() - (
            SELECT stats_reset
            FROM pg_stat_statements_info
        ))),
        0
    ) AS avg_qps_since_reset
FROM pg_stat_statements
WHERE query LIKE 'INSERT INTO "public"."LiteLLM_DailyTagSpend" ("id"%'
ORDER BY calls DESC
LIMIT 10;
       query_prefix        |  avg_qps_since_reset   
---------------------------+------------------------
 INSERT INTO "public"."Lit | 0.16589514881214770545
(1 row)
```

Using Redis Transaction Buffer
```
litellm=# select
  calls,                            
  left(query, 50) as query_prefix
from pg_stat_statements
where query ilike 'insert%'
order by calls desc
limit 15;
 calls |                    query_prefix                    
-------+----------------------------------------------------
    50 | INSERT INTO "public"."LiteLLM_DailyTeamSpend" ("id
    50 | INSERT INTO "public"."LiteLLM_DailyUserSpend" ("id
    50 | INSERT INTO "public"."LiteLLM_DailyTagSpend" ("id"
     1 | INSERT INTO "public"."LiteLLM_SpendLogs" ("end_use

litellm=# SELECT
    left(query, 25) AS query_prefix,
    calls / NULLIF(
        EXTRACT(EPOCH FROM (now() - (
            SELECT stats_reset
            FROM pg_stat_statements_info
        ))),
        0
    ) AS avg_qps_since_reset
FROM pg_stat_statements
WHERE query LIKE 'INSERT INTO "public"."LiteLLM_DailyTagSpend" ("id"%'
ORDER BY calls DESC
LIMIT 10;
       query_prefix        |  avg_qps_since_reset   
---------------------------+------------------------
 INSERT INTO "public"."Lit | 0.14892439673581266593
(1 row)
```