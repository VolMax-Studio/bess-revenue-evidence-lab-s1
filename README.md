# Evidence Lab #002: European BESS Revenue Benchmarks (August 2026)

[![Reproducibility](https://img.shields.io/badge/reproduction-100%25%20pass-10b981.svg)](reproduce.sh)
[![Integrity](https://img.shields.io/badge/SHA--256-pinned%20%26%20verified-38bdf8.svg)](data/MANIFEST.sha256)
[![Status](https://img.shields.io/badge/verdict-METHODOLOGY__MISMATCH-f59e0b.svg)](evidence/receipt_de_comparability.json)

An inspectable **Evidence Lab primitive** evaluating public European Battery Energy Storage System (BESS) revenue benchmarks for August 2026 published by Mark Böhmer (Boehmer Advisory UG) via [bess-index.com](https://www.bess-index.com).

## Core Epistemological Principle

> **Start with what is indisputable. Then expose what is consequential.**

---

## Source Attribution

Benchmark data used in this case originates from [bess-index.com](https://www.bess-index.com) / Boehmer Advisory and the respective benchmark providers. VolMax Studio does not claim ownership of the underlying benchmark data. This Evidence Lab case independently verifies selected published claims and examines comparability of declared assumptions.

---


## 1. The Two-Tier Architecture

### Tier 1: Indisputable Arithmetic (Spread Verification)
Evaluates deterministic spread arithmetic $\text{Spread} = \max(B) - \min(B)$ directly against the byte-pinned live web application bundle:

- **Germany (DE):** $303 - 187 = 116\text{ kEUR/MW/year}$ $\to$ **`VERIFIED`** (`suena` vs `Regelleistung Online`)
- **Belgium (BE):** $229 - 145 = 84\text{ kEUR/MW/year}$ $\to$ **`VERIFIED`** (`Re-Twin` vs `Aurora`)
- **Spain (ES):** $507 - 287 = 220\text{ kEUR/MW/year}$ $\to$ **`VERIFIED`** (`Clean Horizon` vs `Modo Energy`)
- **Negative Control:** Synthetic counter-claim ($50\text{ kEUR}$) $\to$ **`NOT_VERIFIED`** (proves verifier is not a hardcoded green checkmark)

### Tier 2: Consequential Depth (Comparability Adjudication)
Adjudicates whether the highest and lowest benchmarks represent equivalent economic assets under identical operational constraints:

| Operational Dimension | Top Provider (`suena`) | Bottom Provider (`Regelleistung`) | Match Status | Epistemological Finding |
|---|---|---|---|---|
| **Degradation Model** | `Managed` | `Not applied` | **`MISMATCH`** | Explicit operational disparity; different degradation treatment materially affects the economic interpretation of cycling revenues. |

| **Revenue Stack** | `Wholesale; Balancing` | `Wholesale; Balancing / aFRR` | **`DECLARATION_DIFFERENCE`** | Published wording differs; semantic incompatibility is not inferred from wording alone. |
| **Dispatch Foresight** | `Modelled / realised optimiser dispatch` | `Modelled dispatch on market prices` | **`DECLARATION_DIFFERENCE`** | Published wording differs; different descriptive phrasing. |
| **Cycle Limit Applied** | `n/a` | `2 cycles/day` | **`UNDISCLOSED`** | `suena` does not disclose cycle capping parameter. |
| **Cycling Intensity** | `n/a` | `n/a` | **`UNDISCLOSED`** | Latent operational parameter undisclosed by both providers. |
| **Asset Availability** | `n/a` | `n/a` | **`UNDISCLOSED`** | Operational availability undisclosed. |
| **Modelling Basis** | `Published monthly benchmark series` | `Published monthly benchmark series` | **`MATCH`** | Identical declared category. |

**Tier 2 Verdict:** **`METHODOLOGY_MISMATCH`**  
> *At least one explicit methodology mismatch is documented: Degradation Model. There are also 2 declaration differences and 3 undisclosed dimensions. Direct comparability of the two benchmark values is therefore not established; no causal decomposition of the 116 kEUR spread is claimed.*

---

## 2. Pinned Provenance & Manifest

All benchmark values and provider methodology attributes are pinned from the live production JavaScript bundle of `bess-index.com` (`assets/routes-6Gnn6JDp.js`) with zero reconstruction from social media posts:

- `data/raw/source_snapshot/bess_index_routes.js` (`a6ff4041...`)
- `data/raw/source_snapshot/bess_index_page.html` (`094c6487...`)
- `data/raw/bess_benchmarks_august_2026.csv` (`8de77319...`)
- `data/raw/bess_providers_methodology.json` (`c8631418...`)

Integrity is validated via `data/MANIFEST.sha256`.

---

## 3. Public Evidence Package & Verification

Independently reproduce the Evidence Lab calculations from the packaged extracted dataset:

```bash
# Download and verify standalone package
curl -O https://bess-revenue-evidence-lab-s1.vercel.app/evidence-package-august-2026.zip
unzip evidence-package-august-2026.zip
./reproduce.sh
```

### Audit Custody Disclosure
Full raw web source snapshots are retained in private audit custody pending redistribution clearance. Public source URLs, extracted evidence used by the verifier, deterministic verification code, and cryptographic hashes are available for inspection.



---

## 4. Web Inspector

The repository is a zero-dependency static package. To preview locally:

```bash
python3 -m http.server 8085
# Open http://localhost:8085
```

Deployable to Vercel, Cloudflare Pages, or any static host out of the box.
