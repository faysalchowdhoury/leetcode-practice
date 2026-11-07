// Runs the Python test harness inside Pyodide.
let pyodide = null;
let harnessSrc = null;
onmessage = async (e) => {
  const m = e.data;
  if (m.t === 'init') {
    try {
      importScripts('https://cdn.jsdelivr.net/pyodide/v' + m.version + '/full/pyodide.js');
      pyodide = await loadPyodide();
      harnessSrc = await (await fetch('harness.py')).text();
      harnessSrc = harnessSrc.replace('EMIT_HOOK = None', 'EMIT_HOOK = _emit_hook');
      postMessage({ t: 'ready' });
    } catch (err) { postMessage({ t: 'initerror', msg: String(err && err.message || err) }); }
    return;
  }
  if (m.t === 'run') {
    pyodide.FS.writeFile('input.json', m.input);
    pyodide.FS.writeFile('solution.py', m.code);
    pyodide.setStdout({ batched: (s) => postMessage({ t: 'out', s }) });
    pyodide.setStderr({ batched: (s) => postMessage({ t: 'out', s }) });
    const ns = pyodide.globals.get('dict')();
    ns.set('_emit_hook', (line) => postMessage({ t: 'rec', line }));
    ns.set('__name__', '__main__');
    try { pyodide.runPython(harnessSrc, { globals: ns }); }
    catch (err) { postMessage({ t: 'rec', line: JSON.stringify({ fatal: String(err && err.message || err).split('\n').slice(-6).join('\n') }) }); }
    ns.destroy();
    postMessage({ t: 'done' });
  }
};
