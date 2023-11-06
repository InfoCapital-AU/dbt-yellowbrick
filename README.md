## dbt-yellowbrick
The dbt-yellowbrick adapter allows *[dbt](https://www.getdbt.com/)* to work with *[Yellowbrick Data Warehouse](https://yellowbrick.com)* and leverage the 
powerful capabilities of both platforms to build data analysis workflows. This adapter is based on the *postgres-adapter* with 
extensions to support Yellowbrick specific features.  

The dbt-yellowbrick adapter has been developed for projects that implement *dbt-core* through the command-line interface (CLI) which is 
available as an [open source project](https://github.com/dbt-labs/dbt-core).

## Installation
This project is hosted on PyPI, so you should be able to install ```dbt-yellowbrick``` and the necessary dependencies via:

```pip install dbt-yellowbrick```

The latest supported version targets dbt-core 1.7.x .

## dbt Profile Configuration
Here is a basic example of a profile configuration (```profiles.yml```) to use with ```dbt-yellowbrick```.
```yaml
yb_test_models:
  target: dev
  outputs:
    dev:
      type: yellowbrick
      host: <host>
      user: <user_name>
      password: <password>
      port: 5432
      dbname: <database_name>
      schema: <schema_name>
      threads: 1
      connect_timeout: 30 # seconds  
  
    prod:
      type: yellowbrick
      host: <host>
      user: <user_name>
      password: <password>
      port: 5432
      dbname: <database_name>
      schema: <schema_name>
      threads: 1
      connect_timeout: 30 # seconds  
```

## Features
dbt-yellowbrick supports the following Yellowbrick specific features:
* distribution
* clustering
* sort
* materialisations based on cross-database queries
* incremental strategies "append" and "delete+insert"

Refer to the official [Yellowbrick documentation](https://docs.yellowbrick.com/5.2.27/) for detailed explanation of all of these.

### Some example model configurations
* ```DISTRIBUTE REPLICATE``` with a ```SORT``` column...
```sql
{{
  config(
    materialized = "table",
    dist = "replicate",
    sort_col = "stadium_capacity"
  )
}}

select
    hash(stg.name) as team_key
    , stg.name as team_name
    , stg.nickname as team_nickname
    , stg.city as home_city
    , stg.stadium as stadium_name
    , stg.capacity as stadium_capacity
    , stg.avg_att as average_game_attendance
    , current_timestamp as md_create_timestamp
from
    {{ source('premdb_public','team') }} stg
where
    stg.name is not null
``` 
gives the following model output:

```sql
create table if not exists marts.dim_team as (
select
    hash(stg.name) as team_key
    , stg.name as team_name
    , stg.nickname as team_nickname
    , stg.city as home_city
    , stg.stadium as stadium_name
    , stg.capacity as stadium_capacity
    , stg.avg_att as average_game_attendance
    , current_timestamp as md_create_timestamp
from
    premdb.public.team stg
where
    stg.name is not null
)
distribute REPLICATE
sort on (stadium_capacity);
```
<br>

* ```DISTRIBUTE``` on a single column and define up to four ```CLUSTER``` columns...

```sql 
{{
  config(
    materialized = 'table',
    dist = 'match_key',
    cluster_cols = ['season_key', 'match_date_key', 'home_team_key', 'away_team_key']
  )
}}

select
	hash(concat_ws('||',
	    lower(trim(s.season_name)),
		translate(left(m.match_ts,10), '-', ''),
	    lower(trim(h."name")),
		lower(trim(a."name")))) as match_key
	, hash(lower(trim(s.season_name))) as season_key
	, cast(translate(left(m.match_ts,10), '-', '') as integer) as match_date_key
	, hash(lower(trim(h."name"))) as home_team_key
	, hash(lower(trim(a."name"))) as away_team_key
	, m.htscore
	, split_part(m.htscore, '-', 1)  as home_team_goals_half_time
	, split_part(m.htscore , '-', 2)  as away_team_goals_half_time
	, m.ftscore
	, split_part(m.ftscore, '-', 1)  as home_team_goals_full_time
	, split_part(m.ftscore, '-', 2)  as away_team_goals_full_time
from
	{{ source('premdb_public','match') }} m
		inner join {{ source('premdb_public','team') }} h on (m.htid = h.htid)
		inner join {{ source('premdb_public','team') }} a on (m.atid = a.atid)
		inner join {{ source('premdb_public','season') }} s on (m.seasonid = s.seasonid)
```
gives the following model output:

```sql
create  table if not exists marts.fact_match as (
select
    hash(concat_ws('||',
        lower(trim(s.season_name)),
        translate(left(m.match_ts,10), '-', ''),
        lower(trim(h."name")),
        lower(trim(a."name")))) as match_key
    , hash(lower(trim(s.season_name))) as season_key
    , cast(translate(left(m.match_ts,10), '-', '') as integer) as match_date_key
    , hash(lower(trim(h."name"))) as home_team_key
    , hash(lower(trim(a."name"))) as away_team_key
    , m.htscore
    , split_part(m.htscore, '-', 1)  as home_team_goals_half_time
    , split_part(m.htscore , '-', 2)  as away_team_goals_half_time
    , m.ftscore
    , split_part(m.ftscore, '-', 1)  as home_team_goals_full_time
    , split_part(m.ftscore, '-', 2)  as away_team_goals_full_time
from
    premdb.public.match m
        inner join premdb.public.team h on (m.htid = h.htid)
        inner join premdb.public.team a on (m.atid = a.atid)
        inner join premdb.public.season s on (m.seasonid = s.seasonid)
)
distribute on (match_key)
cluster on (season_key, match_date_key, home_team_key, away_team_key);
```

## Limitations
This is an initial implementation of the dbt adapter for Yellowbrick Data Warehouse and may not support some use cases. 
We strongly advise validating all records or transformations resulting from the adapter output.
