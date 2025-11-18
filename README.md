# Bonnie Bully

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Bonnie Bully** is a Python package designed to simplify date manipulation. It provides an intuitive way to increment or decrement dates by years, months, days, or business days, with flexible alignment options.

## Features ✨

- 📆 **Multiple Intervals**: Support for `YEAR`, `MONTH`, `DAY`, and `BDAY` (business days)
- ⬅️➡️ **Bidirectional**: Increment dates forward or backward with positive/negative values
- 🎯 **Flexible Alignment**: Align results to beginning (`B`), end (`E`), or same day (`S`) of the interval
- 🏢 **Business Days**: Calculate business days with country/state-specific holiday support
- 📅 **Fiscal Calendar**: Support for fiscal week calendar (4-4-5 pattern) in addition to normal calendar
- 🌍 **International**: Support for holidays from multiple countries and regions
- 🔧 **Robust**: Comprehensive input validation and error handling

## Installation 📦

```bash
pip install bonniebully
```

## Quick Start 🚀

```python
from bonniebully import intdate
from datetime import date

# Get the first day of next month
next_month_start = intdate('MONTH', date.today(), 1, 'B').getDates()
print(f"Next month starts on: {next_month_start}")

# Get the last day of the year, 2 years ago
two_years_ago_end = intdate('YEAR', date.today(), -2, 'E').getDates()
print(f"End of year 2 years ago: {two_years_ago_end}")

# Get 3 business days from today (Brazil, São Paulo)
business_day = intdate('BDAY', date.today(), 3, 'S', "BR", "SP").getDates()
print(f"3 business days from today: {business_day}")
```

## API Reference 📚

### Class: `intdate`

```python
intdate(Interval, Date, Increment, Alignment, Country="", State="", Weekend=False, CalendarType="NORMAL")
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `Interval` | `str` | ✅ Yes | Interval type: `'YEAR'`, `'MONTH'`, `'DAY'`, or `'BDAY'` |
| `Date` | `date` or `str` | ✅ Yes | Reference date (format: `'YYYY-MM-DD'` if string) |
| `Increment` | `int` | ✅ Yes | Number of intervals to add (positive) or subtract (negative) |
| `Alignment` | `str` | ✅ Yes | Alignment: `'B'` (beginning), `'E'` (end), or `'S'` (same) |
| `Country` | `str` | ⚠️ Required for `BDAY` | Country code for holiday calculation (e.g., `'BR'`, `'US'`) |
| `State` | `str` | ❌ No | State/region code for regional holidays (e.g., `'SP'`, `'NY'`) |
| `Weekend` | `bool` | ❌ No | If `True`, Saturday is considered a business day (default: `False`) |
| `CalendarType` | `str` | ❌ No | Calendar type: `'NORMAL'` (default) or `'FISCAL'` (4-4-5 week pattern) |

#### Alignment Options

| Alignment | Description | Example (MONTH interval) |
|-----------|-------------|--------------------------|
| `'B'` | **Beginning**: First day of the interval | `2024-03-15` → `2024-04-01` |
| `'E'` | **End**: Last day of the interval | `2024-03-15` → `2024-04-30` |
| `'S'` | **Same**: Same relative day within the interval | `2024-03-15` → `2024-04-15` |

#### Methods

##### `getDates() -> date`

Returns the calculated date as a `date` object.

##### `getYearMonth() -> int`

Returns the calculated date as an integer in `YYYYMM` format (e.g., `202403` for March 2024).

## Examples 💡

### Year Intervals

```python
from bonniebully import intdate
from datetime import date

today = date(2024, 3, 15)

# Beginning of next year
next_year_start = intdate('YEAR', today, 1, 'B').getDates()
# Result: 2025-01-01

# End of previous year
last_year_end = intdate('YEAR', today, -1, 'E').getDates()
# Result: 2023-12-31

# Same day, 2 years from now
future_date = intdate('YEAR', today, 2, 'S').getDates()
# Result: 2026-03-15
```

### Month Intervals

```python
from bonniebully import intdate
from datetime import date

today = date(2024, 3, 15)

# First day of next month
next_month_start = intdate('MONTH', today, 1, 'B').getDates()
# Result: 2024-04-01

# Last day of previous month
last_month_end = intdate('MONTH', today, -1, 'E').getDates()
# Result: 2024-02-29 (leap year)

# Same day, 3 months ago
three_months_ago = intdate('MONTH', today, -3, 'S').getDates()
# Result: 2023-12-15

# Get year-month as integer
year_month = intdate('MONTH', today, 1, 'B').getYearMonth()
# Result: 202404
```

### Day Intervals

```python
from bonniebully import intdate
from datetime import date

today = date(2024, 3, 15)

# 10 days from today
future = intdate('DAY', today, 10, 'S').getDates()
# Result: 2024-03-25

# 5 days ago
past = intdate('DAY', today, -5, 'S').getDates()
# Result: 2024-03-10

# First day of the month containing the date 30 days from now
future_month_start = intdate('DAY', today, 30, 'B').getDates()
# Result: 2024-04-01
```

### Business Day Intervals

```python
from bonniebully import intdate
from datetime import date

today = date(2024, 3, 15)  # Friday

# 3 business days from today (Brazil, São Paulo)
# Skips weekends and holidays
next_business = intdate('BDAY', today, 3, 'S', "BR", "SP").getDates()
# Result: 2024-03-20 (skips weekend)

# 5 business days ago
prev_business = intdate('BDAY', today, -5, 'S', "BR", "SP").getDates()
# Result: 2024-03-08

# With Saturday as business day
next_business_sat = intdate('BDAY', today, 3, 'S', "BR", "SP", Weekend=True).getDates()
# Result: 2024-03-19 (only skips Sunday and holidays)
```

### Using String Dates

```python
from bonniebully import intdate

# You can pass dates as strings
result = intdate('MONTH', '2024-03-15', 1, 'B').getDates()
# Result: 2024-04-01
```

### Fiscal Calendar (4-4-5 Week Pattern)

The fiscal calendar follows a 4-4-5 week pattern where:
- Each fiscal month starts on a Monday and ends on a Sunday
- Fiscal months don't align with calendar months
- Fiscal year starts on the last complete-week Monday of November (previous calendar year)

```python
from bonniebully import intdate
from datetime import date

# Using fiscal calendar
fiscal_date = date(2025, 1, 15)

# Get first day of next fiscal month
next_fiscal_month = intdate('MONTH', fiscal_date, 1, 'B', CalendarType='FISCAL').getDates()
# Result: First Monday of the next fiscal month

# Get last day of current fiscal year
fiscal_year_end = intdate('YEAR', fiscal_date, 0, 'E', CalendarType='FISCAL').getDates()
# Result: Last Sunday of fiscal year 12

# Get same day, 3 fiscal months ahead
future_fiscal = intdate('MONTH', fiscal_date, 3, 'S', CalendarType='FISCAL').getDates()
# Result: Same relative day in 3 fiscal months ahead
```

**Fiscal Calendar Rules:**
- **Fiscal Month 1**: Starts on the last Monday of December (if day >= 28) or first Monday of January, ends on last Sunday of January
- **Fiscal Months 2-11**: Start on the last Monday of the corresponding calendar month, end on the last Sunday of the next calendar month (or first Sunday of the following month if needed to complete a full week)
- **Fiscal Month 12**: Starts on the last complete-week Monday of November, ends on the first Sunday of January (next calendar year) that completes a full week

## Real-World Use Cases 🌟

### Financial Reporting

```python
from bonniebully import intdate
from datetime import date

# Get end of current quarter (assuming Q1 ends in March)
current_date = date(2024, 2, 15)
quarter_end = intdate('MONTH', current_date, 1, 'E').getDates()
print(f"Q1 ends on: {quarter_end}")  # 2024-03-31

# Get start of next fiscal year (normal calendar)
fiscal_year_start = intdate('YEAR', current_date, 1, 'B').getDates()
print(f"Next fiscal year starts: {fiscal_year_start}")  # 2025-01-01

# Get start of next fiscal year (4-4-5 fiscal calendar)
fiscal_year_start_445 = intdate('YEAR', current_date, 1, 'B', CalendarType='FISCAL').getDates()
print(f"Next fiscal year (4-4-5) starts: {fiscal_year_start_445}")  # Last Monday of November

# Get end of current fiscal month (4-4-5)
fiscal_month_end = intdate('MONTH', current_date, 0, 'E', CalendarType='FISCAL').getDates()
print(f"Current fiscal month ends: {fiscal_month_end}")  # Last Sunday of current fiscal month
```

### Project Planning

```python
from bonniebully import intdate
from datetime import date

project_start = date(2024, 4, 1)

# Calculate project milestones (business days only)
milestone_1 = intdate('BDAY', project_start, 10, 'S', "US", "NY").getDates()
milestone_2 = intdate('BDAY', project_start, 30, 'S', "US", "NY").getDates()
milestone_3 = intdate('BDAY', project_start, 60, 'S', "US", "NY").getDates()

print(f"Milestone 1: {milestone_1}")
print(f"Milestone 2: {milestone_2}")
print(f"Milestone 3: {milestone_3}")
```

### Data Analysis

```python
from bonniebully import intdate
from datetime import date

# Compare same period last year
current_date = date(2024, 6, 15)
last_year_same = intdate('YEAR', current_date, -1, 'S').getDates()
print(f"Same date last year: {last_year_same}")  # 2023-06-15

# Get month-over-month comparison
last_month = intdate('MONTH', current_date, -1, 'S').getDates()
print(f"Same day last month: {last_month}")  # 2024-05-15
```

## Error Handling ⚠️

The package includes comprehensive input validation:

```python
from bonniebully import intdate
from datetime import date

# Invalid interval
try:
    intdate('WEEK', date.today(), 1, 'B')
except ValueError as e:
    print(e)  # "Interval deve ser 'YEAR', 'MONTH', 'DAY' ou 'BDAY'"

# Missing country for business days
try:
    intdate('BDAY', date.today(), 1, 'S')
except ValueError as e:
    print(e)  # "Country é obrigatório quando Interval é 'BDAY'"

# Invalid alignment
try:
    intdate('MONTH', date.today(), 1, 'X')
except ValueError as e:
    print(e)  # "Alignment deve ser 'B', 'E' ou 'S'"

# Invalid calendar type
try:
    intdate('MONTH', date.today(), 1, 'B', CalendarType='INVALID')
except ValueError as e:
    print(e)  # "CalendarType deve ser 'NORMAL' ou 'FISCAL'"
```

## Dependencies 📋

- `python-dateutil` - Date manipulation utilities
- `holidays` - Country-specific holiday calculations

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author 👤

**Delvidio Demarchi Neto**

- Email: delvidio.neto@outlook.com.br
- GitHub: [@delvidioneto](https://github.com/delvidioneto)

---

**Made with ❤️ for the Python community**
