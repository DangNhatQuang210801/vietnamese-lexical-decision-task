# Levshina Chap 7

#### Tibor Kiss

#### 11.05.2025

### Step by step coding of Levshina, Chap. 7 (SS 2025)

#### Libraries and data

```r
library(tidyverse)
library(car)
```

#### Read-in data

```r
ELP <- 
  read.csv("ELP_course.csv", stringsAsFactors = TRUE)
```

```r
summary(ELP)
```

```
##            Word         Length         SUBTLWF         POS     
##  abbreviation:  1   Min.   : 3.00   Min.   :   0.020   JJ:159  
##  abortions   :  1   1st Qu.: 7.00   1st Qu.:   0.180   NN:532  
##  abrupt      :  1   Median : 8.00   Median :   0.570   VB:189  
##  absentee    :  1   Mean   : 8.22   Mean   :   8.603           
##  abutment    :  1   3rd Qu.:10.00   3rd Qu.:   2.105           
##  accomplice  :  1   Max.   :20.00   Max.   :2556.730           
##  (Other)     :874                                              
##     Mean_RT        log_SUBTLWF         Length_c    
##  Min.   : 517.5   Min.   :-3.9120   Min.   : 3.00  
##  1st Qu.: 695.7   1st Qu.:-1.7148   1st Qu.: 7.00  
##  Median : 764.5   Median :-0.5621   Median : 8.00  
##  Mean   : 786.8   Mean   :-0.4638   Mean   : 8.22  
##  3rd Qu.: 853.0   3rd Qu.: 0.7443   3rd Qu.:10.00  
##  Max.   :1324.6   Max.   : 7.8465   Max.   :20.00  
## 
```

#### Exploring the data employing graphics

```r
## Simpler plot

ggplot(ELP, aes(x = log_SUBTLWF, y = Mean_RT)) +
  geom_point(alpha = 0.5) +
  theme_bw() +
  labs(x = "Subtitle Word Frequency on log scale", y = "Mean Reaction Time (RT)")
```

```r
## Arithmetic scale for comparison

ggplot(ELP, aes(x = SUBTLWF, y = Mean_RT)) +
  geom_point(alpha = 0.5) +
  theme_bw() +
  labs(x = "Subtitle Word Frequency", y = "Mean Reaction Time (RT)")
```

```r
## More elaborate plot

ggplot(ELP, aes(x = log_SUBTLWF, y = Mean_RT, color = POS)) +
  geom_point(alpha = 0.5) +
  scale_color_brewer(name = "Parts of\nSpeech", labels = c("Adjective", "Noun", "Verb"), 
                     palette = "Set1") +
  theme_bw() +
  labs(x = "Subtitle Word Frequency on log scale", y = "Mean Reaction Time (RT)")
```

### First model

```r
ELP.lm1 <- lm(Mean_RT ~ log_SUBTLWF, data = ELP)

summary(ELP.lm1)
```

```
## 
## Call:
## lm(formula = Mean_RT ~ log_SUBTLWF, data = ELP)
## 
## Residuals:
##     Min      1Q  Median      3Q     Max 
## -227.70  -68.00  -15.76   52.20  432.46 
## 
## Coefficients:
##             Estimate Std. Error t value Pr(>|t|)    
## (Intercept)  769.112      3.595   214.0   <2e-16 ***
## log_SUBTLWF  -38.211      1.846   -20.7   <2e-16 ***
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## Residual standard error: 103.6 on 878 degrees of freedom
## Multiple R-squared:  0.3279, Adjusted R-squared:  0.3271 
## F-statistic: 428.3 on 1 and 878 DF,  p-value: < 2.2e-16
```

```r
ggplot(ELP, aes(x = log_SUBTLWF, y = Mean_RT)) +
  geom_point(color = "firebrick2", alpha = 0.3) +
  geom_line(aes(y = predict(ELP.lm1))) +
  theme_bw() +
  labs(x = "Subtitle Word Frequency (log)", y = "Mean Reaction Time (ms.)")
```

### Second model

```r
ELP.lm2 <- lm(Mean_RT ~ log_SUBTLWF + POS, data = ELP)

summary(ELP.lm2)
```

```
## 
## Call:
## lm(formula = Mean_RT ~ log_SUBTLWF + POS, data = ELP)
## 
## Residuals:
##     Min      1Q  Median      3Q     Max 
## -227.41  -66.29  -13.90   49.19  417.45 
## 
## Coefficients:
##             Estimate Std. Error t value Pr(>|t|)    
## (Intercept)  786.176      8.340  94.261  < 2e-16 ***
## log_SUBTLWF  -37.573      1.846 -20.354  < 2e-16 ***
## POSNN        -12.530      9.347  -1.341 0.180427    
## POSVB        -42.804     11.122  -3.849 0.000127 ***
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## Residual standard error: 102.7 on 876 degrees of freedom
## Multiple R-squared:  0.3408, Adjusted R-squared:  0.3385 
## F-statistic:   151 on 3 and 876 DF,  p-value: < 2.2e-16
```

```r
ggplot(ELP, aes(x = log_SUBTLWF, y = Mean_RT, color = POS)) +
  geom_point(alpha = 0.3) +
  geom_line(aes(y = predict(ELP.lm2))) +
  scale_color_brewer(name = "Parts of\nSpeech", labels = c("Adjective", "Noun", "Verb"), 
                     palette = "Set1") +
  theme_bw() +
  labs(x = "Subtitle Word Frequency (log)", y = "Mean Reaction Time (ms.)")
```

### Third model

We include `Length`, so the model corresponds to the one discussed in Levshina (2015, Chap. 7).

```r
ELP.lm3 <- 
  lm(Mean_RT ~ Length + log_SUBTLWF + POS, data = ELP)


summary(ELP.lm3)
```

```
## 
## Call:
## lm(formula = Mean_RT ~ Length + log_SUBTLWF + POS, data = ELP)
## 
## Residuals:
##     Min      1Q  Median      3Q     Max 
## -213.70  -62.55   -9.71   53.87  389.00 
## 
## Coefficients:
##             Estimate Std. Error t value Pr(>|t|)    
## (Intercept)  622.466     14.191  43.864  < 2e-16 ***
## Length        19.555      1.433  13.645  < 2e-16 ***
## log_SUBTLWF  -29.288      1.784 -16.420  < 2e-16 ***
## POSNN         -6.115      8.506  -0.719  0.47238    
## POSVB        -29.184     10.154  -2.874  0.00415 ** 
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## Residual standard error: 93.29 on 875 degrees of freedom
## Multiple R-squared:  0.4565, Adjusted R-squared:  0.454 
## F-statistic: 183.7 on 4 and 875 DF,  p-value: < 2.2e-16
```

### Plotting despite many dimensions

```r
table(ELP$Length)
```

```
## 
##   3   4   5   6   7   8   9  10  11  12  13  14  15  17  20 
##   6  31  71 109 125 158 141  93  76  34  20   6   8   1   1
```

```r
ELP <-
  ELP %>%
  mutate(Length_cat = ifelse(Length <= 6, "short", 
                             ifelse(Length <= 10, "medium", "long")),
         Length_cat = factor(Length_cat, levels = c("short", "medium", "long")))

summary(ELP)
```

```
##            Word         Length         SUBTLWF         POS     
##  abbreviation:  1   Min.   : 3.00   Min.   :   0.020   JJ:159  
##  abortions   :  1   1st Qu.: 7.00   1st Qu.:   0.180   NN:532  
##  abrupt      :  1   Median : 8.00   Median :   0.570   VB:189  
##  absentee    :  1   Mean   : 8.22   Mean   :   8.603           
##  abutment    :  1   3rd Qu.:10.00   3rd Qu.:   2.105           
##  accomplice  :  1   Max.   :20.00   Max.   :2556.730           
##  (Other)     :874                                              
##     Mean_RT        log_SUBTLWF         Length_c      Length_cat 
##  Min.   : 517.5   Min.   :-3.9120   Min.   : 3.00   short :217  
##  1st Qu.: 695.7   1st Qu.:-1.7148   1st Qu.: 7.00   medium:517  
##  Median : 764.5   Median :-0.5621   Median : 8.00   long  :146  
##  Mean   : 786.8   Mean   :-0.4638   Mean   : 8.22               
##  3rd Qu.: 853.0   3rd Qu.: 0.7443   3rd Qu.:10.00               
##  Max.   :1324.6   Max.   : 7.8465   Max.   :20.00               
## 
```

```r
ggplot(ELP, aes(x = log_SUBTLWF, y = Mean_RT, color = POS)) +
  geom_point(alpha = 0.3) +
  geom_smooth(method = "lm", se = FALSE) +
  scale_color_brewer(name = "Parts of\nSpeech", labels = c("Adjective", "Noun", "Verb"), 
                     palette = "Set1") +
  theme_bw() +
  facet_wrap(~Length_cat) +
  labs(x = "Subtitle Word Frequency (log)", y = "Mean Reaction Time (ms.)")
```

### Selecting predictors manually

Since we want to understand forward selection, we will look at the models 1, 2, and 3; which can be compared to Levshina (2015, Chap. 7)

```r
ELP.lm.null <- 
  lm(Mean_RT ~ 1, data = ELP)

summary(ELP.lm.null)
```

```
## 
## Call:
## lm(formula = Mean_RT ~ 1, data = ELP)
## 
## Residuals:
##     Min      1Q  Median      3Q     Max 
## -269.31  -91.13  -22.33   66.17  537.74 
## 
## Coefficients:
##             Estimate Std. Error t value Pr(>|t|)    
## (Intercept)  786.833      4.256   184.9   <2e-16 ***
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## Residual standard error: 126.2 on 879 degrees of freedom
```

```r
anova(ELP.lm.null, ELP.lm1, ELP.lm2, ELP.lm3)
```

```
## Analysis of Variance Table
## 
## Model 1: Mean_RT ~ 1
## Model 2: Mean_RT ~ log_SUBTLWF
## Model 3: Mean_RT ~ log_SUBTLWF + POS
## Model 4: Mean_RT ~ Length + log_SUBTLWF + POS
##   Res.Df      RSS Df Sum of Sq       F    Pr(>F)    
## 1    879 14009930                                   
## 2    878  9416345  1   4593585 527.825 < 2.2e-16 ***
## 3    876  9235246  2    181099  10.405 3.422e-05 ***
## 4    875  7614993  1   1620252 186.175 < 2.2e-16 ***
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
```

#### Comparison to forward selection

```r
lm3.fw <- step(ELP.lm.null, direction = "forward", scope = ~ Length + log_SUBTLWF + POS)
```

```
## Start:  AIC=8516.31
## Mean_RT ~ 1
## 
##               Df Sum of Sq      RSS    AIC
## + log_SUBTLWF  1   4593585  9416345 8168.7
## + Length       1   3901049 10108881 8231.1
## + POS          2    406956 13602974 8494.4
## <none>                     14009930 8516.3
## 
## Step:  AIC=8168.67
## Mean_RT ~ log_SUBTLWF
## 
##          Df Sum of Sq     RSS    AIC
## + Length  1   1709158 7707187 7994.4
## + POS     2    181099 9235246 8155.6
## <none>                9416345 8168.7
## 
## Step:  AIC=7994.41
## Mean_RT ~ log_SUBTLWF + Length
## 
##        Df Sum of Sq     RSS    AIC
## + POS   2     92194 7614993 7987.8
## <none>              7707187 7994.4
## 
## Step:  AIC=7987.82
## Mean_RT ~ log_SUBTLWF + Length + POS
```

```r
lm3.fw
```

```
## 
## Call:
## lm(formula = Mean_RT ~ log_SUBTLWF + Length + POS, data = ELP)
## 
## Coefficients:
## (Intercept)  log_SUBTLWF       Length        POSNN        POSVB  
##     622.466      -29.288       19.555       -6.115      -29.184
```

```r
drop1(ELP.lm3, test = "F")
```

```
## Single term deletions
## 
## Model:
## Mean_RT ~ Length + log_SUBTLWF + POS
##             Df Sum of Sq     RSS    AIC  F value  Pr(>F)    
## <none>                   7614993 7987.8                     
## Length       1   1620252 9235246 8155.6 186.1749 < 2e-16 ***
## log_SUBTLWF  1   2346341 9961335 8222.2 269.6061 < 2e-16 ***
## POS          2     92194 7707187 7994.4   5.2968 0.00517 ** 
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
```

### Application of forward selection to a model with interactions

```r
ELP.lm4 <- 
  lm(Mean_RT ~ log_SUBTLWF + Length + POS + log_SUBTLWF:POS + Length:POS, data = ELP)

summary(ELP.lm4)
```

```
## 
## Call:
## lm(formula = Mean_RT ~ log_SUBTLWF + Length + POS + log_SUBTLWF:POS + 
##     Length:POS, data = ELP)
## 
## Residuals:
##     Min      1Q  Median      3Q     Max 
## -218.93  -63.87   -8.72   52.31  380.94 
## 
## Coefficients:
##                   Estimate Std. Error t value Pr(>|t|)    
## (Intercept)        562.405     27.383  20.538  < 2e-16 ***
## log_SUBTLWF        -29.036      4.978  -5.833 7.69e-09 ***
## Length              26.419      3.169   8.337 2.96e-16 ***
## POSNN               79.221     31.345   2.527  0.01167 *  
## POSVB               14.651     38.270   0.383  0.70194    
## log_SUBTLWF:POSNN   -2.446      5.473  -0.447  0.65507    
## log_SUBTLWF:POSVB    4.463      6.073   0.735  0.46253    
## Length:POSNN       -10.045      3.658  -2.746  0.00615 ** 
## Length:POSVB        -4.607      4.615  -0.998  0.31842    
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## Residual standard error: 92.95 on 871 degrees of freedom
## Multiple R-squared:  0.4629, Adjusted R-squared:  0.458 
## F-statistic: 93.84 on 8 and 871 DF,  p-value: < 2.2e-16
```

```r
lm4.fw <- step(ELP.lm.null, direction = "forward", 
               scope = ~ log_SUBTLWF + Length + POS + log_SUBTLWF:POS + Length:POS)
```

```
## Start:  AIC=8516.31
## Mean_RT ~ 1
## 
##               Df Sum of Sq      RSS    AIC
## + log_SUBTLWF  1   4593585  9416345 8168.7
## + Length       1   3901049 10108881 8231.1
## + POS          2    406956 13602974 8494.4
## <none>                     14009930 8516.3
## 
## Step:  AIC=8168.67
## Mean_RT ~ log_SUBTLWF
## 
##          Df Sum of Sq     RSS    AIC
## + Length  1   1709158 7707187 7994.4
## + POS     2    181099 9235246 8155.6
## <none>                9416345 8168.7
## 
## Step:  AIC=7994.41
## Mean_RT ~ log_SUBTLWF + Length
## 
##        Df Sum of Sq     RSS    AIC
## + POS   2     92194 7614993 7987.8
## <none>              7707187 7994.4
## 
## Step:  AIC=7987.82
## Mean_RT ~ log_SUBTLWF + Length + POS
## 
##                   Df Sum of Sq     RSS    AIC
## + Length:POS       2     66673 7548321 7984.1
## <none>                         7614993 7987.8
## + log_SUBTLWF:POS  2     20050 7594943 7989.5
## 
## Step:  AIC=7984.08
## Mean_RT ~ log_SUBTLWF + Length + POS + Length:POS
## 
##                   Df Sum of Sq     RSS    AIC
## <none>                         7548321 7984.1
## + log_SUBTLWF:POS  2     23932 7524389 7985.3
```

```r
lm4.fw
```

```
## 
## Call:
## lm(formula = Mean_RT ~ log_SUBTLWF + Length + POS + Length:POS, 
##     data = ELP)
## 
## Coefficients:
##  (Intercept)   log_SUBTLWF        Length         POSNN         POSVB  
##      562.785       -29.365        26.339        74.834        24.127  
## Length:POSNN  Length:POSVB  
##       -9.381        -5.970
```

```r
drop1(ELP.lm4, test = "F")
```

```
## Single term deletions
## 
## Model:
## Mean_RT ~ log_SUBTLWF + Length + POS + log_SUBTLWF:POS + Length:POS
##                 Df Sum of Sq     RSS    AIC F value  Pr(>F)  
## <none>                       7524389 7985.3                  
## log_SUBTLWF:POS  2     23932 7548321 7984.1  1.3851 0.25084  
## Length:POS       2     70554 7594943 7989.5  4.0836 0.01717 *
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
```

### Assumptions third model

We are replicating the results from Levshina (2015).

#### Independency of observations

Levshina (2015: 155) already points out that this assumption is presumably violated. Whether or not independence abounds cannot be tested, but must be considered conceptually. If e.g. judgments or assessments come from a sample of students, where students repeatedly judge, then there judgments are dependent. If the sample is collected from students, where each students provides a single assessment, then the sample might be independent from students, but if the samples are identical, they might be depenedent on what has been chosen as a stimulus, e.g. from the words chosen.

#### Interval-scaled response variable

Crucially, interval-scaled response variables are such that distances have the same interpretation between intervals. (1000 - 500 ~ 1200 - 700; 1000/2 = 500, 1200/2 = 600, but in both cases twice the initial value.)

#### Linear relationship between quantitative independent variables and dependent variable

```r
crPlot(ELP.lm3, var = "Length")
```

```r
crPlot(ELP.lm3, var = "log_SUBTLWF")
```

#### Heteroscedasticity

```r
plot(ELP.lm3, which = 1)
```

```r
ncvTest(ELP.lm3)
```

```
## Non-constant Variance Score Test 
## Variance formula: ~ fitted.values 
## Chisquare = 79.67363, Df = 1, p = < 2.22e-16
```

```r
ncvTest(ELP.lm3, ~Length)
```

```
## Non-constant Variance Score Test 
## Variance formula: ~ Length 
## Chisquare = 42.39826, Df = 1, p = 7.4456e-11
```

```r
ncvTest(ELP.lm3, ~log_SUBTLWF)
```

```
## Non-constant Variance Score Test 
## Variance formula: ~ log_SUBTLWF 
## Chisquare = 59.12633, Df = 1, p = 1.4787e-14
```

```r
ELP$resid3 <- residuals(ELP.lm3)

ggplot(ELP, aes(x = log_SUBTLWF, y = resid3)) +
  geom_point() +
  theme_bw()
```

```r
ggplot(ELP, aes(x = Length, y = resid3)) +
  geom_point() +
  theme_bw()
```

#### Multicollinearity

```r
vif(ELP.lm3)
```

```
##                 GVIF Df GVIF^(1/(2*Df))
## Length      1.151054  1        1.072872
## log_SUBTLWF 1.150140  1        1.072446
## POS         1.026925  2        1.006664
```

```r
ELP <-
  ELP %>%
  mutate(Length1 = c(rep(8, 3), Length[4:length(Length)]))

ELP.test <- 
  lm(Mean_RT ~ Length + Length1 + log_SUBTLWF + POS, data = ELP)

vif(ELP.test)
```

```
##                   GVIF Df GVIF^(1/(2*Df))
## Length      543.443758  1       23.311880
## Length1     543.518917  1       23.313492
## log_SUBTLWF   1.150140  1        1.072446
## POS           1.028782  2        1.007119
```

```r
summary(ELP.test)
```

```
## 
## Call:
## lm(formula = Mean_RT ~ Length + Length1 + log_SUBTLWF + POS, 
##     data = ELP)
## 
## Residuals:
##     Min      1Q  Median      3Q     Max 
## -213.71  -62.56   -9.74   53.87  389.00 
## 
## Coefficients:
##             Estimate Std. Error t value Pr(>|t|)    
## (Intercept)  622.399     14.209  43.804  < 2e-16 ***
## Length        15.563     31.158   0.500  0.61755    
## Length1        3.999     31.184   0.128  0.89799    
## log_SUBTLWF  -29.288      1.785 -16.410  < 2e-16 ***
## POSNN         -6.103      8.511  -0.717  0.47352    
## POSVB        -29.134     10.167  -2.866  0.00426 ** 
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## Residual standard error: 93.34 on 874 degrees of freedom
## Multiple R-squared:  0.4565, Adjusted R-squared:  0.4534 
## F-statistic: 146.8 on 5 and 874 DF,  p-value: < 2.2e-16
```

#### Autocorrelation

```r
durbinWatsonTest(ELP.lm3)
```

```
##  lag Autocorrelation D-W Statistic p-value
##    1     0.006290341      1.986366   0.816
##  Alternative hypothesis: rho != 0
```

#### Normality of residuals

Normality can be rejected.

```r
shapiro.test(ELP$resid3)
```

```
## 
##  Shapiro-Wilk normality test
## 
## data:  ELP$resid3
## W = 0.9714, p-value = 4.005e-12
```

```r
ggplot(ELP, aes(sample = resid3)) +
  stat_qq() + 
  stat_qq_line() +
  theme_bw()
```

### Interactions, and plotting them

We already know that an interaction of `POS` and `Length` should be considered, while an interaction of `POS` and `log_SUBTLWF` does not suggest itself.

```r
ELP.lm4 <- 
  lm(Mean_RT ~ Length * POS + log_SUBTLWF, data = ELP)

summary(ELP.lm4)
```

```
## 
## Call:
## lm(formula = Mean_RT ~ Length * POS + log_SUBTLWF, data = ELP)
## 
## Residuals:
##     Min      1Q  Median      3Q     Max 
## -212.71  -64.20   -9.19   51.07  385.73 
## 
## Coefficients:
##              Estimate Std. Error t value Pr(>|t|)    
## (Intercept)   562.785     26.863  20.950  < 2e-16 ***
## Length         26.339      2.962   8.891  < 2e-16 ***
## POSNN          74.834     30.553   2.449  0.01451 *  
## POSVB          24.127     37.204   0.649  0.51683    
## log_SUBTLWF   -29.365      1.778 -16.512  < 2e-16 ***
## Length:POSNN   -9.381      3.397  -2.762  0.00587 ** 
## Length:POSVB   -5.970      4.332  -1.378  0.16852    
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## Residual standard error: 92.99 on 873 degrees of freedom
## Multiple R-squared:  0.4612, Adjusted R-squared:  0.4575 
## F-statistic: 124.6 on 6 and 873 DF,  p-value: < 2.2e-16
```

```r
drop1(ELP.lm4, test = "F")
```

```
## Single term deletions
## 
## Model:
## Mean_RT ~ Length * POS + log_SUBTLWF
##             Df Sum of Sq     RSS    AIC  F value  Pr(>F)    
## <none>                   7548321 7984.1                     
## log_SUBTLWF  1   2357274 9905595 8221.2 272.6302 < 2e-16 ***
## Length:POS   2     66673 7614993 7987.8   3.8555 0.02152 *  
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
```

```r
anova(ELP.lm3, ELP.lm4)
```

```
## Analysis of Variance Table
## 
## Model 1: Mean_RT ~ Length + log_SUBTLWF + POS
## Model 2: Mean_RT ~ Length * POS + log_SUBTLWF
##   Res.Df     RSS Df Sum of Sq      F  Pr(>F)  
## 1    875 7614993                              
## 2    873 7548321  2     66673 3.8555 0.02152 *
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
```

```r
ggplot(ELP, aes(x = Length, y = Mean_RT, color = POS)) +
  geom_point(alpha = 0.3) +
  geom_smooth(method = "lm", se = FALSE) +
  scale_color_brewer(name = "Parts of\nSpeech", labels = c("Adjective", "Noun", "Verb"), 
                     palette = "Set1") +
  theme_bw() +
  facet_wrap(~POS) +
  labs(x = "Word Length", y = "Mean Reaction Time (ms.)")
```
