const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  runCode: (payload) => ipcRenderer.invoke('run-code', payload),
  detectToolchains: () => ipcRenderer.invoke('detect-toolchains'),
  openExternal: (u) => ipcRenderer.invoke('open-external', u),
  monacoPath: () => ipcRenderer.invoke('monaco-path'),
});
