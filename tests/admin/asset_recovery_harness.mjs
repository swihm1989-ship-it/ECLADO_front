import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
const source = readFileSync("admin/eclado_admin/assets/asset_recovery.js", "utf8");
const {default: render} = await import(`data:text/javascript;base64,${Buffer.from(source).toString("base64")}`);
const values = new Map([["eclado.preview.session.v1", "existing-session"]]);
const handlers = new Map();
let reloads = 0;
globalThis.sessionStorage = {
    getItem: key => values.get(key) ?? null,
    setItem: (key, value) => values.set(key, value),
};
globalThis.window = {
    addEventListener: (name, callback) => handlers.set(name, callback),
    location: {reload: () => reloads++},
};
render({data:{revision:"test-v1"}});
assert.equal(typeof handlers.get("vite:preloadError"), "function");
const event = payload => ({payload, preventDefault(){this.prevented = true;}});
const unrelated = event(new Error("business validation"));
handlers.get("vite:preloadError")(unrelated);
assert.equal(reloads, 0);
const missing = event(new TypeError("Failed to fetch dynamically imported module: /static/js/TextInput.hash.js"));
handlers.get("vite:preloadError")(missing);
assert.equal(reloads, 1);
assert.equal(missing.prevented, true);
assert.equal(values.get("eclado.preview.session.v1"), "existing-session");
handlers.get("vite:preloadError")(missing);
assert.equal(reloads, 1, "No reload loop within a tab/revision");
globalThis.sessionStorage = {getItem(){throw Error("blocked");}};
handlers.get("vite:preloadError")(missing);
assert.equal(reloads, 1, "Blocked storage must not trigger unlimited reloads");
console.log("asset recovery: matching errors only, one reload, token preserved, blocked storage safe");
