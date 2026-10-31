'use strict';

const STORAGE_KEY = 'daybreak:progress:v1';
const $ = (id) => document.getElementById(id);
const state = { topics: [], topicId: 'psychopathology', questions: [], index: 0, locked: false, history: readHistory() };
const icons = ['◎', '◇', '◈', '✣', '✧', '✹'];

function readHistory() {
  try {
    const data = JSON.parse(localStorage.getItem(STORAGE_KEY));
    return Array.isArray(data) ? data.filter(x => typeof x.topic_id === 'string' && typeof x.correct === 'boolean').slice(-10000) : [];
  } catch (_) { return []; }
}
function saveHistory() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state.history)); }
  catch (_) { announce('Progress cannot be stored in this browser.'); }
}
function announce(message) {
  const node = $('toast'); node.textContent = message;
  node.classList.add('visible');
  clearTimeout(announce.timer);
  announce.timer = setTimeout(() => node.classList.remove('visible'), 3500);
}
async function getJson(url, init) {
  const response = await fetch(url, init);
  if (!response.ok) throw new Error(`Server responded with ${response.status}`);
  return response.json();
}
function route(name) {
  ['overview', 'practice', 'insights'].forEach((item) => {
    $(`${item}-view`).classList.toggle('hidden', item !== name);
    document.querySelector(`[data-route="${item}"]`).classList.toggle('active', item === name);
  });
  $('breadcrumb-current').textContent = ({overview:'Overview',practice:'Practice room',insights:'My insights'})[name];
  if (name === 'insights') renderInsights();
  window.scrollTo({top:0,behavior:'smooth'});
}
function refreshStats() {
  const total = state.history.length;
  const correct = state.history.filter(x => x.correct).length;
  const accuracy = total ? `${Math.round(correct * 100 / total)}%` : '—';
  $('stat-answered').textContent = total;
  $('stat-accuracy').textContent = accuracy;
  $('stat-topics').textContent = state.topics.length;
  $('ins-answered').textContent = total;
  $('ins-correct').textContent = correct;
  $('ins-accuracy').textContent = accuracy;
}
function renderTopics() {
  const grid = $('topic-grid'); grid.replaceChildren();
  state.topics.forEach((topic, i) => {
    const button = document.createElement('button');
    button.type = 'button'; button.className = 'topic-card';
    const top = document.createElement('div');top.className='topic-card-top';
    const ico=document.createElement('span');ico.className=`topic-icon ${topic.tone}`;ico.textContent=icons[i] || '◈';
    const tag=document.createElement('span');tag.className='topic-tag';tag.textContent=topic.tag;
    top.append(ico,tag);
    const title=document.createElement('h3');title.textContent=topic.name;
    const short=document.createElement('p');short.textContent=topic.short;
    const bottom=document.createElement('div');bottom.className='topic-bottom';
    const left=document.createElement('span');left.textContent='2 sample questions';
    const arrow=document.createElement('span');arrow.className='topic-arrow';arrow.textContent='↗';
    bottom.append(left,arrow);button.append(top,title,short,bottom);
    button.addEventListener('click',()=>beginTopic(topic.id));grid.append(button);
  });
  const picker=$('topic-select');picker.replaceChildren();
  state.topics.forEach(topic=>{const opt=document.createElement('option');opt.value=topic.id;opt.textContent=topic.name;picker.append(opt);});
  picker.value=state.topicId;
}
async function beginTopic(id) {
  state.topicId = id;
  $('topic-select').value = id;
  route('practice');
  const area=$('question-area');area.replaceChildren();
  const loading=document.createElement('p');loading.className='loading';loading.textContent='Preparing your questions…';area.append(loading);
  try {
    const data = await getJson(`/api/questions?topic_id=${encodeURIComponent(id)}&count=2`);
    if (state.topicId !== id) return;
    state.questions=data.questions;state.index=0;state.locked=false;
    renderQuestion();
  } catch(err) {
    area.textContent='Could not load questions. Check the server and try again.';
    announce('Connection problem: please retry.');
  }
}
function renderQuestion() {
  const area = $('question-area'); area.replaceChildren();
  if (state.index >= state.questions.length) { renderComplete(); return; }
  const q = state.questions[state.index];state.locked=false;
  $('question-count').textContent=`QUESTION ${state.index+1} OF ${state.questions.length}`;
  $('progress-fill').style.width=`${state.index / state.questions.length * 100}%`;
  const meta=document.createElement('div');meta.className='question-meta';meta.textContent=`${q.difficulty.toUpperCase()} QUESTION`;
  const heading=document.createElement('h2');heading.className='question-prompt';heading.textContent=q.prompt;
  const choices=document.createElement('div');choices.className='options';
  q.choices.forEach((choice,index)=>{
    const btn=document.createElement('button');btn.type='button';btn.className='option';
    const letter=document.createElement('span');letter.className='option-letter';letter.textContent='ABCD'[index];
    const label=document.createElement('span');label.textContent=choice;btn.append(letter,label);
    btn.addEventListener('click',()=>answer(q,index,choices));choices.append(btn);
  });
  area.append(meta,heading,choices);
}
async function answer(q,index,choices) {
  if (state.locked) return;
  state.locked=true;
  [...choices.children].forEach(button=>button.disabled=true);
  try {
    const feedback=await getJson('/api/grade',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question_id:q.id,answer_index:index})});
    [...choices.children].forEach((button,i)=>{if(i===feedback.correct_index)button.classList.add('correct');else if(i===index)button.classList.add('wrong');});
    state.history.push({topic_id:q.topic_id,correct:feedback.correct});
    saveHistory();refreshStats();
    const box=document.createElement('div');box.className='feedback';
    const strong=document.createElement('strong');strong.textContent=feedback.correct?'Correct — well reasoned.':'Not quite — here is the reasoning.';
    const explanation=document.createElement('p');explanation.textContent=feedback.explanation;
    const actions=document.createElement('div');actions.className='next-row';
    const next=document.createElement('button');next.type='button';next.className='button button-primary';next.textContent=state.index+1>=state.questions.length?'View summary →':'Next question →';
    next.addEventListener('click',()=>{state.index++;renderQuestion();});
    actions.append(next);box.append(strong,explanation,actions);$('question-area').append(box);
    $('progress-fill').style.width=`${(state.index+1) / state.questions.length * 100}%`;
  } catch(err) {state.locked=false;[...choices.children].forEach(button=>button.disabled=false);announce('Answer was not recorded. Try again.');}
}
function renderComplete() {
  $('progress-fill').style.width='100%';$('question-count').textContent='SESSION COMPLETE';
  const area=$('question-area');area.replaceChildren();
  const meta=document.createElement('div');meta.className='question-meta';meta.textContent='PRACTICE COMPLETE';
  const heading=document.createElement('h2');heading.className='question-prompt';heading.textContent='You showed up. That matters.';
  const body=document.createElement('p');body.style.color='#b9c8da';body.style.lineHeight='1.8';body.textContent='Review your explanations and repeat this topic whenever you need. Each attempt will be recorded in your local insights.';
  const again=document.createElement('button');again.className='button button-primary';again.textContent='Practice again ↗';again.addEventListener('click',()=>beginTopic(state.topicId));
  const insights=document.createElement('button');insights.className='button button-outline';insights.style.marginLeft='12px';insights.textContent='View insights';insights.addEventListener('click',()=>route('insights'));
  area.append(meta,heading,body,again,insights);
}
function renderInsights() {
  refreshStats();
  const box=$('topic-performance');box.replaceChildren();
  state.topics.forEach(topic=>{
    const attempts=state.history.filter(x=>x.topic_id===topic.id);
    const correct=attempts.filter(x=>x.correct).length;
    const percent=attempts.length?Math.round(correct*100/attempts.length):0;
    const row=document.createElement('div');row.className='performance-row';
    const head=document.createElement('div');head.className='performance-row-head';
    const name=document.createElement('span');name.textContent=topic.name;
    const score=document.createElement('span');score.textContent=attempts.length?`${correct} / ${attempts.length} · ${percent}%`:'Not attempted';head.append(name,score);
    const bar=document.createElement('div');bar.className='performance-bar';const fill=document.createElement('div');fill.style.width=`${percent}%`;bar.append(fill);row.append(head,bar);box.append(row);
  });
}
async function init() {
  document.querySelectorAll('[data-route]').forEach(el=>el.addEventListener('click',()=>route(el.dataset.route)));
  $('start-practice').addEventListener('click',()=>beginTopic(state.topicId));
  $('all-topics').addEventListener('click',()=>document.getElementById('topic-grid').scrollIntoView({behavior:'smooth'}));
  $('topic-select').addEventListener('change',e=>beginTopic(e.target.value));
  $('reset-history').addEventListener('click',()=>{
    if(!window.confirm('Clear all locally saved DAYBREAK practice results?'))return;
    state.history=[];saveHistory();renderInsights();announce('Local demo progress cleared.');
  });
  try {const data=await getJson('/api/topics');state.topics=data.topics;renderTopics();refreshStats();}
  catch(err){$('topic-grid').textContent='Cannot connect to the question service. Run the Python server and refresh.';announce('Could not connect to the API.');}
}
document.addEventListener('DOMContentLoaded',init);
