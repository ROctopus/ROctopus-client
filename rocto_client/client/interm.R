'''R script linking the client worker to roctoRun in R package.'''

library(rocto)

args <- commandArgs(trailingOnly = TRUE)
print(args)
roctoRun(args[1], args[2], args[3])
