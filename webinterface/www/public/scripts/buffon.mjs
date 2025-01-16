"use strict";

const canvas = document.createElement("canvas");

async function viewDidLoad() {
  Object.assign(canvas, {
    id: "floor-canvas",
    width: 200,
    height: 200,
  });
  let root_drawer = document.getElementById("root_drawer");
  root_drawer.appendChild(canvas);
  root_drawer.style.height = `${canvas.height}`;
  root_drawer.style.width = `${canvas.width}`;
}


async function drawNeedles(){

}

