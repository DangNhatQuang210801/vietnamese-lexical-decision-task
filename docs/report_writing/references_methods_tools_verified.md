# RP2 Methods, Statistics, and Software References - Verified Draft

Scope: Verified core methods, statistics, and software references for RP2. Visual word recognition and Vietnamese-specific references are handled in separate reference files.

## Verification Summary

- Verified items: 9
- Items with minor uncertainty: 1
- Main uncertainty: McKinney (2010) is verified as a pandas/SciPy proceedings source, but secondary databases show inconsistent page ranges. Use the DOI/proceedings version if possible.
- R citation is version-dependent. The citation below was generated from the local installed R 4.6.0 using `citation()` on 2026-05-02.

## Verified APA 7 References

### Mixed-Effects Models and Linguistic Statistics

Baayen, R. H. (2008). *Analyzing linguistic data: A practical introduction to statistics using R*. Cambridge University Press. https://doi.org/10.1017/CBO9780511801686

- Status: verified.
- Verification source: Cambridge University Press page confirms title, author, publisher, 2008 publication year, DOI, ISBN, and page extent.
- Use in RP2: General statistics reference for language data analysis, transformations, regression, and mixed-effects analysis.

Baayen, R. H., Davidson, D. J., & Bates, D. M. (2008). Mixed-effects modeling with crossed random effects for subjects and items. *Journal of Memory and Language, 59*(4), 390-412. https://doi.org/10.1016/j.jml.2007.12.005

- Status: verified.
- Verification source: Max Planck repository confirms authors, year, title, journal, volume, issue, pages, and DOI.
- Use in RP2: Core justification for mixed-effects models with crossed random effects for participants and items.

Bates, D., Mächler, M., Bolker, B., & Walker, S. (2015). Fitting linear mixed-effects models using lme4. *Journal of Statistical Software, 67*(1), 1-48. https://doi.org/10.18637/jss.v067.i01

- Status: verified.
- Verification source: Journal of Statistical Software page confirms authors, publication date, journal, volume, issue, pages, and DOI.
- Use in RP2: Citation for the `lme4` package and linear mixed-effects model implementation.

Levshina, N. (2015). *How to do linguistics with R: Data exploration and statistical analysis*. John Benjamins Publishing Company. https://doi.org/10.1075/z.195

- Status: verified.
- Verification source: John Benjamins/De GruyterBrill catalog record confirms author, title, publisher, 2015 year, and DOI.
- Use in RP2: Applied linguistic statistics reference, especially for R-based data exploration and regression-oriented workflows.

Winter, B. (2019). *Statistics for linguists: An introduction using R*. Routledge. https://doi.org/10.4324/9781315165547

- Status: verified.
- Verification source: Routledge page confirms title, author, publisher, page count, and edition; Crossref/CiNii record confirms DOI and 2019 publication metadata.
- Use in RP2: Accessible reference for linear models, mixed models, transformations, centering/standardization, and reproducible analysis in linguistics.

### PsychoPy and Experiment Implementation

Peirce, J. W. (2007). PsychoPy: Psychophysics software in Python. *Journal of Neuroscience Methods, 162*(1-2), 8-13. https://doi.org/10.1016/j.jneumeth.2006.11.017

- Status: verified.
- Verification source: ScienceDirect and PsychoPy official citation page confirm title, journal, volume, issue, pages, and DOI.
- Use in RP2: Citation for PsychoPy as experiment-control software.
- Note: The original title uses a dash between "PsychoPy" and "Psychophysics"; the colon form above is APA-clean and semantically equivalent. If strict title transcription is required, use `PsychoPy - Psychophysics software in Python`.

Peirce, J. W., Gray, J. R., Simpson, S., MacAskill, M. R., Höchenberger, R., Sogo, H., Kastman, E., & Lindeløv, J. K. (2019). PsychoPy2: Experiments in behavior made easy. *Behavior Research Methods, 51*, 195-203. https://doi.org/10.3758/s13428-018-01193-y

- Status: verified.
- Verification source: Springer page confirms authors, title, journal, publication date, volume, pages, and DOI.
- Use in RP2: Recommended citation for modern PsychoPy/PsychoPy2 experiment implementation, especially if using Builder-compatible or current PsychoPy workflows.

### Python Data Processing and R Software

McKinney, W. (2010). Data structures for statistical computing in Python. In S. van der Walt & J. Millman (Eds.), *Proceedings of the 9th Python in Science Conference* (pp. 56-61). SciPy. https://doi.org/10.25080/Majora-92bf1922-00a

- Status: verified with minor page-range caution.
- Verification source: SciPy Proceedings page confirms title, author, date, and DOI. SciPy index, DBLP, CiNii, and other databases support the proceedings citation.
- Needs verification: Page range is inconsistent across secondary sources. Several sources list 56-61; some list 51-56. The DOI and official proceedings page are stable, so the DOI-based citation is safest.
- Use in RP2: Citation for pandas/data-frame infrastructure if pandas was used in stimulus processing.

R Core Team. (2026). *R: A language and environment for statistical computing*. R Foundation for Statistical Computing. https://doi.org/10.32614/R.manuals

- Status: verified from local R 4.6.0 `citation()` output.
- Verification source: Local R citation output on 2026-05-02 returned: R Core Team (2026), R Foundation for Statistical Computing, Vienna, Austria, DOI 10.32614/R.manuals, and https://www.R-project.org/.
- Needs verification: Update the year/version if the final analysis is run with a different R version.
- Use in RP2: Citation for R if R is used for the final `lme4` analysis.

## Optional PsychoPy Source To Verify Later

Peirce, J. W. (2009). Generating stimuli for neuroscience using PsychoPy. *Frontiers in Neuroinformatics, 2*, Article 10. https://doi.org/10.3389/neuro.11.010.2008

- Status: needs verification.
- Reason not included above as fully verified: It appears on the official PsychoPy citation page and in the 2019 PsychoPy2 article references, but it was not part of the core partial candidate list being completed here.
- Use only if needed: The 2019 PsychoPy2 paper is probably the better citation for the current RP2 script/workflow.

## Sources Consulted

- Cambridge University Press: https://www.cambridge.org/highereducation/books/analyzing-linguistic-data/B2AF752A30911F4144CA35E075C6B233
- Max Planck repository record for Baayen, Davidson, and Bates (2008): https://pure.mpg.de/pubman/faces/ViewItemFullPage.jsp?itemId=item_60973_2
- Journal of Statistical Software lme4 article: https://www.jstatsoft.org/article/view/v067i01
- John Benjamins / De GruyterBrill record for Levshina (2015): https://www.degruyterbrill.com/document/doi/10.1075/z.195/html
- Routledge page for Winter (2019): https://www.routledge.com/Statistics-for-Linguists-An-Introduction-Using-R/Winter/p/book/9781138056091
- Crossref DOI for Winter (2019): https://doi.org/10.4324/9781315165547
- ScienceDirect page for Peirce (2007): https://www.sciencedirect.com/science/article/pii/S0165027006005772
- PsychoPy official citation page: https://psychopy.org/about/
- Springer page for Peirce et al. (2019): https://link.springer.com/article/10.3758/s13428-018-01193-y
- SciPy Proceedings page for McKinney (2010): https://proceedings.scipy.org/articles/Majora-92bf1922-00a
- R Project homepage: https://www.r-project.org/
- Local R command used: `Rscript -e "citation()"`

## Next Recommended Action

Use these methods/tools references in the report methods and planned analysis sections. Continue a separate, targeted verification pass for visual word recognition and Vietnamese orthography sources; do not mix those into this file.
