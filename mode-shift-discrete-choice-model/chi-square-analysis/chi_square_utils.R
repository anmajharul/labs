# ==============================================================================
# chi_square_utils.R — Shared R utilities for Chi-Square Analyses
# Author : Majharul Islam
# Date   : 2026-08-07
# ==============================================================================
suppressPackageStartupMessages({
  library(readxl)
  library(dplyr)
  library(janitor)
  library(officer)
  library(flextable)
})

load_dataset <- function(data_path) {
  df <- read_excel(data_path, sheet = 1)
  colnames(df) <- trimws(colnames(df))
  return(df)
}

detect_column <- function(df, keywords) {
  col_names <- colnames(df)
  for (kw in keywords) {
    matches <- col_names[grepl(kw, col_names, ignore.case = TRUE)]
    if (length(matches) > 0) return(matches[1])
  }
  stop("Column not found")
}

check_missing_values <- function(df, cols) {
  return(df[complete.cases(df[, cols, drop = FALSE]), ])
}

compute_cramers_v <- function(chi2, n, n_rows, n_cols) {
  phi2 <- chi2 / n
  r_corr <- n_rows - 1
  c_corr <- n_cols - 1
  phi2_corr <- max(0, phi2 - (r_corr * c_corr) / (n - 1))
  r_adj <- r_corr - (r_corr - 1)^2 / (n - 1)
  c_adj <- c_corr - (c_corr - 1)^2 / (n - 1)
  denom <- min(max(r_adj, 0), max(c_adj, 0))
  if (denom == 0) return(0.0)
  return(round(sqrt(phi2_corr / denom), 4))
}

interpret_cramers_v <- function(v) {
  if (v < 0.10) return("negligible")
  else if (v < 0.20) return("small")
  else if (v < 0.40) return("moderate")
  else return("large")
}

make_decision <- function(p_val, alpha = 0.05) {
  if (p_val < alpha) return(sprintf("Reject H0 (p = %.4f < alpha = %.2f).", p_val, alpha))
  else return(sprintf("Fail to reject H0 (p = %.4f >= alpha = %.2f).", p_val, alpha))
}

run_full_analysis <- function(data_path, row_keywords, col_keywords, row_var_label, col_var_label, table_title, output_dir, row_order=NULL, col_order=NULL, use_monte_carlo_ffh=FALSE, use_monte_carlo_permutation=FALSE, n_replications=99999, seed=42, row_recode=NULL, col_recode=NULL) {
  dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)
  df <- load_dataset(data_path)
  row_col <- detect_column(df, row_keywords)
  col_col <- detect_column(df, col_keywords)
  df <- check_missing_values(df, c(row_col, col_col))

  if (!is.null(row_recode)) {
    df[["_row_recoded"]] <- row_recode[as.character(df[[row_col]])]
    df <- df[!is.na(df[["_row_recoded"]]), ]
    row_col <- "_row_recoded"
  }
  if (!is.null(col_recode)) {
    df[["_col_recoded"]] <- col_recode[as.character(df[[col_col]])]
    df <- df[!is.na(df[["_col_recoded"]]), ]
    col_col <- "_col_recoded"
  }

  obs <- table(df[[row_col]], df[[col_col]])
  test_res <- chisq.test(obs, correct = FALSE)
  chi2 <- as.numeric(test_res$statistic)
  p_val <- test_res$p.value
  dof <- test_res$parameter
  cramers_v <- compute_cramers_v(chi2, nrow(df), nrow(obs), ncol(obs))
  v_interp <- interpret_cramers_v(cramers_v)
  decision <- make_decision(p_val)

  results <- list(
    analysis = table_title, row_variable = row_var_label, col_variable = col_var_label,
    n_total = nrow(df), chi2_statistic = round(chi2, 4), degrees_of_freedom = dof,
    p_value = round(p_val, 6), cramers_v = cramers_v, effect_size_label = v_interp, decision = decision
  )
  return(results)
}
