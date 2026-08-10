# ==============================================================================
# analysis.R — In-Vehicle Time Statistical Pipeline Analysis
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
message("ANALYSIS (R): In-Vehicle Time")
message(rep("=", 60))

df <- load_dataset_r(DATA_PATH)
kw_res <- kruskal_wallis_manual_r(df, "What is yout total "In-Vehicle Time" Time spent inside the main bus/train/car in Minutes?", "What is your PRIMARY mode of transport?")
print(kw_res)
