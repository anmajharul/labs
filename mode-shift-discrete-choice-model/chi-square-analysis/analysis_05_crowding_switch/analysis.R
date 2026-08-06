# ==============================================================================
# analysis.R - Analysis 05: Crowding x Switch Intent
# ==============================================================================
# Author : Majharul Islam
# Date   : 2026-08-07
# R      : 4.3+
# ==============================================================================

SCRIPT_DIR <- tryCatch(
  dirname(rstudioapi::getSourceEditorContext()$path),
  error = function(e) getwd()
)
REPO_ROOT <- dirname(SCRIPT_DIR)
DATA_PATH <- file.path(REPO_ROOT, "data", "Mode_shift_bubt.xlsx")
OUTPUT_DIR <- SCRIPT_DIR

source(file.path(REPO_ROOT, "chi_square_utils.R"))

message(rep("=", 60))
message("ANALYSIS 05 (R): Crowding x Switch Intent")
message(rep("=", 60))

results <- run_full_analysis(
  data_path        = DATA_PATH,
  row_keywords     = c("crowded"),
  col_keywords     = c("guarantees a seat"),
  row_var_label    = "Crowding x Switch Intent (Row)",
  col_var_label    = "Crowding x Switch Intent (Col)",
  table_title      = "Table 4.7: Switch by Crowding",
  output_dir       = OUTPUT_DIR,
  row_order        = c("Low (1-2)", "Moderate (3)", "High (4-5)"),
  col_order        = c("Yes", "No"),
  use_monte_carlo_ffh         = FALSE,
  use_monte_carlo_permutation = FALSE,
  n_replications   = 99999,
  seed             = 42,
  row_recode = c("1"="Low (1-2)","2"="Low (1-2)","3"="Moderate (3)","4"="High (4-5)","5"="High (4-5)")
)

cat("\n", rep("=", 60), "\n")
cat(paste0("ANALYSIS 05 RESULTS -- Crowding x Switch Intent\n"))
cat(rep("=", 60), "\n")
cat(sprintf("  Sample size (N)      : %d\n", results$n_total))
cat(sprintf("  Chi-square           : chi2(%d) = %.4f\n", results$degrees_of_freedom, results$chi2_statistic))
cat(sprintf("  P-value              : %.6f\n", results$p_value))
cat(sprintf("  Cramer V             : %.4f (%s)\n", results$cramers_v, results$effect_size_label))
cat(sprintf("  Decision: %s\n", results$decision))
cat(rep("=", 60), "\n")
cat(sprintf("Outputs saved to: %s\n", OUTPUT_DIR))
