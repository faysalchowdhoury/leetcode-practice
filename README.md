# LeetCode + NeetCode Practice (desktop app)

223 problems in 31 concept groups, each tagged **Both**, **NeetCode only (N)** or **LeetCode only (L)**.
Monaco code editor, Run (first 3 cases) / Submit (all tests), progress tracking, code saved per problem and language.

## Run from source
    npm install
    npm start

## Build installers
Installers must be built on their own OS (or use the included GitHub Actions workflow, which builds both):
    npm run dist:win   # on Windows -> dist/*.exe
    npm run dist:mac   # on macOS   -> dist/*.dmg
Push a `v*` tag or run the "Build installers" workflow on GitHub and download the artifacts.
(Mac builds are unsigned: right-click > Open the first time.)

## Languages (your code runs locally)
| Language | Needs on your computer |
|---|---|
| JavaScript | nothing (uses Electron's built-in Node) |
| Python 3 | `python3` / `py -3` on PATH |
| Java | JDK (`javac` + `java`) on PATH |
| C++ | `g++` or `clang++` (Xcode CLT on Mac, MinGW-w64 on Windows) |

Java and C++ are offered only for problems with simple types (arrays, strings, numbers): 164 of 223.
Each run has a 10 second limit.

## Regenerating problem data
`python3 authoring/build.py` rebuilds `renderer/problems-data.js`; expected outputs come from reference solutions.

## Double-click installers
- Windows: run `LeetCode-Practice-Setup-*.exe` (one-click install, desktop + Start menu shortcut). SmartScreen may warn because the app is unsigned: More info > Run anyway.
- Mac: open the `.dmg`, drag the app to Applications; first launch: right-click > Open (unsigned).

## Website version (GitHub Pages)
The same UI also runs in a browser: JavaScript runs in a Web Worker and Python runs in Pyodide (WebAssembly), all on the visitor's computer, so there is no server to run or secure.
Java and C++ are desktop-app only. The Python runtime and editor load from the jsDelivr CDN.

    node web/build.js     # builds ./docs (open it through any static web server)

To publish: push the repo to GitHub, then Settings > Pages > Source: "GitHub Actions". The included `pages.yml` workflow builds and deploys on every push to `main`.
