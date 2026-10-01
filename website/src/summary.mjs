// Display-only extraction. These values are declarations, never verification results.
const isObject = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const displayText = (value, fallback = 'Not declared') => typeof value === 'string' && value.trim() ? value.slice(0, 180) : fallback;
export function summarizeTransport(input) {
  if (!isObject(input) || input.format !== 'paygod-demo-transport/1' || !isObject(input.files)) throw Error('Choose a PayGod demo bundle JSON file.');
  const names = Object.keys(input.files);
  if (names.length > 32 || names.some(name => typeof input.files[name] !== 'string')) throw Error('Unsupported bundle file map.');
  const read = name => {
    if (!Object.hasOwn(input.files, name)) return {};
    try { const value = JSON.parse(input.files[name]); return isObject(value) ? value : {}; } catch { return {}; }
  };
  const measurement = read('measurement.json'), receipt = read('receipt.json'), manifest = read('manifest.json');
  const value = typeof measurement.value === 'number' && Number.isFinite(measurement.value) ? String(measurement.value) : 'Not declared';
  return {
    measurement: value + (typeof measurement.unit === 'string' ? ' ' + measurement.unit.slice(0, 24) : ''),
    metric: displayText(measurement.metric, 'No measurement summary available'),
    source: displayText(measurement.source),
    decision: displayText(receipt.verdict?.value).toUpperCase(),
    rule: displayText(receipt.verdict?.rule_name),
    time: displayText(receipt.generated_at),
    files: names.length,
    committed: Array.isArray(manifest.files) ? manifest.files.length : 0
  };
}
