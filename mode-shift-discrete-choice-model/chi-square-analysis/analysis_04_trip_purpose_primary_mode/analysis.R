# ==============================================================================
# analysis.R - Analysis 04: Trip Purpose x Primary Mode
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
message("ANALYSIS 04 (R): Trip Purpose x Primary Mode")
message(rep("=", 60))

results <- run_full_analysis(
  data_path        = DATA_PATH,
  row_keywords     = c("primary purpose"),
  col_keywords     = c("PRIMARY mode"),
  row_var_label    = "Trip Purpose x Primary Mode (Row)",
  col_var_label    = "Trip Purpose x Primary Mode (Col)",
  table_title      = "Table 4.5: Mode by Purpose",
  output_dir       = OUTPUT_DIR,
  row_order        = c("Education (Classes/Exam)", "Work / Job", "Personal Business"),
  col_order        = c("Public Bus", "MRT (Metro Rail)", "Personal Motorcycle", "Ridesharing (Uber/Pathao)"),
  use_monte_carlo_ffh         = TRUE,
  use_monte_carlo_permutation = FALSE,
  n_replications   = 99999,
  seed             = 42
)

cat("\n", rep("=", 60), "\n")
cat(paste0("ANALYSIS 04 RESULTS -- Trip Purpose x Primary Mode\n"))
cat(rep("=", 60), "\n")
cat(sprintf("  Sample size (N)      : %d\n", results$n_total))
cat(sprintf("  Chi-square           : chi2(%d) = %.4f\n", results$degrees_of_freedom, results$chi2_statistic))
cat(sprintf("  P-value              : %.6f\n", results$p_value))
cat(sprintf("  Cramer V             : %.4f (%s)\n", results$cramers_v, results$effect_size_label))
cat(sprintf("  Decision: %s\n", results$decision))
cat(rep("=", 60), "\n")
cat(sprintf("Outputs saved to: %s\n", OUTPUT_DIR))
