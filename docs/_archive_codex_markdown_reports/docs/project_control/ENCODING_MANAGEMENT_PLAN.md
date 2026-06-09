# Encoding Management Plan

## Current Issue

The current dataset can be read with more than one encoding. In the latest audit, 11 files were read as `utf-8-sig`, and 37 files required `cp1258` fallback.

This does not mean the raw data are unusable. It means the final analysis scripts should handle encoding carefully.

## Rule for Raw Data

Raw participant CSV files must not be modified. Do not open and resave raw files in Excel or another editor just to fix encoding.

## Analysis Approach

For final analysis, create standardized cleaned copies in a separate analysis folder. These cleaned copies can be written as UTF-8 after reading the raw files with encoding fallback. The raw data folder should remain unchanged.

## Item Grouping

Use `trial_id` as the main item key in QC and analysis. This reduces the risk that encoding differences in Vietnamese stimulus text affect item grouping.

## Documentation

Any encoding conversion for analysis should be documented in the analysis script and output folder. The documentation should state that cleaned files are derived copies, not replacements for raw data.

