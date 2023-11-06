{% macro cluster_on(cluster_cols) %}
  {%- if cluster_cols is not none -%}
      {%- if cluster_cols is string -%}
          cluster on ({{ cluster_cols }})
      {%- else -%}
        cluster on (
          {%- for item in cluster_cols -%}
            {{ item }}
            {%- if not loop.last -%},{%- endif -%}
          {%- endfor -%}
        )
      {%- endif -%}
  {%- endif -%}
{%- endmacro -%}