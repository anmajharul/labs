# ==============================================================================
# analysis.R — Access Time (min) Kruskal-Wallis H Test
# ==============================================================================
# Author : Majharul Islam (BUBT)
# Date   : 2026-08-11
# ==============================================================================

SCRIPT_DIR <- tryCatch(
  dirname(rstudioapi::getSourceEditorContext()$path),
  error = function(e) getwd()
)
REPO_ROOT  <- dirname(SCRIPT_DIR)
DATA_PATH  <- file.path(REPO_ROOT, "data", "raw", "Mode_shift_bubt.xlsx")
OUTPUT_DIR <- SCRIPT_DIR

source(file.path(REPO_ROOT, "kruskal_wallis_utils.R"))

message(rep("=", 60))
message("ANALYSIS (R): Access Time (min)")
message(rep("=", 60))

raw_df <- readxl::read_excel(DATA_PATH)
prep   <- prepare_analysis_dataframe(raw_df)
df     <- prep$df

kw_res <- kruskal_wallis_manual_r(df, "access_time", "primary_mode")
es_res <- kw_effect_size_r(kw_res$H_corrected, kw_res$N, kw_res$df + 1)
dunn   <- dunn_bonferroni_r(df, "access_time", "primary_mode")

cat("
", rep("=", 60), "
")
cat("KRUSKAL-WALLIS RESULTS -- Access Time (min)
")
cat(rep("=", 60), "
")
cat(sprintf("  Sample size (N)     : %d
", kw_res$N))
cat(sprintf("  H (uncorrected)     : %.4f
", kw_res$H_uncorrected))
cat(sprintf("  Tie Correction (C)  : %.6f
", kw_res$tie_correction))
cat(sprintf("  H (corrected)       : %.4f (df = %d, p = %.6f)
", kw_res$H_corrected, kw_res$df, kw_res$p_value))
cat(sprintf("  Effect Size (eta2)  : %.4f (%s)
", es_res$eta2, es_res$interpretation))
cat(rep("=", 60), "
")

write.csv(dunn, file.path(OUTPUT_DIR, "dunn_posthoc_r.csv"), row.names = FALSE)
