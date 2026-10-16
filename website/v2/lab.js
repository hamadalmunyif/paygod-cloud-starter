/* Evidence Lab only. Policy display is illustrative; integrity calls the unchanged browser verifier. */
import {verifyTransport, VERIFIER_VERSION} from "./verifier.mjs";

const byId = id => document.getElementById(id);
const labels = JSON.parse(byId("lab-labels").textContent);
const score = byId("cve-score");
const remediation = byId("remediation");
const scanComplete = byId("scan-complete");
const expected = byId("cve-outcome");
const why = byId("cve-reason");

function renderCve() {
  const scoreX10 = Number(score.value);
  byId("cve-value").textContent = (scoreX10 / 10).toFixed(1);
  let state, explanation;
  if (!scanComplete.checked) {
    state = "withheld";
    explanation = labels.withheldwhy;
  } else if (remediation.value === "fixed" || scoreX10 < 70) {
    state = "allow";
    explanation = labels.allowwhy;
  } else if (scoreX10 >= 90) {
    state = "deny";
    explanation = labels.denywhy;
  } else {
    state = "flag";
    explanation = labels.flagwhy;
  }
  expected.dataset.state = state;
  expected.textContent = labels[state];
  why.textContent = explanation;
}
score.addEventListener("input", renderCve);
remediation.addEventListener("change", renderCve);
scanComplete.addEventListener("change", renderCve);
renderCve();

const goodButton = byId("verify-clean");
const badButton = byId("verify-tampered");
const outcome = byId("integrity-outcome");
const detail = byId("integrity-detail");
const checks = byId("integrity-checks");
let samplePromise;
let attempt = 0;

async function getPreparedSample() {
  if (!samplePromise) {
    samplePromise = fetch("/lab/assets/sample.json", {cache:"no-store"}).then(async response => {
      if (!response.ok) throw new Error("Fixture not available: HTTP " + response.status);
      const raw = await response.text();
      if (new TextEncoder().encode(raw).length > 2000000) throw new Error("Fixture over size limit");
      const parsed = JSON.parse(raw);
      if (parsed.format !== "paygod-demo-transport/1" || typeof parsed.files?.["measurement.json"] !== "string")
        throw new Error("Unexpected synthetic fixture");
      return parsed;
    }).catch(error => {samplePromise = undefined; throw error;});
  }
  return samplePromise;
}

async function runChallenge(mode) {
  const selected = ++attempt;
  goodButton.disabled = true;
  badButton.disabled = true;
  outcome.dataset.state = "idle";
  outcome.textContent = labels.checking;
  detail.textContent = "";
  checks.textContent = "";
  try {
    const original = await getPreparedSample();
    const transport = structuredClone(original);
    if (mode === "tampered") {
      const before = transport.files["measurement.json"];
      const changed = before.replace('"value": 420', '"value": 421');
      if (before === changed) throw new Error("Expected fixture bytes not found");
      transport.files["measurement.json"] = changed;
    }
    const result = await verifyTransport(transport, {trustedIssuerKeys:{}});
    if (selected !== attempt) return;
    const good = result.verification?.integrity === "verified";
    outcome.dataset.state = good ? "allow" : "deny";
    outcome.textContent = good ? labels.verified : labels.failed;
    const failures = (result.checks || []).filter(item => !item.ok).map(item => item.name);
    const passed = (result.checks || []).filter(item => item.ok).length;
    detail.textContent = good
      ? "v" + VERIFIER_VERSION + " · SHA-256 / manifest / receipt / ledger consistency"
      : (failures.join(" · ") || (result.errors || []).join(" · ") || "Integrity rejected");
    checks.textContent = passed + " / " + (result.checks || []).length + " checks passed";
  } catch (error) {
    if (selected !== attempt) return;
    outcome.dataset.state = "deny";
    outcome.textContent = labels.failure;
    detail.textContent = String(error?.message || error);
  } finally {
    if (selected === attempt) {
      goodButton.disabled = false;
      badButton.disabled = false;
    }
  }
}
goodButton.addEventListener("click", () => runChallenge("clean"));
badButton.addEventListener("click", () => runChallenge("tampered"));
