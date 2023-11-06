{% macro dist(dist) %}
  {%- if dist is not none -%}
      {%- if dist is string -%}
        {%- if dist.upper() in ['RANDOM', 'REPLICATE'] -%}
          distribute {{ dist.upper() }}
        {%- else -%}
          distribute on ({{ dist }})
        {%- endif -%}
      {%- else -%}
        distribute on ( {{ dist | first }} )
      {%- endif -%}
  {%- endif -%}
{%- endmacro -%}