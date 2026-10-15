# Localization — Odoo Brazil Hub

Coleção de módulos de localização fiscal para **Odoo 19.0**, mantida pelo
[Odoo Brazil Hub](https://github.com/odoo-brazil-hub). Fornece um framework
base de cálculo de impostos, integração com a biblioteca `tributus-engine`
(impostos brasileiros) e um motor de mapeamento de impostos por contexto
(país, estado, cidade, parceiro e tipo de produto).

---

## Módulos

| Módulo | Descrição | Depende de |
| --- | --- | --- |
| `l10n_tax_engine` | Framework base que conecta motores fiscais de localização ao mecanismo padrão de impostos do Odoo (hook em `_get_tax_details()` / `compute_taxes_with_localization()`). | `base`, `account`, `product` |
| `l10n_br_tax_engine` | Integra a biblioteca `tributus-engine` ao Odoo para cálculo de impostos brasileiros (ICMS, IPI, PIS, COFINS, FCP, IBS, CBS), com seleção de CST. | `l10n_tax_engine` + `tributus-engine` (Python) |
| `l10n_tax_mapper` | Permite controlar quais impostos são aplicados aos produtos conforme regras configuráveis (país, estado, cidade, grupo de países, parceiro e tipo de produto). | `base`, `account`, `product`, `contacts`, `base_address_extended` |
| `l10n_tax_sale` | Integra os *tax mappers* aos pedidos de venda, determinando automaticamente os impostos das linhas de venda. | `l10n_tax_mapper`, `sale` |

> `l10n_tax_sale` possui `auto_install=True`, ou seja, é instalado
> automaticamente quando `l10n_tax_mapper` e `sale` já estiverem presentes.

---

## Requisitos

- **Odoo 19.0** (Community ou Enterprise)
- **Python 3.10+**
- **PostgreSQL 12+**
- Acesso ao shell do servidor Odoo para instalar as dependências Python

---

## Dependências externas

Além dos módulos padrão do Odoo, este repositório possui **duas dependências
externas** que precisam ser instaladas/configuradas **antes** da instalação
dos módulos.

### 1. `tributus-engine` (Python — obrigatória para `l10n_br_tax_engine`)

Biblioteca de cálculo de impostos brasileiros. É declarada em
`external_dependencies` do módulo `l10n_br_tax_engine` e importada no código
como `tributus_engine`.

```bash
pip install tributus-engine
```

> Se a biblioteca não estiver instalada, o módulo ainda pode ser instalado,
> porém o cálculo brasileiro ficará indisponível: o código aplica *fallback*
> e registra um aviso no log.

### 2. `base_address_extended` (módulo OCA — obrigatória para `l10n_tax_mapper`)

Módulo da OCA que fornece o modelo `res.city` (utilizado nos filtros por
cidade). Não faz parte do Odoo padrão e deve ser obtido do repositório
[OCA/partner-contact](https://github.com/OCA/partner-contact):

```bash
git clone --branch 19.0 https://github.com/OCA/partner-contact.git \
    /mnt/extra_addons/partner-contact
```

Em seguida, adicione o caminho ao `addons_path` (ver abaixo).

---

## Instalação

### 1. Obtenha o código

```bash
git clone git@github.com:odoo-brazil-hub/localization.git /mnt/localization
```

Via HTTPS, caso não tenha chave SSH configurada:

```bash
git clone https://github.com/odoo-brazil-hub/localization.git /mnt/localization
```

### 2. Configure o `addons_path`

Edite o arquivo de configuração do Odoo (`odoo.conf`) e inclua os diretórios
dos módulos:

```ini
[options]
addons_path = /path/to/odoo/addons,/mnt/localization,/mnt/extra_addons/partner-contact
db_host = localhost
db_user = odoo
db_password = odoo
```

### 3. Instale as dependências Python

```bash
pip install tributus-engine
```

### 4. Instale os módulos

**Via interface web (recomendado):**

1. Ative o *Developer Mode* (**Configurações → Ativar o modo desenvolvedor**).
2. Vá em **Aplicativos → Atualizar Lista de Aplicativos**.
3. Procure e instale, **nesta ordem**:
   1. `Tax Engine (Base)` (`l10n_tax_engine`)
   2. `Brazilian Tax Engine` (`l10n_br_tax_engine`)
   3. `Tax Mapper` (`l10n_tax_mapper`)
   4. `Taxes - Sale Integration` (`l10n_tax_sale`)

**Via linha de comando:**

No Odoo 19 a CLI é baseada em subcomandos (`db`, `module`, `server`, ...). As
flags antigas (`-i`, `--stop-after-init`) foram substituídas:

```bash
# 1) Crie o banco de dados, caso ele ainda não exista
odoo db init -c /etc/odoo/odoo.conf <nome_do_banco>

# 2) Instale os módulos na ordem correta
odoo module install -c /etc/odoo/odoo.conf -d <nome_do_banco> \
    l10n_tax_engine l10n_br_tax_engine l10n_tax_mapper l10n_tax_sale
```

### Ordem de instalação

```
l10n_tax_engine  →  l10n_br_tax_engine
                 →  l10n_tax_mapper  →  l10n_tax_sale (auto_install)
```

O Odoo resolve as dependências automaticamente, mas a ordem acima reflete a
hierarquia correta dos módulos.

---

## Configuração pós-instalação

### Impostos brasileiros (Tributus)

Em **Contabilidade → Configuração → Impostos**, abra um imposto e localize o
grupo **Tributus Engine**:

- **Tax Engine Type**: `ICMS`, `IPI`, `PIS`, `COFINS`, `FCP`, `IBS` ou `CBS`.
- **ICMS CST**: código de situação tributária (obrigatório apenas quando o
  tipo é `ICMS`).

### Tax Mappers

Em **Contabilidade → Configuração → Tax Mappers** (visível para o grupo
*Account Manager*), crie regras com:

- **Used In**: *Sales* ou *Purchases*.
- **Product Type**: *Goods*, *Service*, *Combo* ou vazio (aplica-se a todos).
- **Mapper Lines**: filtros por país, estado, cidade, grupo de países e
  parceiro, além dos impostos a aplicar.

Depois, associe os mappers aos produtos: no formulário do produto, use os
campos **Sale Tax Mappers** (`sale_tax_tag_ids`) e **Purchase Tax Mappers**
(`purchase_tax_tag_ids`). Nas linhas de venda, os impostos são determinados
automaticamente com base nessas regras.

---

## Licença

Publicado sob a licença **LGPL-3**. Veja o arquivo `LICENSE` para mais
detalhes.

Part of Odoo Brazil Hub. See LICENSE file for full copyright and licensing
details.
