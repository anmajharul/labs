
# ============================================================
# CHAPTER 4 - Mann-Whitney U reproducibility script
# IMPORTANT:
# Replace DATA_PATH and column names if your raw dataset differs.
# Gender must be coded 1=Male, 2=Female.
# ============================================================

DATA_PATH <- "data/chapter4_raw.csv"
GENDER_COL <- "Gender"
OUTCOME_COL <- "crowding"

dat <- read.csv(DATA_PATH, stringsAsFactors = FALSE)

d <- dat[complete.cases(dat[, c(GENDER_COL, OUTCOME_COL)]),
         c(GENDER_COL, OUTCOME_COL)]

male <- as.numeric(d[d[[GENDER_COL]] == 1, OUTCOME_COL])
female <- as.numeric(d[d[[GENDER_COL]] == 2, OUTCOME_COL])

cat("N male:", length(male), "\n")
cat("N female:", length(female), "\n")
cat("Total N:", length(male) + length(female), "\n")

# R's wilcox.test reports the rank-based statistic for the first group.
# exact=FALSE is required/appropriate with ties.
wt <- wilcox.test(male, female,
                  alternative = "two.sided",
                  exact = FALSE,
                  correct = TRUE)

cat("\nWilcoxon/Mann-Whitney W (first group):", wt$statistic, "\n")
cat("Two-sided p-value:", wt$p.value, "\n")

n1 <- length(male)
n2 <- length(female)
N <- n1 + n2

# Convert W to U
W1 <- as.numeric(wt$statistic)
U1 <- W1 - n1 * (n1 + 1) / 2
U2 <- n1*n2 - U1
U <- min(U1, U2)

cat("\nU1 (Male):", U1, "\n")
cat("U2 (Female):", U2, "\n")
cat("Reported U = min(U1,U2):", U, "\n")

# Rank-sum cross-check
values <- c(male, female)
ranks <- rank(values, ties.method = "average")
R1 <- sum(ranks[seq_len(n1)])
R2 <- sum(ranks[(n1+1):N])

cat("\nR1 (Male):", R1, "\n")
cat("R2 (Female):", R2, "\n")
cat("R1+R2:", R1+R2, "\n")

# Tie-corrected variance and Z
tie_counts <- table(values)
tie_sum <- sum(tie_counts^3 - tie_counts)

mu_U <- n1*n2/2
sigma_U <- sqrt((n1*n2/12) *
                ((N+1) - tie_sum/(N*(N-1))))

# No-continuity-correction Z
z_nocc <- (U - mu_U) / sigma_U
p_nocc <- 2 * pnorm(-abs(z_nocc))

# Continuity correction toward the mean
cc <- ifelse(U < mu_U, 0.5, -0.5)
z_cc <- (U - mu_U + cc) / sigma_U
p_cc <- 2 * pnorm(-abs(z_cc))

cat("\nTie sizes:", paste(as.integer(tie_counts), collapse=", "), "\n")
cat("Sum(t^3-t):", tie_sum, "\n")
cat("Expected mean mu_U:", mu_U, "\n")
cat("Tie-corrected sigma_U:", sigma_U, "\n")
cat("Z (no continuity correction):", z_nocc, "\n")
cat("p from Z (no continuity correction):", p_nocc, "\n")
cat("Z (with continuity correction):", z_cc, "\n")
cat("p from Z (with continuity correction):", p_cc, "\n")

cat("\nDescriptives:\n")
cat("Male mean / median:", mean(male), "/", median(male), "\n")
cat("Female mean / median:", mean(female), "/", median(female), "\n")

# NOTE:
# Different software may report W or U and may use different continuity/tie
# conventions. Verify the raw-data result before copying numbers into the thesis.
