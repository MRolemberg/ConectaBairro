// ConectaBairro PWA - Frontend Controller
let categorias = [];
let categoriaSelecionadaId = null;

// Registro do Service Worker para funcionalidade offline (PWA)
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/static/js/service-worker.js')
      .then(() => console.log('Service Worker registrado com sucesso.'))
      .catch((err) => console.warn('Erro ao registrar Service Worker:', err));
  });
}

document.addEventListener('DOMContentLoaded', () => {
  carregarCategorias();
  carregarPrestadores();
  configurarMascaraTelefone();
  configurarEventos();
});

function configurarEventos() {
  const formCadastro = document.getElementById('form-cadastro-prestador');
  if (formCadastro) {
    formCadastro.addEventListener('submit', submeterCadastro);
  }
}

// Tela 1: Carregamento de Categorias
async function carregarCategorias() {
  try {
    const res = await fetch('/api/vitrine/categorias');
    categorias = await res.json();
    const nav = document.getElementById('categories-nav');
    if (!nav) return;

    nav.innerHTML = `
      <button class="category-chip active" onclick="filtrarCategoria(null, this)" aria-label="Todas as categorias">
        Todas
      </button>
    `;

    const selectCategoria = document.getElementById('form-categoria');
    if (selectCategoria) selectCategoria.innerHTML = '<option value="">Selecione uma categoria</option>';

    categorias.forEach((cat) => {
      const chip = document.createElement('button');
      chip.className = 'category-chip';
      chip.textContent = cat.nome;
      chip.onclick = () => filtrarCategoria(cat.id, chip);
      chip.setAttribute('aria-label', `Filtrar por ${cat.nome}`);
      nav.appendChild(chip);

      if (selectCategoria) {
        const option = document.createElement('option');
        option.value = cat.id;
        option.textContent = cat.nome;
        selectCategoria.appendChild(option);
      }
    });
  } catch (err) {
    console.error('Erro ao carregar categorias:', err);
  }
}

// Tela 1: Filtro de Prestadores
function filtrarCategoria(id, el) {
  categoriaSelecionadaId = id;
  document.querySelectorAll('.category-chip').forEach(btn => btn.classList.remove('active'));
  if (el) el.classList.add('active');
  carregarPrestadores();
}

async function carregarPrestadores() {
  const listContainer = document.getElementById('prestadores-list');
  if (!listContainer) return;
  listContainer.innerHTML = '<p aria-live="polite">Carregando profissionais da comunidade...</p>';

  try {
    let url = '/api/vitrine/prestadores';
    if (categoriaSelecionadaId) {
      url += `?categoria_id=${categoriaSelecionadaId}`;
    }
    const res = await fetch(url);
    const prestadores = await res.json();

    if (!prestadores.length) {
      listContainer.innerHTML = '<p>Nenhum prestador encontrado para esta categoria no momento.</p>';
      return;
    }

    listContainer.innerHTML = '';
    prestadores.forEach((p) => {
      const card = document.createElement('article');
      card.className = 'card';
      card.innerHTML = `
        <div class="card-header">
          <h3 class="card-title">${p.nome}</h3>
          <span class="badge">${p.categoria ? p.categoria.nome : 'Geral'}</span>
        </div>
        <p class="card-desc">${p.descricao}</p>
        <button class="btn btn-primary" onclick="abrirConfirmacaoConexao(${p.id}, '${p.nome}', '${p.categoria ? p.categoria.nome : 'Geral'}')" aria-label="Contatar ${p.nome}">
          Solicitar Contato
        </button>
      `;
      listContainer.appendChild(card);
    });
  } catch (err) {
    listContainer.innerHTML = '<p>Erro ao conectar à vitrine. Tente novamente.</p>';
  }
}

// Tela 2: Auto-cadastro de Prestador
async function submeterCadastro(e) {
  e.preventDefault();
  const feedback = document.getElementById('cadastro-feedback');
  feedback.textContent = 'Enviando cadastro...';

  const payload = {
    nome: document.getElementById('form-nome').value,
    telefone: document.getElementById('form-telefone').value,
    categoria_id: parseInt(document.getElementById('form-categoria').value),
    descricao: document.getElementById('form-descricao').value
  };

  try {
    const res = await fetch('/api/prestadores', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok) {
      feedback.textContent = `Erro: ${data.detail || 'Verifique os dados informados.'}`;
      feedback.style.color = '#c62828';
      return;
    }

    feedback.textContent = 'Cadastro realizado com sucesso na vitrine da comunidade!';
    feedback.style.color = '#1b5e20';
    e.target.reset();
    setTimeout(() => {
      mostrarTela('vitrine');
      carregarPrestadores();
    }, 1500);
  } catch (err) {
    feedback.textContent = 'Erro ao processar requisição. Verifique sua conexão.';
    feedback.style.color = '#c62828';
  }
}

// Tela 3: Confirmação e Redundância Visual (RA01)
async function abrirConfirmacaoConexao(prestadorId, nome, categoria) {
  mostrarTela('conexao');
  const details = document.getElementById('conexao-detalhes');
  const btnWhatsapp = document.getElementById('btn-whatsapp-action');
  details.innerHTML = `<p>Preparando conexão com <strong>${nome}</strong> (${categoria})...</p>`;

  try {
    const res = await fetch('/api/conexao/iniciar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prestador_id: prestadorId })
    });
    const data = await res.json();

    details.innerHTML = `
      <p>Você selecionou <strong>${data.nome_prestador}</strong>.</p>
      <p>Clique no botão abaixo para iniciar a conversa direta no WhatsApp sem intermediários.</p>
    `;
    btnWhatsapp.href = data.whatsapp_url;
    btnWhatsapp.target = '_blank';
    btnWhatsapp.style.display = 'inline-flex';
  } catch (err) {
    details.innerHTML = '<p>Falha ao gerar link do WhatsApp. Tente novamente.</p>';
  }
}

// Navegação entre Telas
function mostrarTela(nome) {
  document.getElementById('secao-vitrine').style.display = nome === 'vitrine' ? 'block' : 'none';
  document.getElementById('secao-cadastro').style.display = nome === 'cadastro' ? 'block' : 'none';
  document.getElementById('secao-conexao').style.display = nome === 'conexao' ? 'block' : 'none';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Máscara de Telefone
function configurarMascaraTelefone() {
  const telInput = document.getElementById('form-telefone');
  if (!telInput) return;
  telInput.addEventListener('input', (e) => {
    let v = e.target.value.replace(/\D/g, '');
    if (v.length > 11) v = v.substring(0, 11);
    if (v.length > 10) {
      e.target.value = `(${v.substring(0, 2)}) ${v.substring(2, 7)}-${v.substring(7)}`;
    } else if (v.length > 6) {
      e.target.value = `(${v.substring(0, 2)}) ${v.substring(2, 6)}-${v.substring(6)}`;
    } else if (v.length > 2) {
      e.target.value = `(${v.substring(0, 2)}) ${v.substring(2)}`;
    } else {
      e.target.value = v;
    }
  });
}
