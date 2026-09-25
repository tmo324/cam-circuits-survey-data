'use strict';
const constraintMetrics={area_um2:'Cell area (µm²)',information_density_bits_per_um2:'Density (bits/µm²)',search_energy_fj_per_bit_per_search:'Reported energy (fJ/bit/search)'};
let authorNames={};
function normalizedSearch(value){return String(value).normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase();}
function matchesDiscovery(d){
 const terms=normalizedSearch(state.query).trim().split(/\s+/).filter(Boolean);
 const haystack=normalizedSearch([d.paper_title,authorNames[d.citation_key]||'',d.cell_structure,d.citation_key,d.manuscript_reference_number,d.technology].join(' '));
 if(!terms.every(t=>haystack.includes(t)))return false;
 return Object.entries(state.limits).every(([key,bounds])=>Number.isFinite(d[key])&&(bounds.min===undefined||d[key]>=bounds.min)&&(bounds.max===undefined||d[key]<=bounds.max));
}
function paretoFrontier(rows,energyKey){
 const density='information_density_bits_per_um2';
 const eligible=rows.filter(d=>Number.isFinite(d[density])&&Number.isFinite(d[energyKey]));
 return eligible.filter(d=>!eligible.some(other=>other[density]>=d[density]&&other[energyKey]<=d[energyKey]&&(other[density]>d[density]||other[energyKey]<d[energyKey]))).sort((a,b)=>a[density]-b[density]||a[energyKey]-b[energyKey]);
}
function addFrontierTrace(traces){
 if(state.figure!=='pareto')return;
 const f=currentFigure(),front=paretoFrontier(visible,f.y);
 traces.push({type:'scatter',mode:'lines+markers',name:'Pareto frontier',x:front.map(d=>d[f.x]),y:front.map(d=>d[f.y]),customdata:front.map(d=>d.source_row),line:{color:'#012169',width:2,dash:'dot'},marker:{symbol:'circle-open',size:21,color:'#012169',line:{width:2}},hovertext:front.map(d=>`<b>Frontier · [${d.manuscript_reference_number}] ${esc(d.cell_structure)}</b><br>Density: ${fmt(d[f.x])} bits/µm²<br>${f.ylabel}: ${fmt(d[f.y])}<br>Click to inspect`),hovertemplate:'%{hovertext}<extra></extra>',showlegend:false});
}
function renderDiscovery(){
 renderTrendControls();
 if(document.activeElement!==$('design-search'))$('design-search').value=state.query;
 for(const key of Object.keys(constraintMetrics))for(const bound of ['min','max']){const input=$('limit-'+key+'-'+bound);if(document.activeElement!==input&&input.dataset.dirty!=='true')input.value=state.limits[key]?.[bound]??'';}
 $('pareto-summary').hidden=state.figure!=='pareto';if(state.figure!=='pareto')return;
 const front=paretoFrontier(visible,currentFigure().y);
 $('pareto-summary').innerHTML=`<strong>${front.length} frontier ${front.length===1?'design':'designs'} among ${visible.length} eligible designs</strong><p>Higher density → · Lower energy ↓. A design is on the frontier when no other filtered design is at least as good in both metrics and strictly better in one. Ties are retained.</p><div>${front.map(d=>`<button data-frontier="${d.source_row}">[${d.manuscript_reference_number}] ${esc(d.technology)} · ${esc(d.cell_structure)}</button>`).join('')}</div><p class="frontier-caveat">This is a frontier for the current subset and energy definition, not an overall ranking. Operating conditions and evaluation methods may differ. Rings mark frontier points; the dashed line only guides the eye.</p>`;
 document.querySelectorAll('[data-frontier]').forEach(b=>b.onclick=()=>selectDesign(Number(b.dataset.frontier)));
}
function clearConstraintDraft(){document.querySelectorAll('[data-bound]').forEach(input=>{input.dataset.dirty='false';input.value='';});$('constraint-error').textContent='';}
function restoreDiscovery(p){
 state.query=(p.get('q')||'').slice(0,300);state.limits={};
 try{const limits=JSON.parse(p.get('limits')||'{}');if(limits&&typeof limits==='object')for(const key of Object.keys(constraintMetrics)){const candidate=limits[key];if(!candidate||typeof candidate!=='object')continue;const bounds={};for(const b of ['min','max'])if(typeof candidate[b]==='number'&&Number.isFinite(candidate[b])&&candidate[b]>=0)bounds[b]=candidate[b];if(bounds.min!==undefined&&bounds.max!==undefined&&bounds.min>bounds.max)continue;if(Object.keys(bounds).length)state.limits[key]=bounds;}}catch(e){/* Ignore malformed shared constraints. */}
 clearConstraintDraft();
}
function wireDiscovery(){
 $('trends').onchange=()=>{state.trends=$('trends').checked;render();};
 const updateSearch=()=>{state.query=$('design-search').value;render();};$('design-search').oninput=updateSearch;$('design-search').onchange=updateSearch;$('design-search').onsearch=updateSearch;
 document.querySelectorAll('[data-bound]').forEach(input=>input.oninput=()=>input.dataset.dirty='true');
 $('constraints').onsubmit=event=>{event.preventDefault();const limits={};for(const [key,label] of Object.entries(constraintMetrics)){const bounds={};for(const b of ['min','max']){const input=$('limit-'+key+'-'+b);if(input.value!=='')bounds[b]=Number(input.value);}if(bounds.min!==undefined&&bounds.max!==undefined&&bounds.min>bounds.max){$('constraint-error').textContent=label+': minimum must not exceed maximum. Previous limits remain active.';return;}if(Object.keys(bounds).length)limits[key]=bounds;}state.limits=limits;document.querySelectorAll('[data-bound]').forEach(input=>input.dataset.dirty='false');$('constraint-error').textContent='';render();tell('Numeric limits applied.');};
 $('clear-limits').onclick=()=>{state.limits={};clearConstraintDraft();render();};
 $('reset').addEventListener('click',()=>{clearConstraintDraft();render();});$('empty-reset').addEventListener('click',()=>{clearConstraintDraft();render();});
}
async function loadDiscovery(){
 const response=await fetch('p00_data/authors.json');if(!response.ok)throw Error('Author index unavailable');authorNames=await response.json();
 $('constraint-fields').innerHTML=Object.entries(constraintMetrics).map(([key,label])=>`<fieldset><legend>${label}</legend><div class="bounds"><label>Minimum<input id="limit-${key}-min" data-bound="min" type="number" min="0" step="any" placeholder="No min" aria-label="Minimum ${label}"></label><label>Maximum<input id="limit-${key}-max" data-bound="max" type="number" min="0" step="any" placeholder="No max" aria-label="Maximum ${label}"></label></div></fieldset>`).join('');
}

function recordTrend(rows,key,maximize=false){
 const yearly=new Map();
 for(const d of rows){if(!Number.isFinite(d.year)||!Number.isFinite(d[key]))continue;const old=yearly.get(d.year);if(old===undefined||(maximize?d[key]>old:d[key]<old))yearly.set(d.year,d[key]);}
 let best=maximize?-Infinity:Infinity;
 return [...yearly].sort((a,b)=>a[0]-b[0]).map(([year,value])=>{best=maximize?Math.max(best,value):Math.min(best,value);return {year,value:best};});
}
function trendAvailable(){return ['6b','7b'].includes(state.figure);}
function renderTrendControls(){
 $('trends').disabled=!trendAvailable();$('trends').checked=state.trends&&trendAvailable();
 $('trend-help').textContent=!trendAvailable()?'Available on Area over time and Search energy.':!state.trends?'Optional dashed step lines, one per technology.':'Dashed steps track the lowest value reported so far within each filtered technology, using the selected energy metric. At least two publication years are needed. Lines stop at the last observation. Different nodes and operating conditions may be pooled; these are dataset records, not forecasts or fitted regressions.';
}
function addTrendTraces(traces){
 if(!state.trends||!trendAvailable())return;
 const f=currentFigure();
 for(const [tech,color] of Object.entries(colors)){
  const points=recordTrend(visible.filter(d=>d.technology===tech),f.y);if(points.length<2)continue;
  const trace={type:'scatter',mode:'lines',name:tech+' best reported so far',x:points.map(p=>p.year),y:points.map(p=>p.value),line:{color,width:2,dash:'dash',shape:'hv'},hovertemplate:esc(tech)+' best so far<br>Through %{x}: %{y:.4g}<extra></extra>',showlegend:false};
  traces.push(trace);if(state.figure==='6b'&&state.scale==='paper')traces.push({...trace,yaxis:'y2'});
 }
}
