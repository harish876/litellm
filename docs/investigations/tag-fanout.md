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
```