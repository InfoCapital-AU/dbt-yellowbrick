{% macro yellowbrick__snapshot_merge_sql(target, source, insert_cols) -%}
    {%- set insert_cols_csv = insert_cols | join(', ') -%}

    '''Note the varchar default length is 256 in YB'''

    update {{ target }}
    set dbt_valid_to = DBT_INTERNAL_SOURCE.dbt_valid_to
    from {{ source }} as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_scd_id::varchar = {{ target }}.dbt_scd_id::varchar
      and DBT_INTERNAL_SOURCE.dbt_change_type::text in ('update'::varchar, 'delete'::varchar)
      and {{ target }}.dbt_valid_to is null;

    insert into {{ target }} ({{ insert_cols_csv }})
    select {% for column in insert_cols -%}
        DBT_INTERNAL_SOURCE.{{ column }} {%- if not loop.last %}, {%- endif %}
    {%- endfor %}
    from {{ source }} as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_change_type::text = 'insert'::varchar;
{% endmacro %}