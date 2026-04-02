# Vietnamese Lexical Decision Task

## Overview
This project investigates how word frequency and syllable-based word length influence reaction times in Vietnamese visual word recognition.

The study is based on a lexical decision task (LDT), in which participants decide whether a presented stimulus is a real Vietnamese word or a pseudoword. Reaction times are used to understand how quickly lexical access occurs.

## Research Question
How do word frequency and word length (measured in syllables) affect reaction times in Vietnamese, and do these factors interact?

## Motivation
Most psycholinguistic research on visual word recognition has focused on Indo-European languages such as English. Vietnamese presents a different case due to its orthographic structure, where spaces often separate syllables rather than full lexical words.

This project aims to test whether well-established effects (frequency and length) generalize to Vietnamese.

## Notes
- Large raw datasets are excluded from the repository.
- Only sample or processed data is included for reproducibility.

## Status
Project setup and data preparation in progress.

## Methodology

### Experimental Design
- Task: Lexical Decision Task
- Language: Vietnamese (Chữ Quốc Ngữ)
- Participants: 40–60 native speakers

### Stimuli
- ~120–160 real words
- ~120–160 pseudowords
- Word frequency obtained from a Vietnamese corpus (log-transformed)
- Word length measured as number of syllables

### Procedure
- Fixation cross (≈500 ms)
- Stimulus presentation
- Participant response (word / non-word)
- Reaction time and accuracy recorded

## Variables

### Dependent Variable
- Reaction time (milliseconds)

### Independent Variables
- Word frequency (log-transformed)
- Word length (number of syllables)

### Interaction
- Frequency × Length

## Data Analysis
- Linear mixed-effects models (R, lme4)
- Random effects:
  - Participants
  - Items
- Preprocessing:
  - Remove incorrect responses
  - Remove outliers

## Repository Structure
vietnamese-lexical-decision-task/
├── data/ # sample or cleaned corpus data
├── experiment/ # PsychoPy experiment scripts
├── analysis/ # R scripts (mixed-effects models)
├── scripts/ # preprocessing and data handling
├── results/ # outputs, figures, tables
├── VietnameseCorpus.ipynb
├── README.md
└── .gitignore
  - Log-transform reaction times

## Repository Structure
