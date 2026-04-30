# Customer Success FTE - 24/7 AI Employee

A production-grade Digital FTE (Full-Time Equivalent) that handles customer support across multiple channels: Email (Gmail), WhatsApp, and Web Form.

## 🎯 Project Overview

This project implements the complete Agent Maturity Model:
- **Stage 1 - Incubation**: Prototype and discover requirements using Claude Code
- **Stage 2 - Specialization**: Production-grade Custom Agent with OpenAI Agents SDK

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    INTAKE LAYER                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │  Gmail   │  │ WhatsApp │  │ Web Form │                  │
│  │   API    │  │  Twilio  │  │  React   │                  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                  │
│       │             │              │                         │
│       └─────────────┴──────────────┘                         │
│                     │                                        │
│                     ▼                                        │
│            ┌─────────────────┐                              │
│            │ Unified Ticket  │                              │
│            │   Ingestion     │                              │
│            │    (Kafka)      │                              │
│            └────────┬────────┘                              │
│                     │                                        │
│                     ▼                                        │
│            ┌─────────────────┐     ┌──────────┐            │
│            │  Agent Worker   │────▶│PostgreSQL│            │
│            │  (OpenAI SDK)   │     │   (CRM)  │            │
│            └─────────────────┘     └──────────┘            │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

- Python 3.10+
- Node.js 18+ (for web form)
- PostgreSQL 16+ with pgvector extension
- Apache Kafka
- Docker & Kubernetes (for deployment)
- Gmail API credentials
- Twilio account (for WhatsApp)
- OpenAI API key

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Copy and configure environment variables
cp .env.example .env
# Edit .env with your actual credentials
```

### 2. Install Dependencies

```bash
# Python dependencies
pip install -r requirements.txt

# Web form dependencies
cd src/web-form
npm install
```

### 3. Database Setup

```bash
# Create database
createdb fte_db

# Run migrations
psql -d fte_db -f production/database/schema.sql

# Enable pgvector extension
psql -d fte_db -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### 4. Start Services

```bash
# Start Kafka (using Docker)
docker-compose up -d kafka zookeeper

# Start the API server
uvicorn production.api.main:app --reload --port 8000

# Start the message processor worker
python production/workers/message_processor.py

# Start the web form (in another terminal)
cd src/web-form
npm run dev
```

## 📁 Project Structure

```
hackathon-5/
├── context/                    # Incubation phase context
│   ├── company-profile.md
│   ├── product-docs.md
│   ├── sample-tickets.json
│   ├── escalation-rules.md
│   └── brand-voice.md
├── src/                        # Incubation prototypes
│   ├── channels/
│   ├── agent/
│   └── web-form/
├── production/                 # Production code
│   ├── agent/
│   │   ├── customer_success_agent.py
│   │   ├── tools.py
│   │   ├── prompts.py
│   │   └── formatters.py
│   ├── channels/
│   │   ├── gmail_handler.py
│   │   ├── whatsapp_handler.py
│   │   └── web_form_handler.py
│   ├── workers/
│   │   └── message_processor.py
│   ├── api/
│   │   └── main.py
│   ├── database/
│   │   ├── schema.sql
│   │   └── queries.py
│   └── tests/
├── k8s/                        # Kubernetes manifests
├── specs/                      # Requirements & specs
├── tests/                      # Test suites
├── .env                        # Environment variables
└── README.md
```

## 🔧 Configuration

### Required Environment Variables

See `.env` file for all configuration options. Key variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `POSTGRES_*`: Database connection details
- `KAFKA_BOOTSTRAP_SERVERS`: Kafka broker address
- `GMAIL_*`: Gmail API credentials
- `TWILIO_*`: Twilio/WhatsApp credentials

## 🧪 Testing

```bash
# Run unit tests
pytest production/tests/

# Run E2E tests
pytest production/tests/test_multichannel_e2e.py

# Run load tests
locust -f production/tests/load_test.py
```

## 📊 Monitoring

Access metrics at:
- Health check: `http://localhost:8000/health`
- Channel metrics: `http://localhost:8000/metrics/channels`

## 🚢 Deployment

### Local Development (Docker Compose)

```bash
docker-compose up
```

### Production (Kubernetes)

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Apply configurations
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml

# Deploy services
kubectl apply -f k8s/deployment-api.yaml
kubectl apply -f k8s/deployment-worker.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Enable autoscaling
kubectl apply -f k8s/hpa.yaml
```

## 📝 Development Workflow

### Phase 1: Incubation (Hours 1-16)

1. **Initial Exploration**: Analyze sample tickets and identify patterns
2. **Prototype Core Loop**: Build basic interaction handling
3. **Add Memory**: Implement conversation state tracking
4. **Build MCP Server**: Expose agent capabilities as tools
5. **Define Skills**: Formalize reusable agent capabilities

### Phase 2: Transition (Hours 15-18)

1. Extract discoveries from incubation
2. Map prototype to production architecture
3. Transform MCP tools to @function_tool
4. Formalize system prompts
5. Create transition test suite

### Phase 3: Specialization (Hours 17-40)

1. Implement PostgreSQL schema (CRM system)
2. Build channel integrations (Gmail, WhatsApp, Web Form)
3. Create OpenAI Agents SDK implementation
4. Build unified message processor
5. Set up Kafka event streaming
6. Create FastAPI service
7. Deploy to Kubernetes

### Phase 4: Testing (Hours 41-48)

1. Multi-channel E2E testing
2. Load testing
3. Documentation
4. 24-hour continuous operation test

## 🎯 Success Criteria

- ✅ Handles customer queries from all 3 channels
- ✅ Response time < 3 seconds (processing)
- ✅ Accuracy > 85% on test set
- ✅ Escalation rate < 20%
- ✅ Cross-channel customer identification > 95%
- ✅ 24/7 operation without downtime
- ✅ Survives pod restarts and scaling events

## 📚 Key Technologies

- **AI Framework**: OpenAI Agents SDK
- **API Framework**: FastAPI
- **Database**: PostgreSQL 16 with pgvector
- **Event Streaming**: Apache Kafka
- **Orchestration**: Kubernetes
- **Email**: Gmail API with Pub/Sub
- **Messaging**: Twilio WhatsApp API
- **Frontend**: React/Next.js (Web Form)

## 🔐 Security

- All credentials stored in environment variables
- Webhook signature validation (Twilio)
- Rate limiting enabled
- PII encryption in database
- Audit logging for compliance

## 📖 Documentation

- [Agent Maturity Model](https://agentfactory.panaversity.org/docs/General-Agents-Foundations/agent-factory-paradigm/the-2025-inflection-point#the-agent-maturity-model)
- [OpenAI Agents SDK](https://platform.openai.com/docs/agents)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Gmail API](https://developers.google.com/gmail/api)
- [Twilio WhatsApp](https://www.twilio.com/docs/whatsapp)

## 🤝 Contributing

This is a hackathon project. Follow the development workflow outlined above.

## 📄 License

MIT License - See LICENSE file for details

## 🆘 Support

For issues or questions:
1. Check the FAQ in the hackathon document
2. Review the troubleshooting guide
3. Contact the hackathon organizers

---

**Built with ❤️ for the CRM Digital FTE Factory Hackathon 5**
