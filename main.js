const { app, BrowserWindow, ipcMain, Menu, shell } = require('electron');
const path = require('path');
const { runCode, detectToolchains } = require('./runner/runner');

function createWindow() {
  const win = new BrowserWindow({
    width: 1500,
    height: 920,
    minWidth: 1000,
    minHeight: 640,
    backgroundColor: '#1a1a1a',
    title: 'LeetCode + NeetCode Practice',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });
  Menu.setApplicationMenu(null);
  win.webContents.setWindowOpenHandler(({ url }) => { if (/^https:\/\/(leetcode\.com|neetcode\.io)\//.test(url)) shell.openExternal(url); return { action: 'deny' }; });
  win.loadFile(path.join(__dirname, 'renderer', 'index.html'));
}

ipcMain.handle('open-external', (_e, url) => { if (/^https:\/\/(leetcode\.com|neetcode\.io)\//.test(String(url))) shell.openExternal(url); });

ipcMain.handle('run-code', async (_e, payload) => {
  try {
    return await runCode(payload);
  } catch (err) {
    return { status: 'error', message: String(err && err.message ? err.message : err), cases: [] };
  }
});

ipcMain.handle('detect-toolchains', async () => detectToolchains());

ipcMain.handle('monaco-path', () => {
  const p = path.join(path.dirname(require.resolve('monaco-editor/package.json')), 'min', 'vs');
  return p;
});

app.whenReady().then(() => {
  createWindow();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
