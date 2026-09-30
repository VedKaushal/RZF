(() => {
  const sidebar = document.querySelector('#zero-sidebar');
  sidebar.querySelectorAll('.zero-toggle').forEach(button => button.addEventListener('click', () => {
    const open = button.getAttribute('aria-expanded') === 'true';
    button.setAttribute('aria-expanded', String(!open));
    document.getElementById(button.getAttribute('aria-controls')).hidden = open;
  }));
  const mobile = document.querySelector('#zero-mobile');
  const shade = document.querySelector('#zero-shade');
  function menu(open) {
    document.body.classList.toggle('zero-menu-open', open);
    mobile.setAttribute('aria-expanded', String(open));
    mobile.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    shade.hidden = !open;
    if (open) sidebar.querySelector('a').focus();
  }
  mobile.addEventListener('click', () => menu(!document.body.classList.contains('zero-menu-open')));
  shade.addEventListener('click', () => {menu(false);mobile.focus();});
  document.addEventListener('keydown', e => {if(e.key === 'Escape') menu(false);});
  document.querySelectorAll('[aria-label="Scroll down"]').forEach(button => {
    const scroll = () => button.closest('section').nextElementSibling?.scrollIntoView({behavior:'smooth'});
    button.addEventListener('click', scroll);
    button.addEventListener('keydown', e => {if(e.key==='Enter'||e.key===' '){e.preventDefault();scroll();}});
  });
  const dialog = document.querySelector('#zero-search');
  const query = document.querySelector('#zero-query');
  const results = document.querySelector('#zero-results');
  let entries;
  async function search() {
    results.replaceChildren();
    if(!entries){results.textContent='Loading archive…';return;}
    const words = query.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
    const matches = entries.filter(p=>words.every(word=>(p.title+' '+p.text).toLocaleLowerCase().includes(word)));
    if(!matches.length){results.textContent='No matching pages.';return;}
    for(const p of matches){
      const a=document.createElement('a');
      a.href=document.body.dataset.root+p.slug+'/';
      const title=document.createElement('strong');title.textContent=p.title;a.append(title);
      const detail=document.createElement('small');detail.textContent=p.text.slice(0,155)+(p.text.length>155?'…':'');a.append(detail);
      results.append(a);
    }
  }
  document.querySelector('#zero-search-open').addEventListener('click', async()=>{
    dialog.showModal();query.focus();search();
    if(!entries){try{const response=await fetch(document.body.dataset.root+'search.json');if(!response.ok)throw new Error();entries=await response.json();search();}catch{results.textContent='Search could not load. You can still browse every page in the left menu.';}}
  });
  query.addEventListener('input', search);
})();
