# Data Dictionary — Mode Shift BUBT Survey

## Source File

**Mode_shift_bubt.xlsx** — Raw survey data (319 respondents, 30 columns)

## Gender Variable

| Raw Column Name | `  Gender  ` (with leading/trailing spaces) |
|---|---|
| After trimming | `Gender` |
| Type | String |
| Values | `Male` (n = 214), `Female` (n = 105) |
| Mapping | Male → Group 1, Female → Group 2 |

**Important**: The raw data uses **text labels**, NOT numeric codes (1/2).
Scripts must handle string comparison, not integer comparison.

## Outcome Variables (Mann-Whitney U Analysis)

| Analysis Name | Raw Excel Column | Scale | Range |
|---|---|---|---|
| `security_harassment` | `How safe do you feel regarding harassment, pickpocketing, or personal security?` | Likert | 1–5 |
| `reliability` | `How reliable is your current mode? (Does it arrive on time?)` | Likert | 1–5 |
| `road_accidents` | `How safe do you feel regarding road accidents on this mode?` | Likert | 1–5 |
| `comfort` | `How would you rate the physical comfort (Seating space, AC, Noise) of your current mode?` | Likert | 1–5 |
| `crowding` | `How crowded is the vehicle usually?` | Likert | 1–5 |

## Scale Interpretation

### Security/Harassment, Road Accidents
- 1 = Very unsafe
- 5 = Very safe

### Reliability
- 1 = Very unreliable
- 5 = Very reliable

### Comfort
- 1 = Very uncomfortable
- 5 = Very comfortable

### Crowding
- 1 = Empty
- 5 = Very crowded

## Column Name Matching

Raw Excel columns have **trailing whitespace**. Scripts must use substring matching or strip whitespace before column detection. The `mann_whitney_utils.py` module handles this automatically.

## Total Sample

- **N = 319** respondents
- No missing values in the five outcome variables (all 319 have valid 1–5 responses)
- No missing Gender values

## Warning about "Reliability" Column

There are **TWO** reliability-related columns in the raw data:

1. ✅ `How reliable is your current mode? (Does it arrive on time?)` — **Likert 1–5** (correct)
2. ❌ `If your current mode arrived 10 minutes LATE three times a week, would you switch to a more reliable option?` — **Yes/No** (NOT the analysis variable)

The pipeline uses column #1 (Likert scale), matched by the fragment "How reliable is your current mode".