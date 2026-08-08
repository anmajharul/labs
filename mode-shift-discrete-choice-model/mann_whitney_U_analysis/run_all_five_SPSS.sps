
* ============================================================
* Table 4.4: all five Mann-Whitney U comparisons.
* Gender: 1=Male, 2=Female.
* ============================================================.

NPAR TESTS
  /MANN-WHITNEY = security_harassment reliability road_accidents
                  comfort crowding BY Gender(1 2)
  /MISSING ANALYSIS.

MEANS TABLES=security_harassment reliability road_accidents
             comfort crowding BY Gender
  /CELLS MEAN MEDIAN COUNT.
