# ============================================================
# kw_utils.R
# Core utility functions for Kruskal-Wallis analysis pipeline
#
# Author  : Majharul Islam (BUBT)
# Date    : 2026-08-11
# Chapter : 4 — Kruskal-Wallis H Analysis
# ============================================================

library(readxl)

# ── Column detection ──────────────────────────────────────────────────────────
RAW_COLUMN_FRAGMENTS <- list(
  primary_mode    = "PRIMARY mode of transport",
  one_way_cost    = "TOTAL One-Way Cost",
  access_time     = "Access Time",
  in_vehicle_time = "In-Vehicle Time"
)

EXPECTED_MODES <- c(
  "Public Bus",
  "MRT (Metro Rail)",
  "Personal Motorcycle",
  "Ridesharing (Uber/Pathao)"
)

VARIABLE_LABELS <- c(
  one_way_cost      = "One-Way Cost (BDT)",
  access_time       = "Access Time (min)",
  in_vehicle_time   = "In-Vehicle Time (min)",
  total_travel_time = "Total Travel Time (min)"
)

# Chapter 4 reported values (validation only, never used in calculation)
CHAPTER4_H <- c(
  one_way_cost      = 97.911,
  access_time       = 169.538,
  in_vehicle_time   = 110.929,
  total_travel_time = 73.325
)

# ── Data loading ──────────────────────────────────────────────────────────────
load_raw_data <- function(data_path) {
  if (!file.exists(data_path)) stop(paste("Dataset not found:", data_path))
  df <- read_excel(data_path)
  names(df) <- trimws(names(df))
  message(sprintf("Loaded %d rows x %d columns from %s", nrow(df), ncol(df), data_path))
  df
}

detect_column <- function(df, short_name) {
  fragment <- RAW_COLUMN_FRAGMENTS[[short_name]]
  matches  <- grep(fragment, names(df), ignore.case = TRUE, value = TRUE)
  if (length(matches) == 0) stop(paste("Cannot find column for:", short_name))
  matches[1]
}

# ── Data preparation ──────────────────────────────────────────────────────────
prepare_analysis_dataframe <- function(df) {
  mode_col  <- detect_column(df, "primary_mode")
  cost_col  <- detect_column(df, "one_way_cost")
  at_col    <- detect_column(df, "access_time")
  ivt_col   <- detect_column(df, "in_vehicle_time")

  work <- data.frame(
    primary_mode    = trimws(as.character(df[[mode_col]])),
    one_way_cost    = suppressWarnings(as.numeric(df[[cost_col]])),
    access_time     = suppressWarnings(as.numeric(df[[at_col]])),
    in_vehicle_time = suppressWarnings(as.numeric(df[[ivt_col]])),
    stringsAsFactors = FALSE
  )

  original_n <- nrow(work)
  exclusions <- character(0)

  # Remove invalid modes
  bad_mode <- !(work$primary_mode %in% EXPECTED_MODES) | is.na(work$primary_mode)
  if (sum(bad_mode) > 0) {
    exclusions <- c(exclusions, paste("Invalid mode rows excluded:", sum(bad_mode)))
    work <- work[!bad_mode, ]
  }

  # Remove zero/negative cost
  bad_cost <- is.na(work$one_way_cost) | work$one_way_cost <= 0
  if (sum(bad_cost) > 0) {
    exclusions <- c(exclusions, paste("Zero/negative cost rows excluded:", sum(bad_cost)))
    work <- work[!bad_cost, ]
  }

  # Remove zero/negative access time
  bad_at <- is.na(work$access_time) | work$access_time <= 0
  if (sum(bad_at) > 0) {
    exclusions <- c(exclusions, paste("Zero/negative access time excluded:", sum(bad_at)))
    work <- work[!bad_at, ]
  }

  # Remove zero/negative in-vehicle time
  bad_ivt <- is.na(work$in_vehicle_time) | work$in_vehicle_time <= 0
  if (sum(bad_ivt) > 0) {
    exclusions <- c(exclusions, paste("Zero/negative IVT excluded:", sum(bad_ivt)))
    work <- work[!bad_ivt, ]
  }

  # Derive Total Travel Time
  work$total_travel_time <- work$access_time + work$in_vehicle_time

  message(sprintf("Analysis N = %d (of %d, excluded %d)",
                  nrow(work), original_n, original_n - nrow(work)))
  list(df = work, exclusions = exclusions)
}

# ── Manual rank computation (average ties) ────────────────────────────────────
compute_ranks_manual <- function(values) {
  # R's rank() with ties.method="average" does the same thing.
  # We replicate it manually for transparency.
  n     <- length(values)
  order <- order(values)
  ranks <- numeric(n)
  i     <- 1
  while (i <= n) {
    j <- i
    while (j <= n && values[order[j]] == values[order[i]]) j <- j + 1
    avg_rank <- (i + j - 1) / 2
    ranks[order[i:(j-1)]] <- avg_rank
    i <- j
  }
  ranks
}

# ── Tie correction ────────────────────────────────────────────────────────────
compute_tie_correction <- function(values) {
  N <- length(values)
  counts <- table(values)
  t3_t <- as.numeric(counts)^3 - as.numeric(counts)
  sum_t3_t <- sum(t3_t)
  denom <- N^3 - N
  C <- if (denom > 0) 1 - sum_t3_t / denom else 1.0
  tie_tbl <- data.frame(
    Value      = as.numeric(names(counts)),
    Frequency  = as.numeric(counts),
    t3_minus_t = t3_t,
    stringsAsFactors = FALSE
  )
  tie_tbl <- tie_tbl[tie_tbl$Frequency > 1, ]
  list(C = C, sum_t3_t = sum_t3_t, N3_minus_N = denom, tie_table = tie_tbl)
}

# ── Manual KW H statistic ─────────────────────────────────────────────────────
kruskal_wallis_manual_r <- function(df, variable, mode_col = "primary_mode") {
  vals   <- df[[variable]]
  modes  <- df[[mode_col]]
  all_v  <- as.numeric(vals)
  N      <- length(all_v)

  ranks  <- compute_ranks_manual(all_v)

  # Group stats
  group_modes <- sort(unique(modes))
  group_stats <- lapply(group_modes, function(m) {
    idx  <- which(modes == m)
    n_i  <- length(idx)
    R_i  <- sum(ranks[idx])
    list(mode = m, n = n_i, rank_sum = R_i, mean_rank = R_i / n_i)
  })
  names(group_stats) <- group_modes

  # H uncorrected
  sigma <- sum(sapply(group_stats, function(g) g$rank_sum^2 / g$n))
  H_unc <- (12 / (N * (N + 1))) * sigma - 3 * (N + 1)

  # Tie correction
  tc    <- compute_tie_correction(all_v)
  C     <- tc$C
  H_cor <- H_unc / C

  # p-value
  df_kw <- length(group_modes) - 1
  p_val <- pchisq(H_cor, df = df_kw, lower.tail = FALSE)

  list(
    variable      = variable,
    N             = N,
    group_stats   = group_stats,
    H_uncorrected = H_unc,
    tie_correction = C,
    sum_t3_t      = tc$sum_t3_t,
    N3_minus_N    = tc$N3_minus_N,
    H_corrected   = H_cor,
    df            = df_kw,
    p_value       = p_val,
    tie_table     = tc$tie_table
  )
}

# ── Effect size ───────────────────────────────────────────────────────────────
kw_effect_size_r <- function(H, N, k) {
  eta2 <- (H - k + 1) / (N - k)
  interpretation <- if (eta2 >= 0.14) {
    "Large (eta2 >= 0.14; Tomczak & Tomczak, 2014)"
  } else if (eta2 >= 0.06) {
    "Medium (0.06 <= eta2 < 0.14; Tomczak & Tomczak, 2014)"
  } else if (eta2 >= 0.01) {
    "Small (0.01 <= eta2 < 0.06; Tomczak & Tomczak, 2014)"
  } else {
    "Negligible (eta2 < 0.01; Tomczak & Tomczak, 2014)"
  }
  list(eta2 = eta2, interpretation = interpretation,
       citation = "Tomczak & Tomczak (2014). Trends in Sport Sciences, 1(21), 19-25.")
}

# ── Dunn post-hoc (manual Bonferroni) ────────────────────────────────────────
dunn_bonferroni_r <- function(df, variable, mode_col = "primary_mode") {
  vals   <- as.numeric(df[[variable]])
  modes  <- df[[mode_col]]
  N      <- length(vals)
  ranks  <- compute_ranks_manual(vals)

  group_modes <- sort(unique(modes))
  k <- length(group_modes)

  group_mr <- sapply(group_modes, function(m) mean(ranks[modes == m]))
  group_ns <- sapply(group_modes, function(m) sum(modes == m))

  # Tie term
  counts   <- table(vals)
  sum_t3_t <- sum(as.numeric(counts)^3 - as.numeric(counts))
  tie_term <- sum_t3_t / (12 * (N - 1))
  base_var <- N * (N + 1) / 12

  pairs <- combn(group_modes, 2, simplify = FALSE)
  m     <- length(pairs)
  bonf  <- 0.05 / m

  result <- lapply(pairs, function(p) {
    A <- p[1]; B <- p[2]
    n_A <- group_ns[A]; n_B <- group_ns[B]
    inv <- 1/n_A + 1/n_B
    SE  <- sqrt((base_var - tie_term) * inv)
    z   <- (group_mr[A] - group_mr[B]) / SE
    p_raw <- 2 * pnorm(-abs(z))
    p_adj <- min(p_raw * m, 1.0)
    data.frame(
      Comparison              = paste(A, "vs", B),
      Group_A                 = A,
      Group_B                 = B,
      Mean_Rank_A             = round(group_mr[A], 3),
      Mean_Rank_B             = round(group_mr[B], 3),
      z_statistic             = round(z, 4),
      Raw_p                   = round(p_raw, 4),
      Bonferroni_p            = round(p_adj, 4),
      Bonferroni_threshold    = round(bonf, 4),
      Significant_Bonferroni  = if (p_adj < 0.05) "Yes" else "No",
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, result)
}

message("kw_utils.R loaded successfully.")
