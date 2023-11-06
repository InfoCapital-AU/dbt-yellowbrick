{% macro sort_on(sort_col) %}
  {%- if sort_col is not none -%}
      {%- if sort_col is string -%}
        sort on ({{ sort_col }})
      {%- else -%}
        sort on ( {{ sort_col | first }} )
      {%- endif -%}
  {%- endif -%}
{%- endmacro -%}