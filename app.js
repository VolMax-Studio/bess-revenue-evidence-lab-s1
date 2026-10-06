// Evidence Lab Case #002 Client Logic
// Pinned datasets & calculations embedded for zero-dependency offline & static execution

const CASES = {
  DE: {
    marketCode: "DE",
    marketName: "Germany",
    targetPeriod: "August 2026",
    claimId: "CLAIM-EVID-002-DE-SPREAD",
    headlineFormula: "303 - 187 = 116",
    maxVal: 303,
    minVal: 187,
    spreadVal: 116,
    unit: "kEUR/MW/year",
    verdict: "VERIFIED",
    isNegativeCtrl: false,
    statement: "Highest benchmark is 303 kEUR/MW/year (suena) and lowest is 187 kEUR/MW/year (Regelleistung Online), creating a monthly spread of 116 kEUR/MW/year.",
    maxProvider: {
      id: "suena",
      name: "suena — Optimiser Benchmark",
      short: "suena",
      exact: 303.6,
      integer: 303,
      color: "#ea580c"
    },
    minProvider: {
      id: "regelleistung",
      name: "Regelleistung Online — Benchmark",
      short: "Regelleistung",
      exact: 187.232,
      integer: 187,
      color: "#b45309"
    },
    receiptHash: "9757659cb030a5ca66352c349cb37667da96df6ef52a78ec4f31cfa0aa3aa8cb",
    comparability: {
      providerA: "suena",
      providerB: "Regelleistung Online",
      spreadKeur: "116.368",
      verdict: "METHODOLOGY_MISMATCH",
      rationale: "At least one explicit methodology mismatch is documented: degradation treatment is Managed vs Not applied. Revenue-stack and foresight declarations use different wording, while three additional dimensions are undisclosed. Direct comparability of the two benchmark values is therefore not established; no causal decomposition of the 116 kEUR spread is claimed.",
      dimensions: [
        {
          name: "Revenue Stack Included",
          a: "Wholesale trading arbitrage; Balancing",
          b: "Wholesale trading arbitrage; Balancing / aFRR",
          status: "DECLARATION_DIFFERENCE",
          note: "Published wording differs; semantic incompatibility is not inferred from wording alone."
        },
        {
          name: "Dispatch Foresight Assumption",
          a: "Modelled / realised optimiser dispatch",
          b: "Modelled dispatch on market prices",
          status: "DECLARATION_DIFFERENCE",
          note: "Published wording differs; semantic incompatibility is not inferred from wording alone."
        },
        {
          name: "Degradation Model",
          a: "Managed",
          b: "Not applied",
          status: "MISMATCH",
          note: "Explicit declared mismatch: Managed vs Not applied. This is sufficient to block a direct comparability finding."
        },
        {
          name: "Cycle Limit Applied",
          a: "n/a (Undisclosed)",
          b: "2 cycles/day",
          status: "UNDISCLOSED",
          note: "suena does not disclose cycle capping."
        },
        {
          name: "Cycling Intensity",
          a: "n/a (Undisclosed)",
          b: "n/a (Undisclosed)",
          status: "UNDISCLOSED",
          note: "Neither provider discloses actual cycling throughput."
        },
        {
          name: "Asset Availability",
          a: "n/a (Undisclosed)",
          b: "n/a (Undisclosed)",
          status: "UNDISCLOSED",
          note: "Neither provider discloses an availability value in the pinned source."
        },
        {
          name: "Empirical / Modelling Basis",
          a: "Published monthly benchmark series",
          b: "Published monthly benchmark series",
          status: "MATCH",
          note: "Both published as regular monthly industry benchmarks."
        }
      ]
    }
  },
  BE: {
    marketCode: "BE",
    marketName: "Belgium",
    targetPeriod: "August 2026",
    claimId: "CLAIM-EVID-002-BE-SPREAD",
    headlineFormula: "229 - 145 = 84",
    maxVal: 229,
    minVal: 145,
    spreadVal: 84,
    unit: "kEUR/MW/year",
    verdict: "VERIFIED",
    isNegativeCtrl: false,
    statement: "Highest benchmark is 229 kEUR/MW/year (Re-Twin) and lowest is 145 kEUR/MW/year (Aurora), creating a monthly spread of 84 kEUR/MW/year.",
    maxProvider: {
      id: "retwin",
      name: "Re-Twin — Digital Twin Benchmark",
      short: "Re-Twin",
      exact: 229.91,
      integer: 229,
      color: "#0891b2"
    },
    minProvider: {
      id: "aurora",
      name: "Aurora Energy Research — Central",
      short: "Aurora",
      exact: 145.32,
      integer: 145,
      color: "#1d4ed8"
    },
    receiptHash: "ee60806fcd0bebcf875e521b4b4952be3b5b969ad4eeadb6bd6da2b4cf5d12e2",
    comparability: {
      providerA: "Re-Twin",
      providerB: "Aurora Energy Research",
      spreadKeur: "84.590",
      verdict: "METHODOLOGY_MISMATCH",
      rationale: "Aurora includes Capacity Market floor contracts with battery augmentation CAPEX and 1.5 cycles/day limit; Re-Twin models a digital twin with 2 cycles/day and no capacity market inclusion.",
      dimensions: [
        {
          name: "Revenue Stack Included",
          a: "Wholesale trading arbitrage; Ancillary services",
          b: "Wholesale trading arbitrage; Ancillary services; Capacity market",
          status: "MISMATCH",
          note: "Aurora includes CRM remuneration contracts."
        },
        {
          name: "Dispatch Foresight Assumption",
          a: "Modelled dispatch (digital twin)",
          b: "Optimised dispatch with imperfect-foresight haircut",
          status: "MISMATCH",
          note: "Haircut model vs physical digital twin."
        },
        {
          name: "Degradation Model",
          a: "Modelled",
          b: "Modelled, with augmentation capex",
          status: "MISMATCH",
          note: "Aurora includes cell augmentation capital expenditure."
        },
        {
          name: "Cycle Limit Applied",
          a: "2 cycles/day",
          b: "n/a (1.5 cycles declared cycling)",
          status: "MISMATCH",
          note: "Divergent cycle operating limits."
        },
        {
          name: "Asset Availability",
          a: "n/a (Undisclosed)",
          b: "98%",
          status: "UNDISCLOSED",
          note: "Aurora models 98% availability; Re-Twin does not disclose."
        },
        {
          name: "Empirical / Modelling Basis",
          a: "Published monthly benchmark series",
          b: "Fundamental market model, hourly + intraday shaping",
          status: "MISMATCH",
          note: "Fundamental equilibrium vs benchmark index."
        }
      ]
    }
  },
  ES: {
    marketCode: "ES",
    marketName: "Spain",
    targetPeriod: "August 2026",
    claimId: "CLAIM-EVID-002-ES-SPREAD",
    headlineFormula: "507 - 287 = 220",
    maxVal: 507,
    minVal: 287,
    spreadVal: 220,
    unit: "kEUR/MW/year",
    verdict: "VERIFIED",
    isNegativeCtrl: false,
    statement: "Highest benchmark is 507 kEUR/MW/year (Clean Horizon) and lowest is 287 kEUR/MW/year (Modo Energy), creating a monthly spread of 220 kEUR/MW/year.",
    maxProvider: {
      id: "cleanhorizon",
      name: "Clean Horizon — Storage Index",
      short: "Clean Horizon",
      exact: 507.0,
      integer: 507,
      color: "#0f766e"
    },
    minProvider: {
      id: "modo",
      name: "Modo Energy — Benchmark (2h)",
      short: "Modo",
      exact: 287.887,
      integer: 287,
      color: "#0e7490"
    },
    receiptHash: "e920a5fa54a224e30007ef62527148d4b24f3385a716ba6686bea107bea2a8a7",
    comparability: {
      providerA: "Clean Horizon",
      providerB: "Modo Energy",
      spreadKeur: "219.113",
      verdict: "METHODOLOGY_MISMATCH",
      rationale: "Modo measures metered bottom-up fleet dispatch from real operational batteries under actual commercial constraints; Clean Horizon runs an algorithmic model with a theoretical efficiency factor.",
      dimensions: [
        {
          name: "Empirical / Modelling Basis",
          a: "Published monthly storage revenue index",
          b: "Bottom-up metering of operational fleet",
          status: "MISMATCH",
          note: "Real operational assets vs theoretical dispatch model."
        },
        {
          name: "Revenue Stack Included",
          a: "Wholesale trading arbitrage; Ancillary services",
          b: "Wholesale trading arbitrage; Balancing / BM; Frequency response",
          status: "MISMATCH",
          note: "Different balancing products and Spanish market boundaries."
        },
        {
          name: "Dispatch Foresight Assumption",
          a: "Modelled dispatch with efficiency factor",
          b: "Realised / imperfect foresight (actual asset dispatch)",
          status: "MISMATCH",
          note: "Actual realized operational execution vs model simulation."
        },
        {
          name: "Degradation Model",
          a: "Modelled",
          b: "Implicit in observed operation",
          status: "MISMATCH",
          note: "Real fleet wear vs algorithmic rule."
        },
        {
          name: "Asset Availability",
          a: "100%",
          b: "n/a (As-operated)",
          status: "MISMATCH",
          note: "Clean Horizon assumes perfect 100% availability."
        }
      ]
    }
  },
  CTRL_NEG: {
    marketCode: "DE",
    marketName: "Germany (Negative Control)",
    targetPeriod: "August 2026",
    claimId: "CLAIM-EVID-002-DE-CTRL-NEG",
    headlineFormula: "303 - 187 ≠ 50",
    maxVal: 303,
    minVal: 187,
    spreadVal: 50,
    unit: "kEUR/MW/year",
    verdict: "NOT_VERIFIED",
    isNegativeCtrl: true,
    statement: "Hypothetical counter-claim asserting German BESS benchmark spread is 50 kEUR/MW/year (expected to FAIL deterministic check).",
    maxProvider: {
      id: "suena",
      name: "suena — Optimiser Benchmark",
      short: "suena",
      exact: 303.6,
      integer: 303,
      color: "#ea580c"
    },
    minProvider: {
      id: "regelleistung",
      name: "Regelleistung Online — Benchmark",
      short: "Regelleistung",
      exact: 187.232,
      integer: 187,
      color: "#b45309"
    },
    receiptHash: "3c12f2f3e27899edba3b64dd59f2b82d2df9ae8d7cb24d7d6a0407e6575cb936",
    comparability: null
  }
};

const ALL_DE_BENCHMARKS = [
  { rank: 1, name: "suena — Optimiser Benchmark", short: "suena", valExact: 303.6, valInt: 303, foresight: "Modelled / realised optimiser dispatch", degradation: "Managed", basis: "Published monthly benchmark series" },
  { rank: 2, name: "LCP Delta — Storage Outlook", short: "LCP Delta", valExact: 244.0, valInt: 244, foresight: "Modelled dispatch, near-perfect foresight", degradation: "Modelled", basis: "Dispatch optimiser over modelled price curves" },
  { rank: 3, name: "Clean Horizon — Storage Index", short: "Clean Horizon", valExact: 233.0, valInt: 233, foresight: "Modelled dispatch with efficiency factor", degradation: "Modelled", basis: "Published monthly storage revenue index" },
  { rank: 4, name: "Re-Twin — Digital Twin Benchmark", short: "Re-Twin", valExact: 230.38, valInt: 230, foresight: "Modelled dispatch (digital twin)", degradation: "Modelled", basis: "Published monthly benchmark series" },
  { rank: 5, name: "Aurora Energy Research — Central", short: "Aurora", valExact: 220.2, valInt: 220, foresight: "Optimised dispatch with imperfect-foresight haircut", degradation: "Modelled, with augmentation capex", basis: "Fundamental market model, hourly + intraday shaping" },
  { rank: 6, name: "RWTH Aachen — Academic Model", short: "RWTH Aachen", valExact: 209.68, valInt: 209, foresight: "Perfect foresight linear programme", degradation: "Not modelled", basis: "Deterministic optimisation, university research" },
  { rank: 7, name: "enspired — Realised Trading", short: "enspired", valExact: 202.0, valInt: 202, foresight: "Live algorithmic trading (imperfect foresight)", degradation: "Managed via throughput budget", basis: "Realised optimiser results across managed portfolio" },
  { rank: 8, name: "Modo Energy — Benchmark (2h)", short: "Modo", valExact: 190.611, valInt: 190, foresight: "Realised / imperfect foresight (actual asset dispatch)", degradation: "Implicit in observed operation", basis: "Bottom-up metering of operational fleet" },
  { rank: 9, name: "Regelleistung Online — Benchmark", short: "Regelleistung", valExact: 187.232, valInt: 187, foresight: "Modelled dispatch on market prices", degradation: "Not applied", basis: "Published monthly benchmark series" }
];

let currentKey = "DE";

function renderCase(key) {
  currentKey = key;
  const c = CASES[key];

  // Update tabs
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.key === key);
  });

  // Level 1 Card
  const t1Card = document.getElementById("tier1-card");
  t1Card.classList.toggle("not-verified", c.verdict === "NOT_VERIFIED");

  document.getElementById("t1-title").innerText = `${c.marketName} — ${c.targetPeriod}`;
  document.getElementById("t1-claim-id").innerText = c.claimId;
  
  const vBadge = document.getElementById("t1-verdict-badge");
  vBadge.className = `verdict-badge ${c.verdict.toLowerCase().replace('_', '-')}`;
  vBadge.innerHTML = c.verdict === "VERIFIED" ? "✓ VERIFIED" : "✗ NOT_VERIFIED";

  // Formula
  document.getElementById("calc-max-val").innerText = `${c.maxVal}`;
  document.getElementById("calc-min-val").innerText = `${c.minVal}`;
  
  const spreadEl = document.getElementById("calc-spread-val");
  if (c.isNegativeCtrl) {
    spreadEl.innerHTML = `<span class="wrong">50</span> <span style="font-size:0.8rem; color:#94a3b8">(Actual: 116)</span>`;
  } else {
    spreadEl.innerText = `${c.spreadVal}`;
  }

  // Providers boxes
  document.getElementById("max-p-name").innerText = c.maxProvider.name;
  document.getElementById("max-p-int").innerText = `${c.maxProvider.integer} kEUR/MW/yr`;
  document.getElementById("max-p-exact").innerText = `${c.maxProvider.exact.toFixed(3)} kEUR`;

  document.getElementById("min-p-name").innerText = c.minProvider.name;
  document.getElementById("min-p-int").innerText = `${c.minProvider.integer} kEUR/MW/yr`;
  document.getElementById("min-p-exact").innerText = `${c.minProvider.exact.toFixed(3)} kEUR`;

  document.getElementById("t1-statement").innerText = c.statement;

  // Level 2 Section (Comparability)
  const depthSec = document.getElementById("tier2-section");
  if (c.comparability) {
    depthSec.style.display = "block";
    document.getElementById("t2-comparison-title").innerText = `${c.comparability.providerA} vs ${c.comparability.providerB}`;
    document.getElementById("t2-rationale").innerText = c.comparability.rationale;

    const tbody = document.getElementById("matrix-tbody");
    tbody.innerHTML = "";
    c.comparability.dimensions.forEach(dim => {
      const tr = document.createElement("tr");
      const statusClass = dim.status.toLowerCase();
      tr.innerHTML = `
        <td class="dim-name">${dim.name}</td>
        <td class="dim-val">${dim.a}</td>
        <td class="dim-val">${dim.b}</td>
        <td><span class="status-badge ${statusClass}">${dim.status}</span></td>
        <td style="font-size: 0.8rem; color: #94a3b8;">${dim.note}</td>
      `;
      tbody.appendChild(tr);
    });
  } else {
    depthSec.style.display = "none";
  }

  // Table visibility
  document.getElementById("all-de-section").style.display = (key === "DE" || key === "CTRL_NEG") ? "block" : "none";
}

function renderAllDETable() {
  const tbody = document.getElementById("all-de-tbody");
  tbody.innerHTML = "";
  ALL_DE_BENCHMARKS.forEach(item => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td class="rank-pill">#${item.rank}</td>
      <td style="font-weight: 600;">${item.name}</td>
      <td class="val-col">${item.valInt} <span style="font-size:0.75rem; color:#64748b">(${item.valExact.toFixed(2)})</span></td>
      <td style="font-size:0.8rem; color:#cbd5e1">${item.foresight}</td>
      <td style="font-size:0.8rem; color:#cbd5e1">${item.degradation}</td>
      <td style="font-size:0.8rem; color:#94a3b8">${item.basis}</td>
    `;
    tbody.appendChild(tr);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  renderAllDETable();
  renderCase("DE");

  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      renderCase(btn.dataset.key);
    });
  });
});
