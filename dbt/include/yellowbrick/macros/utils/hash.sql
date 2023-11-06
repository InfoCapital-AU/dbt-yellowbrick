{% macro yellowbrick__hash(field) -%}

    -- HASH(string [, algorithm ]). The default is 2 (SHA-2).
    hash(
        coalesce(
            cast({{ field }} as {{ type_string() }}),
            ''
        )
    )

{%- endmacro %}