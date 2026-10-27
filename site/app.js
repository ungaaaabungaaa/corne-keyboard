// SPDX-License-Identifier: GPL-2.0-or-later
'use strict';
const ns='http://www.w3.org/2000/svg';
let data;
function render(index){
 const layer=data.layers[index],svg=document.getElementById('layout');svg.replaceChildren();
 data.positions.forEach((position,i)=>{
  const x=35+position.x*74,y=20+position.y*70;
  const rect=document.createElementNS(ns,'rect');
  Object.entries({x,y,width:68,height:60,rx:5,class:i>=36?'thumb':'key'}).forEach(([key,value])=>rect.setAttribute(key,value));
  const label=document.createElementNS(ns,'text');Object.entries({x:x+34,y:y+35,'text-anchor':'middle',class:'key-text'}).forEach(([key,value])=>label.setAttribute(key,value));label.textContent=layer.keys[i].replace('KC_','');
  svg.append(rect,label);
 });
 document.querySelectorAll('[data-layer]').forEach(button=>button.setAttribute('aria-pressed',Number(button.dataset.layer)===index));
 document.getElementById('status').textContent=`${layer.name} / 42 physical positions / preview only`;
 document.getElementById('layer-name').textContent=layer.name;
 const table=document.getElementById('actions');table.replaceChildren();
 data.positions.forEach((position,i)=>{
  const [row,col]=position.matrix,side=row<4?'Left':'Right',localRow=row%4;
  const tr=document.createElement('tr'),th=document.createElement('th'),td=document.createElement('td');th.scope='row';
  th.textContent=`${side} ${localRow===3?'thumb':'row '+(localRow+1)} · key ${localRow===3?(side==='Left'?col-2:6-col):(side==='Left'?col+1:6-col)}`;
  td.textContent=layer.keys[i];tr.append(th,td);table.append(tr);
 });
 document.getElementById('help').textContent=['QWERTY letters and dedicated modifiers. Thumb keys select the other layers.','Numbers, navigation, editing and F1–F10. Hold NAV on the left thumb.','Punctuation and paired symbols. Hold SYMBOL on the right thumb.','Hold NAV and SYMBOL together. Media keys and F11/F12; BOOT enters the bootloader only on the real keyboard.'][index];
}
fetch('keymap.json').then(response=>{if(!response.ok)throw Error();return response.json();}).then(value=>{data=value;render(0);document.querySelectorAll('[data-layer]').forEach(button=>button.addEventListener('click',()=>render(Number(button.dataset.layer))));}).catch(()=>{document.getElementById('status').textContent='Layout could not be loaded. Serve the generated site over local HTTP.';});
