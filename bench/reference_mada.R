# Usage: Rscript bench/reference_mada.R results/full/corpus.csv results/full/mada.jsonl
# Reference fits with mada (reitsma, which calls mvmeta's mvmeta.fit) for every dataset in the corpus:
#   method in reml / ml / fixed / mm / vc  x  correction.control in all / single / none (correction 0.5),
#   plus bivariate meta-regressions on smoking: ~ type, ~ population, ~ type + population (all methods).
# A fit mada refuses (e.g. correction "none" with a zero cell) is recorded with its error message.
# Per fit: coefficients, vcov, Psi, logLik (mada's Jacobian-adjusted value), AIC, BIC, convergence; for
# intercept-only random-effects fits also summary sensitivity / FPR with 95% CIs, the random-effects
# correlation, the Rutter-Gatsonis (HSROC) parameters, AUC and partial AUC (Rutter-Gatsonis and naive
# SROC), SROC values on a grid, and the 95% confidence and prediction regions (100 points each;
# prediction region = ellipse(Psi + vcov), as plot.reitsma(predict = TRUE)). Per dataset and correction
# rule: the Moses-Littenberg regression of mslSROC(). One JSON object per dataset per line, numbers with
# 17 significant digits. The same grid as allmeta's hub/shared/tests/_dta_parity_gen.R.
suppressMessages(library(mada))
args <- commandArgs(trailingOnly = TRUE)
corpus <- read.csv(args[1], stringsAsFactors = FALSE, colClasses = c(type = "character", population = "character"))
out <- args[2]

num <- function(x) ifelse(is.finite(x), formatC(x, digits = 17, format = "g"), "null")
vec <- function(x) paste0("[", paste(num(as.numeric(x)), collapse = ","), "]")
str <- function(s) paste0('"', gsub('["\\\\\n\r\t]', " ", s), '"')
obj <- function(...) { a <- list(...); a <- a[!vapply(a, is.null, NA)]; paste0("{", paste(paste0('"', names(a), '":', unlist(a)), collapse = ","), "}") }
tryq <- function(e) { r <- try(suppressWarnings(e), silent = TRUE); if (inherits(r, "try-error")) NULL else r }
FPRGRID <- c(0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.99)

fitone <- function(d, method, cc, formula = NULL) {
  head <- list(method = str(method), correction = str(cc), formula = if (is.null(formula)) NULL else str(deparse(formula)))
  args <- list(data = d, method = method, correction.control = cc)
  if (!is.null(formula)) args$formula <- formula
  f <- try(suppressWarnings(do.call(reitsma, args)), silent = TRUE)
  if (inherits(f, "try-error") || any(!is.finite(as.numeric(coef(f))))) {
    msg <- if (inherits(f, "try-error")) as.character(f) else "non-finite estimates"
    return(do.call(obj, c(head, list(ok = "false", error = str(substr(msg, 1, 200))))))
  }
  ll <- as.numeric(f$logLik)
  res <- list(ok = "true", p = num(nrow(f$coefficients)),
    coef = vec(f$coefficients), vcov = vec(vcov(f)), Psi = if (is.null(f$Psi)) NULL else vec(f$Psi),
    logLik = num(ll), df = num(attr(f$logLik, "df")),
    AIC = if (is.finite(ll)) num(AIC(f)) else NULL, BIC = if (is.finite(ll)) num(BIC(f)) else NULL,
    converged = if (is.null(f$converged)) NULL else tolower(as.character(f$converged)))
  if (is.null(formula) && !is.null(f$Psi)) {
    s <- summary(f); tf <- s$coefficients
    res$summary <- obj(sens = vec(tf["sensitivity", c(1, 5, 6)]), fpr = vec(tf["false pos. rate", c(1, 5, 6)]),
                       corRandom = num(s$corRandom[1, 2]))
    h <- mada:::calc_hsroc_coef(f)
    res$hsroc <- obj(Theta = num(h$Theta), Lambda = num(h$Lambda), beta = num(h$beta),
                     sigma2theta = num(h$sigma2theta), sigma2alpha = num(h$sigma2alpha))
    a1 <- tryq(AUC(f, sroc.type = "ruttergatsonis")); a2 <- tryq(AUC(f, sroc.type = "naive"))
    res$auc <- obj(rg = if (is.null(a1)) NULL else vec(c(a1$AUC, a1$pAUC)), naive = if (is.null(a2)) NULL else vec(c(a2$AUC, a2$pAUC)))
    res$sroc <- obj(fpr = vec(FPRGRID), rg = vec(sroc(f, fpr = FPRGRID, type = "ruttergatsonis")[, 2]),
                    naive = vec(sroc(f, fpr = FPRGRID, type = "naive")[, 2]))
    mu <- f$coefficients["(Intercept)", ]
    ce <- ROCellipse(f, add = FALSE)$ROCellipse
    pe <- ellipse::ellipse(f$Psi + vcov(f), centre = mu, level = 0.95)
    res$conf <- obj(fpr = vec(ce[, 1]), sens = vec(ce[, 2]))
    res$pred <- obj(fpr = vec(plogis(pe[, 2])), sens = vec(plogis(pe[, 1])))
  }
  do.call(obj, c(head, res))
}

METHODS <- c("reml", "ml", "fixed", "mm", "vc")
CC <- c("all", "single", "none")
REG <- list(smoking = c("type", "population", "type + population"))
pdf(NULL)  # mslSROC draws; keep the run free of Rplots.pdf
lines <- character()
for (dn in unique(corpus$dataset)) {
  d <- corpus[corpus$dataset == dn, c("TP", "FN", "FP", "TN", "type", "population")]
  rownames(d) <- NULL
  fits <- character()
  for (cc in CC) for (me in METHODS) fits <- c(fits, fitone(d, me, cc))
  for (rhs in REG[[dn]]) for (me in METHODS) fits <- c(fits, fitone(d, me, "all", as.formula(paste("cbind(tsens, tfpr) ~", rhs))))
  ms <- vapply(CC, function(cc) {
    m <- tryq(mslSROC(d, correction.control = cc, extrapolate = TRUE))
    if (is.null(m) || !all(is.finite(c(m$A1, m$B1)))) return(obj(correction = str(cc), ok = "false"))
    obj(correction = str(cc), ok = "true", A1 = num(m$A1), B1 = num(m$B1))
  }, "")
  lines <- c(lines, sprintf('{"dataset":"%s","k":%d,"fits":[%s],"moses":[%s]}', dn, nrow(d), paste(fits, collapse = ","), paste(ms, collapse = ",")))
}
dev.off()
writeLines(lines, out, useBytes = TRUE)
cat(sprintf("mada %s (mvmeta %s, ellipse %s), R %s: %d datasets, %d configurations -> %s\n", packageVersion("mada"), packageVersion("mvmeta"),
            packageVersion("ellipse"), getRversion(), length(lines), sum(lengths(regmatches(lines, gregexpr('"method":', lines)))), out))
