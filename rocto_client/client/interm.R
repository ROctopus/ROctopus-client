# R script linking worker to roctoRun in R package.

library(rocto)

args <- commandArgs(trailingOnly = TRUE)
roctoRun(args[1], args[2], args[3])
