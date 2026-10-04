# Usage: Rscript bench/build_corpus.R results/full/corpus.csv
# DTA validation corpus: the six diagnostic-accuracy datasets shipped with the R package mada, in one
# long format: dataset, study, TP, FN, FP, TN, type, population (type and population: smoking, IAQ and
# SAQ only; empty elsewhere). Sources as documented in mada's ?`mada-data`.
suppressMessages(library(mada))
args <- commandArgs(trailingOnly = TRUE)
out <- if (length(args)) args[1] else "data/corpus.csv"
DS <- c("AuditC", "Dementia", "IAQ", "SAQ", "skin_tests", "smoking")
L <- list()
for (d in DS) {
  e <- new.env(); data(list = d, package = "mada", envir = e); x <- as.data.frame(get(d, envir = e))
  L[[d]] <- data.frame(dataset = d, study = seq_len(nrow(x)), TP = x$TP, FN = x$FN, FP = x$FP, TN = x$TN,
                       type = if (is.null(x$type)) "" else as.character(x$type),
                       population = if (is.null(x$population)) "" else as.character(x$population), stringsAsFactors = FALSE)
}
corpus <- do.call(rbind, L)
zero <- with(corpus, TP == 0 | FN == 0 | FP == 0 | TN == 0)
dir.create(dirname(out), showWarnings = FALSE, recursive = TRUE)
for (v in c("TP", "FN", "FP", "TN")) corpus[[v]] <- sprintf("%.17g", corpus[[v]])  # integer counts; exact text on every platform
write.csv(corpus, out, row.names = FALSE, fileEncoding = "UTF-8", quote = c(1, 7, 8))
cat(sprintf("corpus: %d datasets, %d studies, %d with a zero cell (mada %s)\n", length(DS), nrow(corpus), sum(zero), packageVersion("mada")))
