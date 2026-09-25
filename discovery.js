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
 $('trend-type').onchange=()=>{state.trendType=$('trend-type').value;render();};
 $('project-trend').onchange=()=>{state.projectTrend=$('project-trend').checked;render();};
 $('projection-year').onchange=()=>{state.projectionYear=Number($('projection-year').value);render();};
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
 const active=state.trends&&trendAvailable(),fit=state.trendType==='fit';
 $('trends').disabled=!trendAvailable();$('trends').checked=active;
 $('fit-controls').hidden=!active;$('trend-type').value=state.trendType;
 $('project-trend').checked=state.projectTrend;$('project-trend').disabled=!fit;
 $('projection-year').value=state.projectionYear;$('projection-year').disabled=!fit||!state.projectTrend;
 $('trend-help').textContent=!trendAvailable()?'Available on Area over time and Search energy.':!active?'Show a fitted curve through all designs, or track the best reported value.':fit?'Solid: log-linear least-squares fit to all positive values, separately by technology. Dashed: if the historical trend continues. Shading: pointwise 95% confidence interval for the fitted geometric mean, not a future-design prediction interval.':'Dashed steps track the lowest value reported so far within each filtered technology. At least two publication years are needed. Lines stop at the last observation.';
 $('fit-summary').hidden=!active||!fit;
 if(!active||!fit)return;
 const key=currentFigure().y;
 $('fit-summary').innerHTML='<details><summary>Fit details and projected values</summary>'+Object.keys(colors).filter(t=>state.tech.has(t)).map(tech=>{
  const model=fitTrend(visible.filter(d=>d.technology===tech),key);
  if(!model)return `<p><b>${tech}</b>: insufficient data (need 3 positive observations across 3 years).</p>`;
  const canProject=model.n>=5&&model.last-model.first>=3;
  const projected=state.projectTrend&&state.projectionYear>model.last;
  return `<p><b style="color:${colors[tech]}">${tech}</b> · n=${model.n} · ${model.first}–${model.last} · ${((Math.exp(model.slope)-1)*100).toFixed(1)}%/year · R² (log) ${model.r2===null?'undefined':model.r2.toFixed(2)}${projected?(canProject?`<br>If continued to ${state.projectionYear}: <b>${fmt(trendEstimate(model,state.projectionYear).value)}</b> ${state.figure==='6b'?'µm²':'fJ/bit/search'}; 95% fit CI ${fmt(trendEstimate(model,state.projectionYear).low)}–${fmt(trendEstimate(model,state.projectionYear).high)}`:'<br>Projection withheld: need 5 observations spanning at least 3 years.') : ''}</p>`;
 }).join('')+'<p class="table-hint">Exploratory model, not a technology roadmap. Each design has equal weight; designs from the same paper may be correlated. Different nodes, modes and conditions may be pooled. Bands assume independent, constant-variance normal errors in log space and omit selection bias and model uncertainty. Filtering changes the fit. <a href="https://www.itl.nist.gov/div898/handbook/pmd/section4/pmd431.htm" target="_blank" rel="noreferrer">Fit method ↗</a></p></details>';
}
// Two-sided 95% Student t critical values, df 1–40. Dataset has 41 rows at most.
const t95=[0,12.706,4.303,3.182,2.776,2.571,2.447,2.365,2.306,2.262,2.228,2.201,2.179,2.160,2.145,2.131,2.120,2.110,2.101,2.093,2.086,2.080,2.074,2.069,2.064,2.060,2.056,2.052,2.048,2.045,2.042,2.040,2.037,2.035,2.032,2.030,2.028,2.026,2.024,2.023,2.021];
function fitTrend(rows,key){
 const valid=rows.filter(d=>Number.isFinite(d.year)&&Number.isFinite(d[key])&&d[key]>0),n=valid.length;
 if(n<3||new Set(valid.map(d=>d.year)).size<3)return null;
 const mx=valid.reduce((a,d)=>a+d.year,0)/n,my=valid.reduce((a,d)=>a+Math.log(d[key]),0)/n;
 const sxx=valid.reduce((a,d)=>a+(d.year-mx)**2,0),sxy=valid.reduce((a,d)=>a+(d.year-mx)*(Math.log(d[key])-my),0),slope=sxy/sxx;
 const sse=valid.reduce((a,d)=>a+(Math.log(d[key])-my-slope*(d.year-mx))**2,0),sst=valid.reduce((a,d)=>a+(Math.log(d[key])-my)**2,0);
 return {n,mx,my,sxx,slope,sigma:Math.sqrt(sse/(n-2)),critical:t95[Math.min(40,n-2)],r2:sst<1e-20?null:Math.max(0,1-sse/sst),first:Math.min(...valid.map(d=>d.year)),last:Math.max(...valid.map(d=>d.year))};
}
function trendEstimate(m,year){const logValue=m.my+m.slope*(year-m.mx),half=m.critical*m.sigma*Math.sqrt(1/m.n+(year-m.mx)**2/m.sxx);return {year,value:Math.exp(logValue),low:Math.exp(logValue-half),high:Math.exp(logValue+half)};}
function fittedTraces(tech,color,key){
 const m=fitTrend(visible.filter(d=>d.technology===tech),key);if(!m)return [];
 const end=state.projectTrend&&m.n>=5&&m.last-m.first>=3?Math.max(m.last,state.projectionYear):m.last;
 const sample=(a,b)=>Array.from({length:61},(_,i)=>trendEstimate(m,a+(b-a)*i/60));
 const points=sample(m.first,end),base={type:'scatter',mode:'lines',showlegend:false};
 const result=[{...base,x:points.map(p=>p.year),y:points.map(p=>p.low),line:{width:0},hoverinfo:'skip'}, {...base,x:points.map(p=>p.year),y:points.map(p=>p.high),line:{width:0},fill:'tonexty',fillcolor:color+'18',hoverinfo:'skip'}];
 for(const [a,b,dash] of [[m.first,m.last,'solid'],[m.last,end,'dash']]){if(b<=a)continue;const ps=sample(a,b);result.push({...base,name:tech+' fitted trend',x:ps.map(p=>p.year),y:ps.map(p=>p.value),line:{color,width:2,dash},hovertemplate:tech+(dash==='dash'?' conditional projection':' fitted trend')+'<br>Year %{x:.1f}: %{y:.4g}<extra></extra>'});}
 return result;
}
function addTrendTraces(traces){
 if(!state.trends||!trendAvailable())return;
 const f=currentFigure();
 for(const [tech,color] of Object.entries(colors)){
  if(state.trendType==='fit'){const fitted=fittedTraces(tech,color,f.y);traces.push(...fitted);if(state.figure==='6b'&&state.scale==='paper')traces.push(...fitted.map(t=>({...t,yaxis:'y2'})));continue;}
  const points=recordTrend(visible.filter(d=>d.technology===tech),f.y);if(points.length<2)continue;
  const trace={type:'scatter',mode:'lines',name:tech+' best reported so far',x:points.map(p=>p.year),y:points.map(p=>p.value),line:{color,width:2,dash:'dash',shape:'hv'},hovertemplate:esc(tech)+' best so far<br>Through %{x}: %{y:.4g}<extra></extra>',showlegend:false};
  traces.push(trace);if(state.figure==='6b'&&state.scale==='paper')traces.push({...trace,yaxis:'y2'});
 }
}
