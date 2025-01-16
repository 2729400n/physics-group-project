const state = {
  id: null,
  count: 0,
  hits: 0,
  needleLength: 0,
  spacingwidth: 0,
  pi: Number.NaN,
  iters: 1,
};
const THROW_API = "/throw_needle";
const UPDATE_API = "/";
const RESET_API = "/";

async function init() {
  let resp = await fetch("/", { method: "POST" });
  try {
    let data = await resp.json();
    state.id = data.id ?? null;
    state.count = data.count || 0;
    state.hits = data.hits || 0;
  } catch (error) {
    throw new Error("failed to fetch the initial payload!");
  }
}

async function throwNeedle() {
  let payload = JSON.stringify(state);
  let resp = await fetch("/buffon.py", {
    method: "POST",
    body: payload,
    headers: { "Content-Type": "application/json" },
  });
  try {
    let data = await resp.json();
    state.id = data.id ?? null;
    state.count = data.count || 0;
    state.hits = data.hits || 0;
    console.log(state);
  } catch (error) {
    throw new Error("failed to fetch the initial payload!");
  }
}

function cheatOpen(elem: HTMLElement) {
  let cheatBox = document.createElement("section");
  cheatBox.id = "cheactBox";
  let probBox = document.createElement("input");
  probBox.type = "number";
  probBox.placeholder = "";
  probBox.id = "probBox";
  probBox.name = "probBox";

  let probLabel = document.createElement("label");
  probLabel.htmlFor = "probBox";

  let cheatButton = document.createElement("button");
  cheatButton.addEventListener('click',(ev)=>{})
  elem.append();
}

function saveCanvas(params) {
  let image = canvas.toDataURL("image/png");
  let imageA = document.createElement("a", {
    href: image,
    download: "buffonCanvas.png",
  });
  imageA.click();
}

function updateParams(elem) {
  let fields = elem.parentElement.getElementsByTagName("input");
  for (let field of fields) {
    state[field.name] = (state[field.name] ?? "").constructor(
      field.value ?? "0"
    );
  }
  state.hits = 0;
  state.count = 0;
  console.log(state);
}

async function syncState() {
  let resp = await fetch("/throwNeedle", { method: "HEAD" });
  try {
    let data = await resp.json();
    state.id = data.id ?? null;
    state.count = data.count || 0;
    state.hits = data.hits || 0;
  } catch (error) {
    throw new Error("failed to fetch the initial payload!");
  }
}

function resetData(params) {}

function reset(params) {}
