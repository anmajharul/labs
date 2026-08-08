
DATA_PATH <- "data/chapter4_raw.csv"
GENDER_COL <- "Gender"

OUTCOMES <- c(
  Security_Harassment = "security_harassment",
  Reliability = "reliability",
  Road_Accidents = "road_accidents",
  Comfort = "comfort",
  Crowding = "crowding"
)

dat <- read.csv(DATA_PATH, stringsAsFactors = FALSE)
results <- data.frame()

for (label in names(OUTCOMES)) {
  col <- OUTCOMES[[label]]
  d <- dat[complete.cases(dat[, c(GENDER_COL, col)]),
           c(GENDER_COL, col)]

  male <- as.numeric(d[d[[GENDER_COL]] == 1, col])
  female <- as.numeric(d[d[[GENDER_COL]] == 2, col])

  wt <- wilcox.test(male, female, alternative="two.sided",
                    exact=FALSE, correct=TRUE)

  W1 <- as.numeric(wt$statistic)
  n1 <- length(male)
  n2 <- length(female)
  U1 <- W1 - n1*(n1+1)/2
  U2 <- n1*n2 - U1

  results <- rbind(results, data.frame(
    Outcome=label,
    Male_N=n1,
    Female_N=n2,
    Male_Mean=mean(male),
    Male_Median=median(male),
    Female_Mean=mean(female),
    Female_Median=median(female),
    U1_Male=U1,
    U2_Female=U2,
    U_reported=min(U1,U2),
    p_value=wt$p.value,
    Significant_alpha_0.05=wt$p.value < 0.05
  ))
}

print(results)
write.csv(results, "outputs/mann_whitney_table4_4_R.csv", row.names=FALSE)
