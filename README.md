<p align="center">
  <img src="https://raw.githubusercontent.com/dbt-labs/dbt/ec7dee39f793aa4f7dd3dae37282cc87664813e4/etc/dbt-logo-full.svg" alt="dbt logo" width="500"/>
</p>

**[dbt](https://www.getdbt.com/)** enables data analysts and engineers to transform their data using the same practices that software engineers use to build applications.

dbt is the T in ELT. Organize, cleanse, denormalize, filter, rename, and pre-aggregate the raw data in your warehouse so that it's ready for analysis.

## dbt-yellowbrick
The dbt-yellowbrick adapter allows *[dbt](https://www.getdbt.com/)* to work with *[Yellowbrick Data Warehouse](https://yellowbrick.com)* and leverage the powerful capabilities of both platforms to build data analysis workflows. This adapter is based on the *postgres-adapter* with extensions to support Yellowbrick specific features.  

The dbt-yellowbrick adapter has been developed for projects that implement *dbt-core* through the command-line interface (CLI) which is free to use and available as an [open source project](https://github.com/dbt-labs/dbt-core).

## Getting Started

#### Setting up Locally

#### Connect to Github


## Features
dbt-yellowbrick supports the following Yellowbrick specific features:
* distribution
* clustering
* sort
* materialisations based on cross-database queries

<table>
<tr>
<td> model config </td> <td> generated sql </td>
</tr>
<tr>
<td> 

```yml
{{
  config(
    materialized = "table",
    dist = "replicate",
    sort_col = "stadium_capacity"
  )
}}
```

```sql
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

</td>
<td>

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
</td>
</tr>
<tr>
<td> 

```yml 
{{
  config(
    materialized = 'table',
    dist = 'match_key',
    cluster_cols = ['season_key', 'match_date_key', 'home_team_key', 'away_team_key']
  )
}}
``` 
```sql 
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
</td>
<td>

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
</td>
</tr>
</table>