#!/usr/bin/env Rscript
# =============================================================================
# analysis_R.R
# =============================================================================
# Independent R implementation of the Mann-Whitney U analysis for Chapter 4,
# Table 4.4.  This script reads the raw Excel data directly and computes all
# intermediate statistics from scratch, paralleling the Python implementation.
#
# Usage:
#   Rscript analysis_R.R
#
# Required packages: readxl (for Excel), stats (base R)
# Install if needed: install.packages("readxl")
#
# Author : Majharul Islam
# Date   : 2026-08-09
# =============================================================================

# --- Setup -------------------------------------------------------------------
if (!requireNamespace("readxl", quietly = TRUE)) {
  install.packages("readxl", repos = "https://cran.r-project.org")
}
library(readxl)

SCRIPT_DIR <- dirname(sys.frame(1)$ofile %||% ".")
if (SCRIPT_DIR == ".") SCRIPT_DIR <- getwd()

DATA_PATH <- file.path(SCRIPT_DIR, "data", "Mode_shift_bubt.xlsx")
OUTPUT_DIR <- file.path(SCRIPT_DIR, "outputs")
dir.create(OUTPUT_DIR, showWarnings = FALSE, recursive = TRUE)

# --- Column mapping ----------------------------------------------------------
# Exact raw column names (after trimming in R)
COLUMN_MAP <- list(
  security_harassment = "How safe do you feel regarding harassment, pickpocketing, or personal security?",
  reliability         = "How reliable is your current mode? (Does it arrive on time?)",
  road_accidents      = "How safe do you feel regarding road accidents on this mode?",
  comfort             = "How would you rate the physical comfort (Seating space, AC, Noise) of your current mode?",
  crowding            = "How crowded is the vehicle usually?"
)

LABELS <- list(
  security_harassment = "Safety: Harassment/Security",
  reliability         = "Reliability",
  road_accidents      = "Safety: Road Accidents",
  comfort             = "Comfort",
  crowding            = "Crowding"
)

# --- Load data ---------------------------------------------------------------
cat("Loading data from:", DATA_PATH, "\n")
df <- read_excel(DATA_PATH)
colnames(df) <- trimws(colnames(df))
cat("Loaded:", nrow(df), "rows x", ncol(df), "columns\n\n")

# Detect gender column
gender_col <- grep("gender", colnames(df), ignore.case = TRUE, value = TRUE)[1]
cat("Gender column:", gender_col, "\n")
df$Gender_clean <- trimws(as.character(df[[gender_col]]))
cat("Gender distribution:\n")
print(table(df$Gender_clean, useNA = "ifany"))
cat("\n")

# --- Detect outcome columns --------------------------------------------------
outcome_cols <- list()
for (short_name in names(COLUMN_MAP)) {
  pattern <- COLUMN_MAP[[short_name]]
  matched <- grep(pattern, colnames(df), fixed = TRUE, value = TRUE)
  if (length(matched) == 0) {
    # Try partial match
    matched <- grep(substr(pattern, 1, 30), colnames(df), fixed = TRUE, value = TRUE)
  }
  if (length(matched) == 0) {
    stop(paste("Cannot find column for:", short_name))
  }
  outcome_cols[[short_name]] <- matched[1]
  cat("Mapped:", short_name, "->", matched[1], "\n")
}

# =============================================================================
# MANN-WHITNEY U ANALYSIS (for each variable)
# =============================================================================

all_results <- data.frame()

for (short_name in names(outcome_cols)) {
  col_name <- outcome_cols[[short_name]]
  label <- LABELS[[short_name]]

  cat("\n", paste(rep("=", 60), collapse = ""), "\n")
  cat(label, "\n")
  cat(paste(rep("=", 60), collapse = ""), "\n")

  # Extract values by gender (complete cases)
  mask <- df$Gender_clean %in% c("Male", "Female") & !is.na(df[[col_name]])
  d <- df[mask, ]
  male   <- as.numeric(d[[col_name]][d$Gender_clean == "Male"])
  female <- as.numeric(d[[col_name]][d$Gender_clean == "Female"])

  # Remove any NAs from numeric conversion
  male   <- male[!is.na(male)]
  female <- female[!is.na(female)]

  n1 <- length(male)
  n2 <- length(female)
  N  <- n1 + n2

  cat("N Male:", n1, "| N Female:", n2, "| Total N:", N, "\n")

  # --- Descriptives ---
  cat("Male:   mean =", round(mean(male), 4),
      " median =", median(male),
      " SD =", round(sd(male), 4), "\n")
  cat("Female: mean =", round(mean(female), 4),
      " median =", median(female),
      " SD =", round(sd(female), 4), "\n")

  # --- Combined ranks ---
  combined <- c(male, female)
  ranks <- rank(combined, ties.method = "average")
  R1 <- sum(ranks[1:n1])            # Male rank sum
  R2 <- sum(ranks[(n1 + 1):N])      # Female rank sum

  cat("R1 (Male):", R1, "\n")
  cat("R2 (Female):", R2, "\n")

  # Identity check
  expected_rank_sum <- N * (N + 1) / 2
  cat("R1 + R2 =", R1 + R2, " | Expected N(N+1)/2 =", expected_rank_sum, "\n")
  if (abs(R1 + R2 - expected_rank_sum) > 1e-6) {
    cat("*** ERROR: RANK SUM IDENTITY FAILED ***\n")
  }

  # --- U1 and U2 ---
  U1 <- n1 * n2 + n1 * (n1 + 1) / 2 - R1
  U2 <- n1 * n2 + n2 * (n2 + 1) / 2 - R2

  cat("U1 (Male):", U1, "\n")
  cat("U2 (Female):", U2, "\n")

  # Identity check
  cat("U1 + U2 =", U1 + U2, " | Expected n1*n2 =", n1 * n2, "\n")
  if (abs(U1 + U2 - n1 * n2) > 1e-6) {
    cat("*** ERROR: U IDENTITY FAILED ***\n")
  }

  U_min <- min(U1, U2)
  cat("U (min) =", U_min, "\n")

  # --- Expected U ---
  mu_U <- n1 * n2 / 2
  cat("mu_U =", mu_U, "\n")

  # --- Tie correction ---
  tie_counts <- table(combined)
  tie_sum <- sum(as.numeric(tie_counts)^3 - as.numeric(tie_counts))
  cat("Tie groups:\n")
  print(tie_counts)
  cat("Sum(t^3 - t) =", tie_sum, "\n")

  var_U <- (n1 * n2 / 12) * ((N + 1) - tie_sum / (N * (N - 1)))
  sigma_U <- sqrt(var_U)
  cat("sigma_U (tie-corrected) =", sigma_U, "\n")

  # --- Z calculations ---
  Z_no_CC <- (U_min - mu_U) / sigma_U

  # Continuity correction
  cc <- ifelse(U_min < mu_U, 0.5, ifelse(U_min > mu_U, -0.5, 0))
  Z_CC <- (U_min - mu_U + cc) / sigma_U

  cat("Z (no CC) =", Z_no_CC, "\n")
  cat("Z (CC) =", Z_CC, "\n")

  # --- p-values ---
  p_no_CC <- 2 * pnorm(-abs(Z_no_CC))
  p_CC    <- 2 * pnorm(-abs(Z_CC))

  cat("p (no CC, manual) =", p_no_CC, "\n")
  cat("p (CC, manual) =", p_CC, "\n")

  # --- R wilcox.test cross-validation ---
  wt_cc   <- wilcox.test(male, female, alternative = "two.sided",
                         exact = FALSE, correct = TRUE)
  wt_nocc <- wilcox.test(male, female, alternative = "two.sided",
                         exact = FALSE, correct = FALSE)

  # R reports W = rank sum of first group = R1
  W_R <- as.numeric(wt_cc$statistic)
  # Convert W to U:  U1 = W - n1*(n1+1)/2
  U1_from_R <- W_R - n1 * (n1 + 1) / 2

  cat("R wilcox.test W:", W_R, "\n")
  cat("R wilcox.test U1 (from W):", U1_from_R, "\n")
  cat("R wilcox.test p (CC):", wt_cc$p.value, "\n")
  cat("R wilcox.test p (no CC):", wt_nocc$p.value, "\n")

  # --- Effect size ---
  r_effect <- abs(Z_no_CC) / sqrt(N)
  r_biserial <- 1 - (2 * U_min) / (n1 * n2)

  cat("Effect size r =", round(r_effect, 4), "\n")
  cat("Rank-biserial r =", round(r_biserial, 4), "\n")

  # --- Significance ---
  sig_label <- ifelse(p_no_CC < 0.05, "SIGNIFICANT", "not significant")
  cat("Decision (alpha=0.05):", sig_label, "\n")

  # --- Collect results ---
  row <- data.frame(
    Variable        = label,
    n1_male         = n1,
    n2_female       = n2,
    N               = N,
    male_mean       = round(mean(male), 4),
    male_median     = median(male),
    female_mean     = round(mean(female), 4),
    female_median   = median(female),
    R1_male         = R1,
    R2_female       = R2,
    U1_male         = U1,
    U2_female       = U2,
    U_min           = U_min,
    mu_U            = mu_U,
    tie_sum         = tie_sum,
    sigma_U         = round(sigma_U, 4),
    Z_no_CC         = round(Z_no_CC, 4),
    Z_CC            = round(Z_CC, 4),
    p_no_CC_manual  = round(p_no_CC, 6),
    p_CC_manual     = round(p_CC, 6),
    R_wilcox_p_CC   = round(wt_cc$p.value, 6),
    R_wilcox_p_noCC = round(wt_nocc$p.value, 6),
    effect_size_r   = round(r_effect, 4),
    rank_biserial   = round(r_biserial, 4),
    significant     = p_no_CC < 0.05,
    stringsAsFactors = FALSE
  )
  all_results <- rbind(all_results, row)
}

# =============================================================================
# EXPORT RESULTS
# =============================================================================
output_file <- file.path(OUTPUT_DIR, "mann_whitney_results_R.csv")
write.csv(all_results, output_file, row.names = FALSE)
cat("\n\nResults exported to:", output_file, "\n")

# Print summary table
cat("\n", paste(rep("=", 60), collapse = ""), "\n")
cat("SUMMARY TABLE (R)\n")
cat(paste(rep("=", 60), collapse = ""), "\n")
print(all_results[, c("Variable", "U_min", "Z_no_CC", "p_no_CC_manual",
                       "effect_size_r", "significant")])

cat("\nDone.\n")
