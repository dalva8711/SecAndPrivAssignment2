# HR Dataset Statistical Analysis

This project performs statistical analysis on an HR dataset to investigate potential relationships between demographic factors and employment outcomes.

## Overview

The analysis examines three key claims using chi-square tests and independent t-tests:

1. **Claim 1**: Relationship between race/ethnicity and termination rates
2. **Claim 2**: Gender pay gap analysis
3. **Claim 3**: Relationship between race/ethnicity and performance scores

## Dataset

The analysis uses `HRDataset_v14.csv.xls`, which should contain employee data including:
- Race/Ethnicity information
- Gender/Sex
- Employment status or termination flag
- Pay rate/Salary information
- Performance scores

## Prerequisites

- Python 3.x
- Required Python packages:
  - pandas
  - numpy
  - scipy
  - openpyxl (for reading Excel files)

## Setup

### 1. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

### 2. Install Dependencies

```bash
pip install pandas numpy scipy openpyxl
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

## Usage

Run the analysis script:

```bash
python analysis.py
```

The script will:
1. Read the HR dataset
2. Perform statistical tests for each claim
3. Generate a `results.txt` file with the findings

## Output

The script generates `results.txt` containing:

- **Claim 1**: Chi-square test results and termination rates by race
- **Claim 2**: T-test results comparing male and female pay rates
- **Claim 3**: Chi-square test for race × performance relationship and ordinal t-test comparing minority vs. non-minority performance scores

## Statistical Methods

### Chi-Square Tests
Used to test independence between categorical variables (race/ethnicity and termination status, race/ethnicity and performance categories).

### Independent T-Tests
Used to compare means between two groups:
- Male vs. Female pay rates
- Minority vs. Non-minority performance scores (using ordinal encoding)

### Performance Score Encoding
Performance scores are converted to ordinal values:
- PIP = 0
- Needs Improvement = 1
- Fully Meets = 2
- Exceeds = 3

## Project Structure

```
.
├── README.md                    # This file
├── analysis.py                  # Main analysis script
├── HRDataset_v14.csv.xls       # HR dataset (required)
├── results.txt                  # Generated analysis results
└── requirements.txt             # Python dependencies (optional)
```

## Notes

- The script is designed to be flexible with column naming variations
- Missing data is handled through pandas dropna() operations
- Welch's t-test is used (equal_var=False) which doesn't assume equal variances

## License

This project is for educational purposes as part of Security and Privacy coursework.

