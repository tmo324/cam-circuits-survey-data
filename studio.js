'use strict';
const metricLabels={process_node_nm:'Process node (nm)',area_um2:'Cell area (µm²)',information_density_bits_per_um2:'Information density (bits/µm²)',search_energy_fj_per_bit_per_search:'Reported energy (fJ/bit/search)',layout_normalized_search_energy:'Normalized energy (fJ/bit/search)',year:'Publication year',bits_stored:'Stored information (bits)',layout_factor_k:'Layout factor k'};
let conditions={},schematics=[];
function currentFigure(){
 if(state.figure==='pareto'){const y=state.energy==='raw'?'search_energy_fj_per_bit_per_search':'layout_normalized_search_energy';return {title:'Energy–density Pareto frontier',x:'information_density_bits_per_um2',y,xlabel:metricLabels.information_density_bits_per_um2,ylabel:metricLabels[y],scale:'log'};}
 if(state.figure==='custom')return {title:'Explore the trade-offs',x:state.x,y:state.y,xlabel:metricLabels[state.x],ylabel:metricLabels[state.y],scale:'log'};
 if(state.figure==='7b'&&state.energy==='raw')return {...figures['7b'],title:'Reported search energy',y:'search_energy_fj_per_bit_per_search',ylabel:metricLabels.search_energy_fj_per_bit_per_search};
 return figures[state.figure];
}
function conditionText(d,key){return conditions[d.source_row]?.[key]||'Not recorded';}
function matchingSchematic(d){const norm=s=>s.toLowerCase().replace(/\s/g,'');return schematics.find(s=>s.citation_key===d.citation_key&&s.technology===d.technology&&norm(s.cell_configuration)===norm(d.cell_structure));}
function designExtras(d){const s=matchingSchematic(d);return `<div class="design-additions"><p class="table-hint">Authors: ${esc(authorNames[d.citation_key]||'Not recorded')}</p><button class="outline-button" id="pin-design">${state.pins.includes(d.source_row)?'✓ Remove from comparison':'+ Pin to comparison'}</button><details class="conditions" open><summary>Comparison conditions</summary><dl><dt>Supply voltage (V)</dt><dd>${esc(conditionText(d,'supply_voltage_v'))}</dd><dt>Match-line width (bits)</dt><dd>${esc(conditionText(d,'match_line_bits'))}</dd><dt>Full array size</dt><dd>${esc(conditionText(d,'array_size'))}</dd><dt>Measured / simulated</dt><dd>${esc(conditionText(d,'evaluation_method'))}</dd></dl><a href="https://github.com/tmo324/cam-circuits-survey-data/blob/90ebde2d488055d6142c93556d618eb8eb6fc609/data/raw/cam_survey_main_export.csv" target="_blank" rel="noreferrer">Source workbook, row ${d.source_row} ↗</a><p>Values transcribed as recorded. Match-line width is not full array capacity.</p></details>${s?`<figure class="design-schematic"><a href="${s.asset}" target="_blank" rel="noreferrer"><img src="${s.asset}" alt="${esc(s.technology+' '+s.cell_configuration+' '+s.storage_type)} cell schematic"></a><figcaption>Survey panel: ${esc(s.cell_configuration)} · ${esc(s.storage_type)}. Click to enlarge.</figcaption></figure>`:'<p class="table-hint">No exact matching schematic is available for this record. Browse the circuit gallery below.</p>'}</div>`;}
function togglePin(id){if(state.pins.includes(id))state.pins=state.pins.filter(v=>v!==id);else{if(state.pins.length===4){tell('You can compare four designs. Remove one before adding another.');return;}state.pins.push(id);}render();}
function renderComparison(){
 const pinned=state.pins.map(id=>data.find(d=>d.source_row===id)).filter(Boolean);
 $('compare-count').textContent=pinned.length+' / 4';$('clear-pins').disabled=!pinned.length;
 if(!pinned.length){$('comparison-content').innerHTML='<div class="comparison-empty">Choose two to four designs to compare their metrics and available operating conditions.</div>';return;}
 const fields=[['Technology',d=>d.technology],['Storage mode',d=>d.storage_mode_for_plot||'Not reported'],['Year',d=>fmt(d.year)],['Process node (nm)',d=>fmt(d.process_node_nm)],['Cell area (µm²)',d=>fmt(d.area_um2)],['Density (bits/µm²)',d=>fmt(d.information_density_bits_per_um2)],['Reported energy (fJ/bit/search)',d=>fmt(d.search_energy_fj_per_bit_per_search)],['Normalized energy (fJ/bit/search)',d=>fmt(d.layout_normalized_search_energy)],['Layout factor k',d=>fmt(d.layout_factor_k)],['Supply voltage (V)',d=>conditionText(d,'supply_voltage_v')],['Match-line width (bits)',d=>conditionText(d,'match_line_bits')],['Full array size',d=>conditionText(d,'array_size')],['Measured / simulated',d=>conditionText(d,'evaluation_method')]];
 $('comparison-content').innerHTML=`${pinned.length===1?'<p class="table-hint">Pin one more design to start comparing.</p>':''}<div class="table-scroll compare-scroll"><table><caption class="sr-only">Pinned designs and operating conditions</caption><thead><tr><th scope="col">Metric / condition</th>${pinned.map(d=>`<th scope="col" style="border-top:3px solid ${colors[d.technology]}"><button data-inspect="${d.source_row}">[${d.manuscript_reference_number}] ${esc(d.cell_structure)} · ${d.process_node_nm} nm</button><button data-remove="${d.source_row}" aria-label="Remove reference ${d.manuscript_reference_number} from comparison">×</button><small>${visible.some(v=>v.source_row===d.source_row)?'In current view':'Outside current view'}</small></th>`).join('')}</tr></thead><tbody>${fields.map(([label,value])=>`<tr><th scope="row">${label}</th>${pinned.map(d=>`<td>${esc(value(d))}</td>`).join('')}</tr>`).join('')}<tr><th scope="row">Source paper</th>${pinned.map(d=>`<td class="comparison-paper"><a href="${d.doi?'https://doi.org/'+encodeURI(d.doi):'https://scholar.google.com/scholar?q='+encodeURIComponent(d.paper_title)}" target="_blank" rel="noreferrer">${esc(d.paper_title)} ↗</a></td>`).join('')}</tr></tbody></table></div><p class="table-hint">Different test conditions can limit direct comparisons. “Not recorded” means the released workbook does not specify the condition; it does not mean the source paper omits it.</p>`;
 document.querySelectorAll('[data-remove]').forEach(b=>b.onclick=()=>togglePin(Number(b.dataset.remove)));
 document.querySelectorAll('[data-inspect]').forEach(b=>b.onclick=()=>selectDesign(Number(b.dataset.inspect)));
}
function viewHash(){const p=new URLSearchParams({v:'1',fig:state.figure,tech:[...state.tech].join(','),mode:state.mode,node:state.node,from:state.from,to:state.to,labels:state.labels?'1':'0',scale:state.scale,energy:state.energy,x:state.x,y:state.y,xscale:state.xscale,pins:state.pins.join(',')});if(state.selected!==null)p.set('selected',state.selected);p.set('trends',state.trends?'1':'0');p.set('trendType',state.trendType);p.set('project',state.projectTrend?'1':'0');p.set('projectionYear',state.projectionYear);p.set('q',state.query);p.set('limits',JSON.stringify(state.limits));return '#'+p.toString();}
function restoreView(){
 const p=new URLSearchParams(location.hash.slice(1));if(p.get('v')!=='1')return;
 if(Object.hasOwn(figures,p.get('fig')))state.figure=p.get('fig');state.scale=figures[state.figure].scale;
 if(p.has('tech'))state.tech=new Set(p.get('tech').split(',').filter(t=>Object.hasOwn(colors,t)));
 if(['all','Digital','Analog'].includes(p.get('mode')))state.mode=p.get('mode');
 if(p.get('node')==='all'||data.some(d=>String(d.process_node_nm)===p.get('node')))state.node=p.get('node');
 for(const k of ['from','to'])if(data.some(d=>String(d.year)===p.get(k)))state[k]=Number(p.get(k));
 if(state.from>state.to)[state.from,state.to]=[state.to,state.from];
 restoreDiscovery(p);
 state.trends=p.get('trends')==='1';state.trendType=p.get('trendType')==='record'||(!p.has('trendType')&&p.get('trends')==='1')?'record':'fit';state.projectTrend=p.get('project')==='1';state.projectionYear=Math.max(2023,Math.min(2035,Number(p.get('projectionYear'))||2030));state.labels=p.get('labels')==='1';if(['log','linear'].includes(p.get('scale'))||(state.figure==='6b'&&p.get('scale')==='paper'))state.scale=p.get('scale');
 if(['raw','normalized'].includes(p.get('energy')))state.energy=p.get('energy');
 for(const k of ['x','y'])if(Object.hasOwn(metricLabels,p.get(k)))state[k]=p.get(k);
 if(['linear','log'].includes(p.get('xscale')))state.xscale=p.get('xscale');
 state.pins=[...new Set((p.get('pins')||'').split(',').map(Number).filter(id=>data.some(d=>d.source_row===id)))].slice(0,4);
 if(p.has('selected')&&data.some(d=>d.source_row===Number(p.get('selected'))))state.selected=Number(p.get('selected'));
}
function chooseFigureRestored(){document.querySelectorAll('[data-figure]').forEach(el=>{const active=el.dataset.figure===state.figure;el.classList.toggle('active',active);el.setAttribute('aria-selected',active);el.tabIndex=active?0:-1;});$('plot-view').setAttribute('aria-labelledby','tab-'+state.figure);syncControls();render();}
function syncStudio(){
 $('explore-controls').hidden=state.figure!=='custom';$('energy-controls').hidden=!['7b','pareto'].includes(state.figure);
 $('custom-x').value=state.x;$('custom-y').value=state.y;$('x-scale').value=state.xscale;$('energy-mode').value=state.energy;
 $('energy-formula').textContent=state.energy==='raw'?'Reported energy in fJ/bit/search. No layout normalization.':'Normalized energy = reported energy / k; k = area / (node in µm)².';
}
function renderStudio(){syncStudio();renderDiscovery();renderComparison();document.querySelectorAll('[data-pin]').forEach(b=>b.onclick=e=>{e.stopPropagation();togglePin(Number(b.dataset.pin));});history.replaceState(null,'',location.pathname+location.search+viewHash());}
function wireStudio(){
 wireDiscovery();
 $('custom-x').onchange=()=>{state.x=$('custom-x').value;render();};$('custom-y').onchange=()=>{state.y=$('custom-y').value;render();};$('x-scale').onchange=()=>{state.xscale=$('x-scale').value;render();};$('energy-mode').onchange=()=>{state.energy=$('energy-mode').value;render();};$('clear-pins').onclick=()=>{state.pins=[];render();};
 $('share-view').onclick=()=>{$('share-url').value=location.origin+location.pathname+location.search+viewHash();$('share-dialog').showModal();$('share-url').select();};
 $('close-share').onclick=()=>$('share-dialog').close();$('copy-link').onclick=async()=>{try{await navigator.clipboard.writeText($('share-url').value);tell('View link copied.');}catch(e){$('share-url').focus();$('share-url').select();tell('Select and copy the link above.');}};
 window.addEventListener('hashchange',()=>{restoreView();chooseFigureRestored();});
}
async function loadStudio(){
 figures.custom={scale:'log'};figures.pareto={scale:'log'};await loadDiscovery();
 const responses=await Promise.all(['conditions','schematics'].map(name=>fetch('p00_data/'+name+'.json').then(r=>{if(!r.ok)throw Error('Studio metadata unavailable');return r.json();})));
 [conditions,schematics]=responses;
 for(const id of ['custom-x','custom-y'])$(id).innerHTML=Object.entries(metricLabels).map(([value,label])=>`<option value="${value}">${label}</option>`).join('');
 $('schematic-cards').innerHTML=schematics.map(s=>`<figure><a href="${s.asset}" target="_blank" rel="noreferrer"><img loading="lazy" src="${s.asset}" alt="${esc(s.technology+' '+s.cell_configuration+' '+s.storage_type)} schematic"></a><figcaption><strong>${esc(s.technology)} · ${esc(s.cell_configuration)}</strong><span>${esc(s.storage_type)} · Citation key: ${esc(s.citation_key)}</span></figcaption></figure>`).join('');
}
