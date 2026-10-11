/* Editorial Evidence Lens / Pack-source journey. No execution, payment, or verification logic. */
(() => {
  const lens = document.querySelector('[data-evidence-lens]');
  if (lens) {
    const tabButtons = [...lens.querySelectorAll('[data-claim]')];
    const modes = [...lens.querySelectorAll('[data-lens-toggle]')];
    const panes = [...lens.querySelectorAll('[data-claim-panel]')];
    let claim = 0;
    let mode = 'story';
    const display = () => {
      tabButtons.forEach(button => {
        const selected = Number(button.dataset.claim) === claim;
        button.classList.toggle('is-active', selected);
        button.setAttribute('aria-pressed', String(selected));
      });
      modes.forEach(button => {
        const selected = button.dataset.lensToggle === mode;
        button.classList.toggle('is-active', selected);
        button.setAttribute('aria-pressed', String(selected));
      });
      panes.forEach(pane => {
        pane.hidden = Number(pane.dataset.claimPanel) !== claim || pane.dataset.lensMode !== mode;
      });
    };
    tabButtons.forEach(button => button.addEventListener('click', () => {
      claim = Number(button.dataset.claim);
      display();
    }));
    modes.forEach(button => button.addEventListener('click', () => {
      mode = button.dataset.lensToggle;
      display();
    }));
    display();
  }

  const journey = document.querySelector('[data-evidence-journey]');
  if (!journey) return;
  const dataNode = document.getElementById('v2-lens-translations');
  if (!dataNode) return;
  let data;
  try {
    const locales = JSON.parse(dataNode.textContent);
    data = locales[journey.dataset.language];
  } catch {
    return;
  }
  if (!data) return;

  const packIds = ['critical-cve-blocker', 'ghg-scope-1-2-guard', 'iso27001-policy-review'];
  const choices = [...journey.querySelectorAll('[data-journey-pack]')];
  const stations = [...journey.querySelectorAll('[data-journey-step]')];
  const title = journey.querySelector('[data-journey-title]');
  const desc = journey.querySelector('[data-journey-description]');
  const stageNumber = journey.querySelector('[data-journey-number]');
  const scenario = journey.querySelector('[data-journey-scenario]');
  const source = journey.querySelector('[data-journey-primary]');
  const sourceBase = 'https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/';
  const sourceDoc = sourceBase + 'docs/STANDALONE_VERIFIER.md';
  let pack = 0;
  let stage = 0;
  const sourcesFor = id => {
    const root = sourceBase + 'packs/core/' + id + '/';
    return [
      root + 'tests/cases.yaml',
      root + 'README.md',
      root + 'pack.yaml',
      root + 'tests/cases.yaml',
      sourceDoc,
      '/verifier/'
    ];
  };
  function show() {
    choices.forEach((button, i) => {
      const yes = i === pack;
      button.classList.toggle('is-active', yes);
      button.setAttribute('aria-pressed', String(yes));
    });
    stations.forEach((button, i) => {
      const yes = i === stage;
      button.classList.toggle('is-active', yes);
      button.setAttribute('aria-pressed', String(yes));
    });
    scenario.textContent = data.scenarios[pack];
    stageNumber.textContent = String(stage + 1).padStart(2, '0') + ' / 06';
    title.textContent = data.stageNames[stage];
    desc.textContent = data.stageNotes[stage];
    const href = sourcesFor(packIds[pack])[stage];
    source.href = href;
    if (href.startsWith('https://')) {
      source.target = '_blank';
      source.rel = 'noopener noreferrer';
    } else {
      source.removeAttribute('target');
      source.removeAttribute('rel');
    }
  }
  choices.forEach((button, i) => button.addEventListener('click', () => {
    pack = i;
    show();
  }));
  stations.forEach((button, i) => button.addEventListener('click', () => {
    stage = i;
    show();
  }));
  // Keep the right-hand homepage carousel and the source inspector in sync.
  window.addEventListener('paygod:stage', event => {
    if (Number.isInteger(event.detail?.index)) {
      const chosen = event.detail.index;
      if (chosen >= 0 && chosen < stations.length) {
        stage = chosen;
        show();
      }
    }
  });
  show();
})();
