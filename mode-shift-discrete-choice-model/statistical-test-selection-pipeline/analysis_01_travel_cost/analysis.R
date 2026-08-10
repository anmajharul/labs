# ==============================================================================
# analysis.R — Travel Cost Statistical Pipeline Analysis
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

source(file.path(REPO_ROOT, "pipeline_utils.R"))

message(rep("=", 60))
message("ANALYSIS (R): Travel Cost")
message(rep("=", 60))

df <- load_dataset_r(DATA_PATH)
kw_res <- kruskal_wallis_manual_r(df, "What is the TOTAL One-Way Cost of this trip?", "What is your PRIMARY mode of transport?")
print(kw_res)
