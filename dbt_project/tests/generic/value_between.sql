{% test value_between(model, column_name, min_value, max_value) %}
-- Fails on any value outside [min_value, max_value]. NULLs pass: pair with not_null if they shouldn't.
select {{ column_name }}
from {{ model }}
where {{ column_name }} < {{ min_value }}
   or {{ column_name }} > {{ max_value }}
{% endtest %}
