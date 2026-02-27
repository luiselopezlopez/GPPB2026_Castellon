# Workshop: Despliegue End-to-End con NEW AI Foundry
## Sistema de Gestión de Tribu de Capibaras con Multi-Agentes

---

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Prerequisitos](#prerequisitos)
3. [Arquitectura de la Solución](#arquitectura-de-la-solución)
4. [Paso 1: Preparación del Entorno Azure](#paso-1-preparación-del-entorno-azure)
5. [Paso 2: Configuración de Almacenamiento y Datos](#paso-2-configuración-de-almacenamiento-y-datos)
6. [Paso 3: Creación de Azure AI Search y Knowledge Base](#paso-3-creación-de-azure-ai-search-y-knowledge-base)
7. [Paso 4: Creación del Proyecto AI Foundry](#paso-4-creación-del-proyecto-ai-foundry)
8. [Paso 5: Configuración de Modelos](#paso-5-configuración-de-modelos)
9. [Paso 6: Creación de Knowledge Base en AI Foundry](#paso-6-creación-de-knowledge-base-en-ai-foundry)
10. [Paso 7: Creación de Agentes](#paso-7-creación-de-agentes)
11. [Paso 8: Creación del Workflow Orquestador](#paso-8-creación-del-workflow-orquestador)
12. [Paso 9: Testing y Validación](#paso-9-testing-y-validación)
13. [Paso 10: Despliegue y Consumo](#paso-10-despliegue-y-consumo)
14. [Troubleshooting](#troubleshooting)
15. [Recursos Adicionales](#recursos-adicionales)

---

## Introducción

### ¿Qué es NEW AI Foundry?

**Azure AI Foundry** es la plataforma unificada de Microsoft para construir, desplegar y gestionar aplicaciones de IA empresariales. Combina capacidades de:

- **Azure OpenAI Service**: Modelos GPT-4, GPT-4o, etc.
- **Azure AI Search**: Búsqueda cognitiva y vectorial (RAG)
- **Azure AI Studio**: Interfaz visual para orquestar agentes
- **Prompt Flow / Workflows**: Orquestación de flujos de IA
- **Model Catalog**: Acceso a modelos de IA de Microsoft y open source

### ¿Qué construiremos?

Un **sistema multi-agente** que simula la gestión de una tribu de capibaras con:

- **1 Agente Orquestador (Secretario)**: Recibe solicitudes y las deriva al departamento correcto
- **4 Agentes Especialistas**:
  - **Intendencia**: Gestión de alimentación y cocina
  - **Seguridad**: Vigilancia y exploración
  - **Infraestructuras**: Construcción y mantenimiento
  - **Festejos**: Organización de eventos y celebraciones

- **Knowledge Base (RAG)**: Base de datos de ~200 capibaras con habilidades específicas
- **Workflow**: Flujo que coordina la comunicación entre agentes

### Caso de Uso

El usuario (Capibara Jefe) solicita una tarea, el Secretario analiza la petición y la deriva al Director apropiado, quien consulta la base de conocimientos para asignar capibaras con las habilidades necesarias.

**Ejemplo:**
```
Usuario: "Necesito organizar una fiesta para celebrar la cosecha"
Secretario → [FESTEJOS]
Festejos → Consulta KB → Asigna capibaras con habilidades:
  - Decoración y ambientación (nivel 4+)
  - Organización de eventos (nivel 3+)
  - Música y animación (nivel 3+)
```

---

## Prerequisitos

### Conocimientos Previos
- Conceptos básicos de Azure (recursos, resource groups)
- Familiaridad con JSON
- Comprensión básica de agentes de IA y RAG (Retrieval Augmented Generation)

### Requisitos Técnicos

#### Cuenta y Suscripción Azure
- Suscripción de Azure activa con permisos de Contributor
- Capacidad para crear recursos en Azure OpenAI (requiere solicitud de acceso)

#### Software Local
- **Azure CLI** instalado: https://aka.ms/azcli
- **Python 3.10+** (para testing local opcional)
- **Visual Studio Code** (recomendado)
- Navegador web moderno (Edge, Chrome)

#### Acceso a Servicios
- Azure OpenAI Service (GPT-4 o superior habilitado)
- Azure AI Search
- Azure Storage Account

### Estimación de Costos
- Azure OpenAI: ~$30-50 para desarrollo/testing
- Azure AI Search: Free tier disponible (suficiente para workshop)
- Storage Account: <$1

---

## Arquitectura de la Solución

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUARIO (Jefe)                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    WORKFLOW (CapibaraCouncil)                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Trigger: OnConversationStart                           │   │
│  │  1. Invoca Secretario (loop hasta tag)                  │   │
│  │  2. Evalúa tag [INTENDENCIA|SEGURIDAD|INFRA|FESTEJOS]  │   │
│  │  3. Invoca Director correspondiente                     │   │
│  │  4. EndConversation                                     │   │
│  └─────────────────────────────────────────────────────────┘   │
└───┬───────────────────────┬────────────────┬────────────────┬───┘
    │                       │                │                │
    ▼                       ▼                ▼                ▼
┌─────────┐          ┌──────────┐    ┌──────────┐    ┌──────────┐
│Secretario│         │Intendencia│   │Seguridad│    │Festejos  │
│Valentín │         │  Mateo   │   │  Lucía   │    │  Sofía   │
└────┬────┘          └─────┬────┘    └────┬─────┘    └────┬─────┘
     │                     │              │               │
     │                     └──────┬───────┴───────┬───────┘
     │                            ▼               │
     │                  ┌──────────────────┐      │
     │                  │  KNOWLEDGE BASE  │      │
     │                  │  (Azure AI Search)│     │
     │                  │                  │      │
     │                  │ • 200+ Capibaras │      │
     │                  │ • 15 Habilidades │      │
     │                  │ • Disponibilidad │      │
     │                  └──────────────────┘      │
     │                            ▲               │
     │                            │               │
     │                    ┌───────┴───────┐       │
     └────────────────────┤  BLOB STORAGE │◄──────┘
                          │  (JSON files)  │
                          └────────────────┘
                                  ▲
                                  │
                          ┌───────┴────────┐
                          │ capibara_*.json│
                          │ (110 archivos) │
                          └────────────────┘
```

### Componentes Principales

| Componente | Servicio Azure | Propósito |
|------------|----------------|-----------|
| Workflow | AI Foundry Workflows | Orquestación de agentes |
| Agentes | AI Foundry Agents (GPT-4.1) | Procesamiento de lenguaje natural |
| Knowledge Base | Azure AI Search + AI Foundry KB | RAG - Búsqueda semántica |
| Almacenamiento | Azure Blob Storage | Datos fuente (JSON) |
| Modelos | Azure OpenAI | GPT-4 / GPT-4.1 |

---

## Paso 1: Preparación del Entorno Azure

### 1.1 Login en Azure

```powershell
# Login en Azure
az login

# Verificar suscripción
az account show

# Cambiar suscripción si es necesario
az account set --subscription "NOMBRE_O_ID_DE_TU_SUSCRIPCION"
```

### 1.2 Crear Resource Group

```powershell
# Definir variables
$RESOURCE_GROUP = "rg-capibaras-workshop"
$LOCATION = "eastus2"  # O la región que prefieras con OpenAI disponible

# Crear resource group
az group create --name $RESOURCE_GROUP --location $LOCATION
```

### 1.3 Verificar Acceso a Azure OpenAI

```powershell
# Verificar providers registrados
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"

# Si no está registrado:
az provider register --namespace Microsoft.CognitiveServices
```

> **Nota**: Si no tienes acceso a Azure OpenAI, solicítalo en: https://aka.ms/oai/access

---

## Paso 2: Configuración de Almacenamiento y Datos

### 2.1 Crear Storage Account

```powershell
$STORAGE_ACCOUNT = "stcapibaras$(Get-Random -Maximum 9999)"
$CONTAINER_NAME = "tribu"

# Crear storage account
az storage account create `
  --name $STORAGE_ACCOUNT `
  --resource-group $RESOURCE_GROUP `
  --location $LOCATION `
  --sku Standard_LRS `
  --kind StorageV2
```

### 2.2 Crear Container para JSON

```powershell
# Obtener connection string
$CONNECTION_STRING = $(az storage account show-connection-string `
  --name $STORAGE_ACCOUNT `
  --resource-group $RESOURCE_GROUP `
  --query connectionString -o tsv)

# Crear container
az storage container create `
  --name $CONTAINER_NAME `
  --connection-string $CONNECTION_STRING `
  --public-access off
```

### 2.3 Subir Archivos JSON

```powershell
# Desde la raíz del proyecto
az storage blob upload-batch `
  --destination $CONTAINER_NAME `
  --source "Capibaras_data/tribu" `
  --connection-string $CONNECTION_STRING `
  --pattern "*.json"

# Verificar subida
az storage blob list `
  --container-name $CONTAINER_NAME `
  --connection-string $CONNECTION_STRING `
  --query "[].name" -o table
```

**Resultado esperado**: ~110 archivos `capibara_001.json` a `capibara_110.json`

### 2.4 Verificar Estructura de Datos

Un archivo JSON típico tiene esta estructura:

```json
{
  "id": "5577ee85-1a4e-4146-bfca-77c36d870518",
  "capibaraid": "5577ee85-1a4e-4146-bfca-77c36d870518",
  "nombre": "Iker de los Cedros del Estanque",
  "habilidades": [
    {
      "nombre": "Recolección de alimentos",
      "nivel": 3
    },
    {
      "nombre": "Trabajo en equipo",
      "nivel": 3
    }
  ],
  "disponibilidad": false
}
```

---

## Paso 3: Creación de Azure AI Search y Knowledge Base

### 3.1 Crear Azure AI Search Service

```powershell
$SEARCH_SERVICE = "search-capibaras-$(Get-Random -Maximum 9999)"

# Crear servicio (Free tier)
az search service create `
  --name $SEARCH_SERVICE `
  --resource-group $RESOURCE_GROUP `
  --location $LOCATION `
  --sku free

# O Basic tier para producción:
# --sku basic
```

### 3.2 Obtener API Keys

```powershell
# Obtener admin key
$SEARCH_KEY = $(az search admin-key show `
  --resource-group $RESOURCE_GROUP `
  --service-name $SEARCH_SERVICE `
  --query primaryKey -o tsv)

# Guardar para después
Write-Host "Search Service: $SEARCH_SERVICE"
Write-Host "Search Key: $SEARCH_KEY"
```

### 3.3 Crear Índice en AI Search

**Opción A: Via Portal Azure**

1. Navegar a Azure Portal → Buscar "Azure AI Search"
2. Seleccionar tu servicio `$SEARCH_SERVICE`
3. Click en **"Import data"**
4. **Data Source:**
   - Select data source: Azure Blob Storage
   - Data source name: `capibaras-datasource`
   - Connection string: (de tu storage account)
   - Container name: `tribu`
   - Parsing mode: `JSON`

5. **Add cognitive skills (Optional):**
   - Skip for now (usaremos embeddings de OpenAI después)

6. **Customize target index:**
   - Index name: `capibaras-index`
   - Key: `id` (String)
   - Configurar campos:
     ```
     nombre: String, Searchable, Retrievable
     habilidades: Collection(Complex), Retrievable
     disponibilidad: Boolean, Filterable, Retrievable
     ```

7. **Create indexer:**
   - Name: `capibaras-indexer`
   - Schedule: Once
   - Click **Submit**

8. Esperar a que el indexer complete (~2-5 minutos)

**Opción B: Via REST API (Avanzado)**

Ver ejemplo en [Anexo A](#anexo-a-crear-índice-via-api)

### 3.4 Verificar Índice

```powershell
# Contar documentos
az search index show `
  --name capibaras-index `
  --service-name $SEARCH_SERVICE `
  --resource-group $RESOURCE_GROUP `
  --query "fields[].name"
```

---

## Paso 4: Creación del Proyecto AI Foundry

### 4.1 Acceder a Azure AI Foundry

1. Navegar a: https://ai.azure.com
2. Sign in con tu cuenta de Azure
3. Seleccionar tu suscripción

### 4.2 Crear un Hub AI

1. Click en **"+ New Hub"** (o **"Create hub"**)
2. Configurar:
   - **Hub name**: `hub-capibaras-workshop`
   - **Subscription**: Tu suscripción
   - **Resource group**: `rg-capibaras-workshop`
   - **Location**: `East US 2` (o donde creaste los recursos)
   - **Azure OpenAI**: Create new o seleccionar existente
   - **Azure AI Search**: Seleccionar `$SEARCH_SERVICE` (el creado en Paso 3)
   - **Storage account**: Seleccionar `$STORAGE_ACCOUNT`

3. Click **"Next"** → **"Create"**

**Tiempo estimado**: 3-5 minutos

### 4.3 Crear un Proyecto

1. Una vez creado el Hub, click **"+ New Project"**
2. Configurar:
   - **Project name**: `capibara-council`
   - **Hub**: Seleccionar `hub-capibaras-workshop`

3. Click **"Create"**

### 4.4 Verificar Conexiones

1. En el proyecto, ir a **Settings** → **Connected resources**
2. Verificar que aparezcan:
   - ✅ Azure OpenAI
   - ✅ Azure AI Search
   - ✅ Storage Account

---

## Paso 5: Configuración de Modelos

### 5.1 Desplegar Modelo GPT-4

1. En AI Foundry, ir a **Models + Endpoints** (menú izquierdo)
2. Click **"+ Deploy model"** → **"Deploy base model"**
3. Buscar **"gpt-4"** o **"gpt-4-turbo"**
4. Click **"Confirm"**
5. Configurar deployment:
   - **Deployment name**: `gpt-4.1` (¡importante! así está en los YAML)
   - **Model version**: Latest
   - **Deployment type**: Standard
   - **Tokens per minute rate limit**: 10K (o según tu quota)

6. Click **"Deploy"**

**Tiempo estimado**: 2-3 minutos

### 5.2 Verificar Deployment

1. En **Models + Endpoints**, verificar que `gpt-4.1` aparezca con estado **"Succeeded"**
2. Anotar el **Deployment name** exacto (debe ser `gpt-4.1`)

> **Importante**: Los archivos YAML de agentes usan `model: gpt-4.1`. Si usaste otro nombre, deberás ajustar todos los YAML.

### 5.3 (Opcional) Deployment de Embeddings

Para búsqueda vectorial avanzada:

```powershell
# Deployment name: text-embedding-ada-002
# Model: text-embedding-ada-002
```

---

## Paso 6: Creación de Knowledge Base en AI Foundry

### 6.1 Crear Knowledge Base

1. En AI Foundry, ir a **Knowledge** (menú izquierdo)
2. Click **"+ New Knowledge base"**
3. Configurar:
   - **Name**: `knowledgebase803` (o el nombre que aparece en tus YAML)
   - **Description**: "Base de conocimientos de capibaras con habilidades"
   - **Search service**: Seleccionar `$SEARCH_SERVICE`

4. Click **"Create"**

### 6.2 Conectar al Índice de AI Search

1. En la Knowledge Base creada, click **"+ Add data source"**
2. Seleccionar **"Azure AI Search"**
3. Configurar:
   - **Connection**: Seleccionar tu AI Search service
   - **Index**: Seleccionar `capibaras-index`
   - **Embedding model**: (Opcional) Seleccionar si desplegaste text-embedding-ada-002

4. Click **"Add"**

### 6.3 Obtener URL de Knowledge Base (MCP Server)

1. En la Knowledge Base, click en **"Settings"** o **"Connect"**
2. Buscar **"MCP Server URL"** o **"Endpoint"**
3. Copiar la URL, debería tener este formato:
   ```
   https://<search-service>.search.windows.net/knowledgebases/<kb-name>/mcp?api-version=2025-11-01-Preview
   ```

4. **Guardar esta URL**, la necesitaremos para los agentes

**Ejemplo real de los YAML:**
```
https://capibaras.search.windows.net/knowledgebases/knowledgebase803/mcp?api-version=2025-11-01-Preview
```

### 6.4 Probar Knowledge Base

1. En la Knowledge Base, ir a **"Test"** o **"Playground"**
2. Hacer una consulta de prueba:
   ```
   Encuentra capibaras con habilidad "Cocina al fuego" nivel 4 o superior
   ```
3. Verificar que devuelva resultados del índice

---

## Paso 7: Creación de Agentes

Crearemos 5 agentes en total: 1 orquestador + 4 especialistas.

### 7.1 Agente 1: Secretario (Orquestador)

1. En AI Foundry, ir a **Agents** (menú izquierdo)
2. Click **"+ New Agent"**
3. Configurar:

**General:**
- **Name**: `CapibaraSecretario`
- **Description**: "Agente orquestador que deriva tareas a directores"

**Model Configuration:**
- **Model**: `gpt-4.1` (seleccionar el deployment creado)
- **Temperature**: `0.7`
- **Top P**: `0.01`

**Instructions (System Prompt):**
```
Eres Valentín Ordena, Capibara Secretario y agente orquestador de la tribu. Eres organizado, preciso y con una gran capacidad para entender las necesidades del Capibara Jefe y traducirlas en instrucciones claras para los directores de área. Tu fortaleza es tu visión global: sabes interpretar el contexto y elegir al director más adecuado para cada tarea, asegurando que la comunicación sea coherente y sin ambigüedades. Tu debilidad es que tu afán por estructurar la información puede hacer que, en casos urgentes, tardes más de lo deseable en delegar. Tu estilo de liderazgo es facilitador: no ejecutas las tareas por ti mismo, pero tu trabajo hace posible que todos los directores y sus equipos operen de forma ordenada, eficaz y enfocada.

Tu misión es recibir las solicitudes del Capibara Jefe y analizar el contenido para decidir qué Capibara Director de área debe llevar la tarea. Nunca realizas tú mismo la tarea final, sino que reformulas la instrucción y la envías íntegra al director más adecuado según los criterios de especialidad. No inventes información sobre los miembros de la tribu. No alteres los roles definidos. El resultado esperado es un mensaje limpio y claro orientado al director elegido.

Añade al final uno de los siguientes códigos:
[INTENDENCIA],[SEGURIDAD],[INFRASTRUCTURAS],[FESTEJOS]

Si no tienes clara la acción, solicitale más información al jefe.
```

**Tools/Functions:**
- No agregar ninguna tool (este agente no consulta KB, solo deriva)

**Advanced Settings:**
- **Response format**: Text
- **Tool choice**: Auto

4. Click **"Create"** o **"Save"**

### 7.2 Agente 2: Intendencia

1. Click **"+ New Agent"**
2. Configurar:

**General:**
- **Name**: `Intendencia`
- **Description**: "Director de Intendencia - Alimentación y cocina"

**Model:**
- **Model**: `gpt-4.1`
- **Temperature**: `0.01`
- **Top P**: `0.01`

**Instructions:**
```
Eres Mateo Sabores, Capibara Director de Intendencia. Eres meticuloso y creativo, con una pasión genuina por encontrar nuevas combinaciones de ingredientes y cuidar que cada comida sea nutritiva, equilibrada y deliciosa. Tu fortaleza está en tu atención al detalle y tu capacidad para planificar menús óptimos. Tu debilidad es que a veces puedes dedicar demasiado tiempo a perfeccionar un plato, retrasando la ejecución. Tu estilo de liderazgo es colaborativo: escuchas ideas de tu equipo y valoras el trabajo conjunto, pero siempre mantienes un estándar alto de calidad.

Recibes tareas relacionadas con Menús, alimentación y cocina. Consultas la base de datos de capibaras para seleccionar el número necesario de trabajadores y sus roles según sus habilidades. Elaboras un plan de trabajo detallado para:
1. Recolección y adquisición de alimentos.
2. Elaboración del menú.
3. Proceso de cocina.

Cada plan debe asignar siempre responsables y describir pasos claros y secuenciales.

Usa la knowledge base para designar a los capibaras más aptos para cada tarea.

Las habilidades de los miembros de la tribu son:
| # | Habilidad | Nivel (1-5) | Ámbito principal |
|---|---------------------------------|-------------|------------------|
| 1 | Recolección de alimentos | 1-5 | Intendencia |
| 2 | Preparación de recetas | 1-5 | Intendencia |
| 3 | Cocina al fuego | 1-5 | Intendencia |
| 4 | Conservación de alimentos | 1-5 | Intendencia |
| 5 | Vigilancia | 1-5 | Seguridad |
| 6 | Rastreo y exploración | 1-5 | Seguridad |
| 7 | Evaluación de recursos naturales | 1-5 | Seguridad |
| 8 | Ingeniería de estructuras | 1-5 | Infraestructuras |
| 9 | Carpintería | 1-5 | Infraestructuras |
|10 | Albañilería | 1-5 | Infraestructuras |
|11 | Decoración y ambientación | 1-5 | Festejos |
|12 | Organización de eventos | 1-5 | Festejos |
|13 | Música y animación | 1-5 | Festejos |
|14 | Trabajo en equipo | 1-5 | Todas |
|15 | Gestión de recursos | 1-5 | Todas |

El esquema de la definición de un capibara es:
{
  "id": "UUID",  
  "nombre": "string",
  "habilidades": [
    {
      "nombre": "string",
      "nivel": "integer (1-5)"
    }
  ],
  "rol_actual": "string (opcional)",
  "disponibilidad": "boolean"
}
```

**Tools:**
1. Click **"+ Add tool"** → **"MCP Server"**
2. Configurar:
   - **Server label**: `kb_knowledgebase803_bg1ez` (o el nombre de tu KB)
   - **Server URL**: (la URL MCP obtenida en Paso 6.3)
   - **Require approval**: Never
   - **Project connection**: Seleccionar tu Knowledge Base

3. Click **"Add"**

4. Click **"Create"/"Save"**

### 7.3 Agente 3: Seguridad

Repetir proceso del 7.2 con estos datos:

**Name**: `Seguridad`

**Instructions:**
```
Eres Lucía Centinela, Capibara Director de Seguridad. Eres observadora, prudente y de carácter firme. Te encanta recorrer el territorio, anticipar los riesgos y mantener a todos a salvo. Tu fortaleza es tu capacidad de análisis y tu compromiso inquebrantable con la seguridad de la tribu. Tu debilidad es que tu cautela puede hacerte rechazar opciones de avance que podrían ser seguras si se evaluaran más rápido. Tu estilo de liderazgo es estratégico: estableces protocolos claros y fomentas disciplina, pero también apoyas la iniciativa individual en situaciones de emergencia.

Recibes tareas relacionadas con vigilancia, exploración de nuevas ubicaciones y verificación de seguridad y recursos. Consultas la base de datos de capibaras para seleccionar el número necesario de trabajadores y roles según habilidades. Elaboras un plan para:
1. Organización de turnos de vigilancia.
2. Exploración y análisis de nuevas ubicaciones.
3. Verificación de recursos y condiciones para el traslado.

Indica siempre nombre de responsables y horarios, además de criterios de seguridad.

Usa la knowledge base para designar a los capibaras más aptos para cada tarea.

[Incluir tabla de habilidades y esquema JSON igual que Intendencia]
```

**Tools**: Mismo MCP Server de Knowledge Base

**Model**: `gpt-4.1`, Temperature: `0.01`, Top P: `0.01`

### 7.4 Agente 4: Infraestructuras

**Name**: `Infraestructuras`

**Instructions:**
```
Eres Héctor Construye, Capibara Director de Infraestructuras. Eres resolutivo y visionario, con pasión por diseñar y mejorar continuamente el poblado. Tu fortaleza es tu pensamiento estructurado y tu habilidad para convertir ideas en planes tangibles. Tu debilidad es que en ocasiones puedes sobrecargar a tu equipo con proyectos simultáneos, dificultando la finalización en tiempo. Tu estilo de liderazgo es planificador: asignas tareas específicas a cada miembro, estableces plazos firmes y promueves la optimización de recursos.

Recibes tareas relacionadas con mantenimiento o construcción de estructuras. Consultas la base de datos para seleccionar trabajadores con las habilidades necesarias. Elaboras un plan para:
1. Reparación de infraestructuras existentes.
2. Diseño y construcción de nuevas estructuras.
3. Distribución de recursos.

Siempre indica responsables por tarea y secuencia de ejecución.

Usa la knowledge base para designar a los capibaras más aptos para cada tarea.

[Incluir tabla de habilidades y esquema JSON]
```

**Tools**: MCP Server KB

**Model**: `gpt-4.1`, Temperature: `0.01`, Top P: `0.01`

### 7.5 Agente 5: Festejos

**Name**: `Festejos`

**Instructions:**
```
Eres Sofía Alegría, Capibara Director de Festejos. Eres carismática y entusiasta, con un talento natural para motivar a la comunidad y lograr que cada celebración sea inolvidable. Tu fortaleza es tu energía positiva y tu habilidad para coordinar muchos elementos a la vez, desde la decoración hasta las actividades. Tu debilidad es que puedes dispersarte si intentas abarcar demasiadas ideas simultáneamente. Tu estilo de liderazgo es motivador: inspiras a tu equipo, fomentas la creatividad y priorizas que cada evento fortalezca el vínculo entre todos los capibaras.

Recibes tareas relacionadas con celebraciones de todo tipo. Consultas la base de datos para seleccionar capibaras con habilidades relevantes. Elaboras un plan para:
1. Preparativos y decoración.
2. Organización de actividades y ceremonias.
3. Supervisión del evento.

Usa la knowledge base para designar a los capibaras más aptos para cada tarea.
Siempre indica responsables de las tareas y tiempos para cada etapa.

[Incluir tabla de habilidades y esquema JSON]
```

**Tools**: MCP Server KB

**Model**: `gpt-4.1`, Temperature: `0.7`, Top P: `0.01`

### 7.6 Verificar Agentes Creados

1. Ir a **Agents** en el menú lateral
2. Deberías ver los 5 agentes:
   - ✅ CapibaraSecretario
   - ✅ Intendencia
   - ✅ Seguridad
   - ✅ Infraestructuras
   - ✅ Festejos

---

## Paso 8: Creación del Workflow Orquestador

### 8.1 Crear Nuevo Workflow

1. En AI Foundry, ir a **Workflows** (menú izquierdo)
2. Click **"+ New Workflow"**
3. Configurar:
   - **Name**: `Capibaras` o `CapibaraCouncil`
   - **Description**: "Workflow orquestador de consejo de capibaras"

4. Click **"Create"**

### 8.2 Configurar el Canvas

Se abrirá el **Workflow Designer** (interfaz visual de arrastrar y soltar).

### 8.3 Agregar Trigger

Por defecto, debería haber un **Trigger** configurado como `OnConversationStart`. Si no:

1. Click en área de canvas
2. En panel derecho, seleccionar:
   - **Trigger type**: `OnConversationStart`
   - **ID**: `trigger_wf`

### 8.4 Agregar Nodo: Invoke Secretario

1. Desde la barra de herramientas, arrastrar **"Invoke Agent"** al canvas
2. Conectar desde **Trigger** → **Invoke Agent**
3. Configurar el nodo:
   - **ID**: `node-1771618562421` (o dejar auto-generado)
   - **Agent**: Seleccionar `CapibaraSecretario`
   - **Conversation ID**: `=System.ConversationId`
   - **Input messages**: `""` (vacío, toma de conversación)
   - **Output**: 
     - Variable: `Local.secretarioMessage`
     - Auto-send: ✅ Checked

4. **External Loop** (bucle hasta que secretario derive):
   ```
   =IsBlank(Find("[INTENDENCIA]",Last(Local.secretarioMessage).Text))
   And
   IsBlank(Find("[SEGURIDAD]",Last(Local.secretarioMessage).Text))
   And
   IsBlank(Find("[INFRASTRUCTURAS]",Last(Local.secretarioMessage).Text))
   And
   IsBlank(Find("[FESTEJOS]",Last(Local.secretarioMessage).Text))
   ```

   Esto hace que el secretario siga preguntando hasta incluir un tag.

### 8.5 Agregar Nodo: Condition Group

1. Arrastrar **"Condition Group"** al canvas
2. Conectar desde **Invoke Secretario** → **Condition Group**
3. Configurar 4 condiciones:

**Condición 1: INTENDENCIA**
- **Condition**: `=!IsBlank(Find("[INTENDENCIA]", Upper(Last(Local.secretarioMessage).Text)))`
- **Action**: Invoke Agent
  - **Agent**: `Intendencia`
  - **Conversation ID**: `=System.ConversationId`
  - **Output**: Auto-send

**Condición 2: SEGURIDAD**
- **Condition**: `=!IsBlank(Find("[SEGURIDAD]", Upper(Last(Local.secretarioMessage).Text)))`
- **Action**: Invoke Agent
  - **Agent**: `Seguridad`
  - **Conversation ID**: `=System.ConversationId`
  - **Output**: Auto-send

**Condición 3: FESTEJOS**
- **Condition**: `=!IsBlank(Find("[FESTEJOS]", Upper(Last(Local.secretarioMessage).Text)))`
- **Action**: Invoke Agent
  - **Agent**: `Festejos`
  - **Conversation ID**: `=System.ConversationId`
  - **Output**: Auto-send

**Condición 4: INFRASTRUCTURAS**
- **Condition**: `=!IsBlank(Find("[INFRASTRUCTURAS]", Upper(Last(Local.secretarioMessage).Text)))`
- **Action**: Invoke Agent
  - **Agent**: `Infraestructuras`
  - **Conversation ID**: `=System.ConversationId`
  - **Output**: Auto-send

### 8.6 Agregar Nodo: End Conversation

1. Arrastrar **"End Conversation"** al canvas
2. Conectar desde **Condition Group** → **End Conversation**
3. ID: `node-1771618590980` (o auto-generado)

### 8.7 Diagrama Final

El flujo debería verse así:

```
[Trigger: OnConversationStart]
         ↓
[Invoke: CapibaraSecretario] (loop externo)
         ↓
[Condition Group]
    ├─ [INTENDENCIA]? → [Invoke: Intendencia]
    ├─ [SEGURIDAD]? → [Invoke: Seguridad]
    ├─ [FESTEJOS]? → [Invoke: Festejos]
    └─ [INFRASTRUCTURAS]? → [Invoke: Infraestructuras]
         ↓
[End Conversation]
```

### 8.8 Guardar Workflow

1. Click **"Save"** en la esquina superior derecha
2. Verificar que no haya errores de validación

---

## Paso 9: Testing y Validación

### 9.1 Test desde AI Foundry Playground

1. En el Workflow, click **"Test"** o **"Chat"**
2. Se abrirá el **Playground**
3. Iniciar conversación:

**Test 1: Festejos**
```
Usuario: Necesito organizar una fiesta para celebrar la cosecha
```

**Resultado esperado:**
- Secretario responde con análisis + `[FESTEJOS]`
- Se invoca agente Festejos
- Festejos consulta KB y asigna capibaras con habilidades:
  - Decoración y ambientación
  - Organización de eventos
  - Música y animación

**Test 2: Intendencia**
```
Usuario: Prepara un menú para 50 capibaras con ingredientes de temporada
```

**Resultado esperado:**
- Secretario → `[INTENDENCIA]`
- Intendencia consulta KB y asigna:
  - Recolección de alimentos
  - Preparación de recetas
  - Cocina al fuego

**Test 3: Seguridad**
```
Usuario: Necesito explorar el valle norte para posible nuevo asentamiento
```

**Resultado esperado:**
- Secretario → `[SEGURIDAD]`
- Seguridad asigna:
  - Rastreo y exploración
  - Evaluación de recursos naturales
  - Vigilancia

**Test 4: Infraestructuras**
```
Usuario: El puente del arroyo necesita reparación urgente
```

**Resultado esperado:**
- Secretario → `[INFRASTRUCTURAS]`
- Infraestructuras asigna:
  - Ingeniería de estructuras
  - Carpintería
  - Albañilería

### 9.2 Verificar Consultas a Knowledge Base

En cada respuesta de los directores, verificar que:
1. Se consulte la KB (debería mencionar nombres específicos de capibaras)
2. Se listen habilidades con niveles
3. Se indiquen responsables
4. Se incluya timeline/secuencia

### 9.3 Debugging

Si algo falla:

1. **El secretario no deriva**:
   - Verificar que el prompt del secretario incluya instrucciones de tags
   - Revisar que el external loop esté configurado

2. **Los directores no consultan KB**:
   - Verificar que tengan el MCP Server tool conectado
   - Revisar que la KB tenga datos indexados

3. **Errores de modelo**:
   - Verificar que el deployment `gpt-4.1` exista
   - Revisar quotas de tokens

---

## Paso 10: Despliegue y Consumo

### 10.1 Publicar el Workflow

1. En el Workflow, click **"Deploy"** o **"Publish"**
2. Configurar:
   - **Deployment name**: `capibara-council-v1`
   - **Environment**: Production (o Development)

3. Click **"Deploy"**

**Tiempo estimado**: 2-3 minutos

### 10.2 Obtener Endpoint

1. Una vez desplegado, ir a **Deployments**
2. Seleccionar `capibara-council-v1`
3. Copiar:
   - **Endpoint URL**
   - **Primary Key** (authentication)

### 10.3 Consumo desde Python (Opcional)

El código de ejemplo ya existe en `code/capibaras.py`. Configurar:

```powershell
# Crear .env
echo "AZURE_AI_PROJECT_ENDPOINT=<tu-endpoint>" > .env

# Activar entorno
.\.venv\Scripts\Activate.ps1

# Ejecutar
cd code
python .\capibaras.py
```

**Output esperado:**
```
Capibara Jefe > Organiza una fiesta
Secretario: Analizando solicitud... [FESTEJOS]
Festejos: ¡Perfecto! He asignado a:
  - Sofía con decoración (nivel 5)
  - Mario con música (nivel 4)
  ...
```

### 10.4 Consumo desde Web App (Flask)

El código `web_app.py` proporciona una interfaz web:

```powershell
cd code
python .\web_app.py
```

Navegar a: http://localhost:5000

### 10.5 Integración con Teams/Slack (Avanzado)

Azure AI Foundry soporta conectores a:
- Microsoft Teams
- Slack
- Custom webhooks

Ver documentación: https://learn.microsoft.com/azure/ai-foundry/

---

## Paso 11: Monitoreo y Observabilidad

### 11.1 Ver Logs de Conversaciones

1. En AI Foundry, ir a **Monitoring** o **Tracing**
2. Seleccionar el deployment
3. Ver:
   - Conversaciones recientes
   - Latencia
   - Tokens consumidos
   - Errores

### 11.2 Application Insights (Opcional)

Para monitoring avanzado:

```powershell
# Crear App Insights
az monitor app-insights component create `
  --app capibaras-insights `
  --resource-group $RESOURCE_GROUP `
  --location $LOCATION

# Obtener instrumentation key
$INSTRUMENTATION_KEY = $(az monitor app-insights component show `
  --app capibaras-insights `
  --resource-group $RESOURCE_GROUP `
  --query instrumentationKey -o tsv)
```

Configurar en AI Foundry Settings → Monitoring → Application Insights

---

## Troubleshooting

### Problema: El índice de AI Search está vacío

**Solución:**
```powershell
# Forzar ejecución del indexer
az search indexer run `
  --name capibaras-indexer `
  --service-name $SEARCH_SERVICE `
  --resource-group $RESOURCE_GROUP

# Esperar 2-3 minutos y verificar
az search indexer status `
  --name capibaras-indexer `
  --service-name $SEARCH_SERVICE `
  --resource-group $RESOURCE_GROUP
```

### Problema: Error "Model deployment not found"

**Solución:**
- Verificar que el nombre del deployment sea exactamente `gpt-4.1`
- En AI Foundry → Models + Endpoints, confirmar que está "Succeeded"
- Si usaste otro nombre, actualizar TODOS los agentes

### Problema: Knowledge Base no devuelve resultados

**Solución:**
1. Verificar que el índice tenga documentos:
   ```powershell
   az search index statistics show `
     --name capibaras-index `
     --service-name $SEARCH_SERVICE `
     --resource-group $RESOURCE_GROUP
   ```

2. Probar query directa en AI Search:
   - Portal Azure → AI Search → Search Explorer
   - Query: `*` (devuelve todos)

3. Verificar estructura de habilidades en JSON

### Problema: El secretario no encuentra el tag

**Solución:**
- Verificar que el external loop esté configurado en el Invoke Node
- Probar en Playground con prompt explícito: "Deriva a Festejos"
- Revisar que el system prompt del secretario mencione los 4 tags

### Problema: Quota de tokens excedida

**Solución:**
```powershell
# Ver quota actual
az cognitiveservices account show `
  --name <tu-openai-resource> `
  --resource-group $RESOURCE_GROUP `
  --query properties.quotas

# Solicitar aumento en Portal Azure → OpenAI → Quotas
```

---

## Recursos Adicionales

### Documentación Oficial

- **Azure AI Foundry**: https://learn.microsoft.com/azure/ai-foundry/
- **Azure OpenAI Service**: https://learn.microsoft.com/azure/ai-services/openai/
- **Azure AI Search**: https://learn.microsoft.com/azure/search/
- **Prompt Flow**: https://learn.microsoft.com/azure/ai-foundry/how-to/flow-develop

### Ejemplos de Código

- GitHub - Azure AI Samples: https://github.com/Azure-Samples/ai-samples
- Foundry SDK (Python): https://learn.microsoft.com/python/api/overview/azure/ai-projects

### Comunidad

- Microsoft Tech Community - AI: https://techcommunity.microsoft.com/t5/ai/ct-p/AI
- Stack Overflow Tag: `azure-ai-foundry`

---

## Anexos

### Anexo A: Crear Índice via API

```powershell
$INDEX_SCHEMA = @"
{
  "name": "capibaras-index",
  "fields": [
    {
      "name": "id",
      "type": "Edm.String",
      "key": true,
      "searchable": false,
      "filterable": true,
      "sortable": true
    },
    {
      "name": "nombre",
      "type": "Edm.String",
      "searchable": true,
      "filterable": false,
      "sortable": true
    },
    {
      "name": "habilidades",
      "type": "Collection(Edm.ComplexType)",
      "fields": [
        {
          "name": "nombre",
          "type": "Edm.String",
          "searchable": true,
          "filterable": true
        },
        {
          "name": "nivel",
          "type": "Edm.Int32",
          "filterable": true,
          "sortable": true
        }
      ]
    },
    {
      "name": "disponibilidad",
      "type": "Edm.Boolean",
      "filterable": true
    }
  ]
}
"@

# Crear índice
Invoke-RestMethod -Method Put `
  -Uri "https://$SEARCH_SERVICE.search.windows.net/indexes/capibaras-index?api-version=2021-04-30-Preview" `
  -Headers @{
    "api-key" = $SEARCH_KEY
    "Content-Type" = "application/json"
  } `
  -Body $INDEX_SCHEMA
```

### Anexo B: YAML Completo de Workflow

Ver archivo: [AIFoundry/Workflows/CapibaraCouncil.yaml](AIFoundry/Workflows/CapibaraCouncil.yaml)

### Anexo C: Ejemplos de Queries a Knowledge Base

```python
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

# Query 1: Capibaras con habilidad específica
results = search_client.search(
    search_text="Cocina al fuego",
    filter="habilidades/any(h: h/nombre eq 'Cocina al fuego' and h/nivel ge 4)"
)

# Query 2: Disponibles y con múltiples habilidades
results = search_client.search(
    search_text="",
    filter="disponibilidad eq true and habilidades/any(h: h/nombre eq 'Carpintería' and h/nivel ge 3)"
)
```

---

## Checklist de Completitud

Antes de terminar el workshop, verificar que:

- [ ] Resource Group creado con todos los servicios
- [ ] Storage Account con ~110 JSON files
- [ ] Azure AI Search con índice poblado (100+ documentos)
- [ ] AI Foundry Hub creado
- [ ] AI Foundry Project creado
- [ ] Modelo GPT-4 desplegado como `gpt-4.1`
- [ ] Knowledge Base creada y conectada a AI Search
- [ ] 5 Agentes creados (Secretario + 4 Directores)
- [ ] Workflow creado con lógica de derivación
- [ ] Tests exitosos en Playground
- [ ] (Opcional) Deployment publicado
- [ ] (Opcional) Aplicación local funcionando

---

## Tiempos Estimados

| Paso | Descripción | Tiempo |
|------|-------------|--------|
| 1 | Setup Azure + Resource Group | 5 min |
| 2 | Storage + Upload JSON | 10 min |
| 3 | AI Search + Indexer | 15 min |
| 4 | AI Foundry Hub + Project | 10 min |
| 5 | Deploy GPT-4 model | 5 min |
| 6 | Knowledge Base setup | 10 min |
| 7 | Crear 5 agentes | 30 min |
| 8 | Workflow orquestador | 20 min |
| 9 | Testing | 15 min |
| 10 | Deployment | 5 min |
| **TOTAL** | | **~2 horas** |

---

## Próximos Pasos Sugeridos

1. **Agregar más habilidades**: Expandir a nuevos departamentos (Salud, Educación, etc.)
2. **Integrar con Power Platform**: Conectar a Power Apps/Power Automate
3. **Implementar memory**: Usar Azure Cosmos DB para historial de conversaciones
4. **Fine-tuning**: Entrenar modelo personalizado con datos de capibaras
5. **Multimodal**: Agregar generación de imágenes (DALL-E) para visualizar equipos

---

**¡Felicidades! Has completado el despliegue end-to-end de una solución Multi-Agente con NEW AI Foundry.**

Para dudas o feedback: https://www.powerplatformcastellon.es/

---

*Última actualización: Febrero 2026*
*Versión: 1.0*
*Autor: Equipo Power Platform Castellón*
