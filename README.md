# Now

Date and time manipulations. Inspired by https://github.com/jinzhu/now.

## Example

```python
from datetime import datetime

import now

datetime.now()  # 2022-10-11 10:52:25.386472

now.beginning_of_minute()  # 2022-10-11 10:52:00
now.beginning_of_hour()  # 2022-10-11 10:00:00
now.beginning_of_day()  # 2022-10-11 00:00:00
now.beginning_of_week()  # 2022-10-09 00:00:00
now.beginning_of_month()  # 2022-10-01 00:00:00
now.beginning_of_quarter()  # 2022-10-01 00:00:00
now.beginning_of_half()  # 2022-07-01 00:00:00
now.beginning_of_year()  # 2022-01-01 00:00:00
now.end_of_minute()  # 2022-10-11 10:52:59.999999
now.end_of_hour()  # 2022-10-11 10:59:59.999999
now.end_of_day()  # 2022-10-11 23:59:59.999999
now.end_of_week()  # 2022-10-15 23:59:59.999999
now.end_of_month()  # 2022-10-31 23:59:59.999999
now.end_of_quarter()  # 2022-12-31 23:59:59.999999
now.end_of_half()  # 2022-12-31 23:59:59.999999
now.end_of_year()  # 2022-12-31 23:59:59.999999
```
