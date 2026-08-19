// Hello PSI - JavaScript reference seed (Node >= 16.17, zero dependencies).
//
// Apex PSI — Universal Verification Layer. Proposed open standard under active development. Verification free forever (MIT). IETF drafts are individual submissions, not formally endorsed. Verify everything yourself.
//
// Implements rules R1-R10 of PSI-SEAL/1. Run:  node hello-psi.js
const crypto = require("crypto");
const https = require("https");
const http = require("http");

// Schema digest pinned 2026-08-20 from the live canonical schema at
// https://ai-governance-standard.com/.well-known/psi-schema.json
// (SHA-256 over RFC 8785 JCS of the parsed document). The seed is fully
// deterministic and offline by design; run with --check-live to recompute
// from the network and confirm the pin is current.
const PINNED_SCHEMA_DIGEST =
  "454743698e1b23d5eddb7fc4a97ae1c8c33047921ef360d8e6c86d61f2fe9e77";
const SCHEMA_URL = "https://ai-governance-standard.com/.well-known/psi-schema.json";
const SEALED_AT = "2026-08-20T00:00:00.000Z"; // R6, pinned for reproducible vectors

const VECTORS = [
  ["vector-0", ""],
  ["vector-1", "Hello, PSI."],
  ["vector-2", '{"model":"example","output":"The seal is the math."}'],
];

function sha256hex(input) {
  return crypto.createHash("sha256").update(input).digest("hex");
}

function jcsString(s) {
  let out = '"';
  for (const ch of s) {
    const c = ch.codePointAt(0);
    if (ch === '"') out += '\\"';
    else if (ch === "\\") out += "\\\\";
    else if (ch === "\b") out += "\\b";
    else if (ch === "\f") out += "\\f";
    else if (ch === "\n") out += "\\n";
    else if (ch === "\r") out += "\\r";
    else if (ch === "\t") out += "\\t";
    else if (c < 0x20) out += "\\u" + c.toString(16).padStart(4, "0");
    else out += ch;
  }
  return out + '"';
}

function jcs(value) {
  // R1 - RFC 8785 (PSI subset: no floats). JS string sort compares UTF-16 code units.
  if (value === null) return "null";
  if (typeof value === "boolean") return value ? "true" : "false";
  if (typeof value === "number") return String(value);
  if (typeof value === "string") return jcsString(value);
  if (Array.isArray(value)) return "[" + value.map(jcs).join(",") + "]";
  if (typeof value === "object") {
    const keys = Object.keys(value).sort();
    return "{" + keys.map((k) => jcsString(k) + ":" + jcs(value[k])).join(",") + "}";
  }
  throw new Error("unsupported type in PSI envelope");
}

// Used only by --check-live. http/https modules honour proxy env vars exactly
// like Python's urllib (undici fetch() does not).
function httpGet(url, redirects) {
  redirects = redirects === undefined ? 5 : redirects;
  return new Promise((resolve, reject) => {
    const mod = url.startsWith("https:") ? https : http;
    const req = mod.get(url, { headers: { accept: "application/json" } }, (res) => {
      if (
        res.statusCode >= 301 &&
        res.statusCode <= 308 &&
        res.headers.location &&
        redirects > 0
      ) {
        res.resume();
        resolve(httpGet(new URL(res.headers.location, url).toString(), redirects - 1));
        return;
      }
      if (res.statusCode !== 200) {
        res.resume();
        reject(new Error("HTTP " + res.statusCode));
        return;
      }
      let body = "";
      res.setEncoding("utf-8");
      res.on("data", (c) => {
        body += c;
      });
      res.on("end", () => resolve(body));
    });
    req.on("error", reject);
    req.setTimeout(10000, () => {
      req.destroy(new Error("timeout"));
    });
  });
}

async function fetchSchemaDigest() {
  try {
    const body = await httpGet(SCHEMA_URL);
    const doc = JSON.parse(body);
    return sha256hex(Buffer.from(jcs(doc), "utf-8"));
  } catch (e) {
    return null;
  }
}

function seal(text, name, sealedAt, sd) {
  const raw = Buffer.from(text, "utf-8");
  const h = sha256hex(raw); // R5
  const leaf = sha256hex(Buffer.from("PSI1:" + h, "ascii")); // R9
  const envelope = {
    // R3 order
    schema: "PSI-SEAL/1.0.0",
    schema_digest: sd || "0".repeat(64),
    sealed_at: sealedAt, // R6
    subject: {
      // R7
      name: name.normalize("NFC"),
      size_bytes: raw.length,
    },
    hash: h, // R4/R5
    merkle: { leaf, root: leaf }, // R8
  };
  const sealHash = sha256hex(Buffer.from(jcs(envelope), "utf-8")); // R10
  return { envelope, sealHash };
}

(async () => {
  const sd = PINNED_SCHEMA_DIGEST;
  console.log("language: javascript");
  console.log("schema_digest:", sd);
  if (process.argv.includes("--check-live")) {
    const live = await fetchSchemaDigest();
    console.log("live_digest  :", live || "UNREACHABLE");
    console.log("pin_current  :", live === sd ? "yes" : "no");
  }
  for (const [name, text] of VECTORS) {
    const { envelope, sealHash } = seal(text, name, SEALED_AT, sd);
    console.log("---", name);
    console.log("hash      :", envelope.hash);
    console.log("leaf      :", envelope.merkle.leaf);
    console.log("seal_hash :", sealHash);
    console.log("envelope  :", jcs(envelope));
  }
})();
