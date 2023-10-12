library(googlesheets4)
library(tidyverse)
sheet_url <- "https://docs.google.com/spreadsheets/d/1UmrM2zPuqpjiYYvR1XnglQnoP_QI2tyDMA5Eaz99Q1w/edit#gid=0"
my_sheet <- gs4_get(sheet_url)
sheet_data <- read_sheet(my_sheet, range = "A1:O1682")
write.csv(sheet_data, "pitstop_time_2018-2020", row.names = FALSE)

pitstop_time <- read.csv("pitstop_time_2018-2020")

# Dealing missing values
cleaned_pitstop <- pitstop_time %>%
  # Replace missing values in numeric columns with mean
  mutate_if(is.numeric, ~ifelse(is.na(.), mean(., na.rm = TRUE), .)) %>%
  # Replace missing values in character columns with "Unknown"
  mutate_if(is.character, ~ifelse(is.na(.), "Unknown", .))

cleaned_pitstop <- cleaned_pitstop %>%
  select(SEASON, DATE, GRAND_PRIX, PIT_DUR, DRIVER_NUM, TEAM_SEASON, PIT_IRREGULAR)

write.csv(cleaned_pitstop, "cleaned_pitstop_time_2018-2020", row.names = FALSE)


