/* For examples of how to fill out the macros please refer to the postgres adapter and docs
postgres adapter macros: https://github.com/dbt-labs/dbt-core/blob/main/plugins/postgres/dbt/include/postgres/macros/adapters.sql
dbt docs: https://docs.getdbt.com/docs/contributing/building-a-new-adapter
*/

{% macro postgres__create_table_as(temporary, relation, sql) -%}

  {%- set _dist = config.get('dist') -%}
  {%- set _sort_col = config.get('sort_col') -%}
  {%- set _cluster_cols = config.get('cluster_cols') -%}
  {%- set sql_header = config.get('sql_header', none) -%}

  {{ sql_header if sql_header is not none }}

    {{log('Distribution: ' ~ _dist, True)}}
    {{log('Sort: ' ~ _sort_col, True)}}
    {{log('Cluster: ' ~ _cluster_cols, True)}}

  create {% if temporary -%}temporary{%- endif %} table if not exists
    {{ relation }}
  as (
    {{ sql }}
  )
  {{ dist(_dist) }}
  {{ sort_on(_sort_col) }}
  {{ cluster_on(_cluster_cols) }}
  ;
{%- endmacro %}

{% macro yellowbrick__alter_column_type(relation,column_name,new_column_type) -%}
'''Changes column name or data type'''
  {{ return(postgres__alter_column_comment(relation, column_dict)) }}
{% endmacro %}

{% macro yellowbrick__check_schema_exists(information_schema, schema) -%}
  {{ return(postgres__check_schema_exists(information_schema, schema)) }}
{% endmacro %}


{% macro yellowbrick__create_schema(relation) -%}
'''Creates a new schema in the  target database, if schema already exists, method is a no-op. '''
  {{ return(postgres__create_schema(relation)) }}
{% endmacro %}


{% macro yellowbrick__drop_schema(relation) -%}
'''drops a schema in a target database.'''
  {{ return(postgres__drop_schema(relation)) }}
{% endmacro %}


{% macro yellowbrick__get_columns_in_relation(relation) -%}
'''Returns a list of Columns in a table.'''
  {{ return(postgres__get_columns_in_relation(relation)) }}
{% endmacro %}


{% macro yellowbrick__list_relations_without_caching(schema_relation) -%}
'''creates a table of relations withough using local caching.'''
  {{ return(postgres__list_relations_without_caching(schema_relation)) }}
{% endmacro %}


{% macro yellowbrick__list_schemas(database) -%}
'''Returns a table of unique schemas.'''
  {{ return(postgres__list_schemas(database)) }}
{% endmacro %}


{% macro yellowbrick__current_timestamp() -%}
  {{ return(postgres__current_timestamp()) }}
{%- endmacro %}


{% macro yellowbrick_escape_comment(comment) -%}
  {{ return(postgres_escape_comment(comment)) }}
{%- endmacro %}


{% macro yellowbrick__alter_relation_comment(relation, comment) %}
  {{ return(postgres__alter_relation_comment(relation, comment) ) }}
{% endmacro %}


{% macro yellowbrick__alter_column_comment(relation, column_dict) %}
  {{ return(postgres__alter_column_comment(relation, column_dict)) }}
{% endmacro %}


{% macro yellowbrick__copy_grants() %}
    {{ return(False) }}
{% endmacro %}