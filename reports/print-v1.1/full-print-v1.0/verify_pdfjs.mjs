// Independent browser-engine compatibility check for the repaired page.
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const modules = process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
const {createCanvas, DOMMatrix, Path2D, ImageData} = await import(pathToFileURL(path.join(modules,'@napi-rs/canvas/index.js')));
Object.assign(globalThis, {DOMMatrix, Path2D, ImageData});
const {getDocument} = await import(pathToFileURL(path.join(modules,'pdfjs-dist/legacy/build/pdf.mjs')));
const [input, pageString, output] = process.argv.slice(2);
const start = performance.now();
const doc = await getDocument({data:new Uint8Array(fs.readFileSync(input)),
  standardFontDataUrl: path.join(modules,'pdfjs-dist/standard_fonts/'),
  wasmUrl: path.join(modules,'pdfjs-dist/wasm/'),verbosity:1}).promise;
const page = await doc.getPage(Number(pageString));
const viewport = page.getViewport({scale:1.8});
const canvas = createCanvas(Math.ceil(viewport.width),Math.ceil(viewport.height));
await page.render({canvasContext:canvas.getContext('2d'),viewport}).promise;
fs.writeFileSync(output,canvas.toBuffer('image/png'));
console.log(JSON.stringify({engine:'PDF.js',input,page:Number(pageString),pages:doc.numPages,output,elapsed_ms:Math.round(performance.now()-start)}));
await doc.destroy();
