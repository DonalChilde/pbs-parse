# Input and Output

The process starts with the pdf bid package for each base.

1. Extract text from the pdf file using the included tool.
2. Save each `page` of trips to a json file, along with the extra information needed for parsing.
3. Split each json `page` into individual `trips`, and save them as json files. The header and footer lines, as well as the bid information from the page is copied into each trip in order to make the json trip the smallest complete unit of data for later parsing.
4. Parse the split trips, identifying the data inside - eg. flight numbers and block times. Save this as a json file.
5. Expand each parsed trip such that each expanded trip represents a trip that starts on a particular day, with fully qualified datetimes. Save as json.

## Page

When the page is split off from the source text, some data about the bid package is included in the result.

### The source for a page of trips

```{literalinclude} includes/page-00003.txt
:language: TEXT
:text:
:caption: page-00003.txt


```

### The json for a page of trips

```{literalinclude} includes/page-lines_2025-03_PHX_00003-00.json
:language: JSON
:caption: page-lines_2025-03_PHX_00003-00.json
```

## Raw Trip

The json for a trip split from a page contains all the lines of the trip, plus the page header and footer lines, along with the bid package data that was stored in the page json. This allows the raw trip to be a complete set of data needed for parsing and expanding later.

### The json for a raw Trip

```{literalinclude} includes/trip-lines_2025-03_PHX_00003-01.json
:language: JSON
:caption: trip-lines_2025-03_PHX_00003-01.json
```

## Parsed Trip

The parsed trip json contains a copy of the source lines, as well as the data parsed from those lines.

### The json for a parsed Trip

```{literalinclude} includes/parsed-trip_2025-03_PHX_00003-01.json
:language: JSON
:caption: parsed-trip_2025-03_PHX_00003-01.json
```

## Expanded Trip

Because a trip from the pairing package might operate several times in one month, the trips need to be expanded for efficient sorting and filtering. All times are fully qualified datetimes with timezones.

### The json for an expanded Trip

```{literalinclude} includes/expanded-trip_2025-03_PHX_320_2025-03-23_10645.json
:language: JSON
:caption: expanded-trip_2025-03_PHX_320_2025-03-23_10645.json
```
