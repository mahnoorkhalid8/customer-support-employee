-- =============================================================================
-- CUSTOMER SUCCESS FTE - DATABASE SCHEMA
-- =============================================================================
-- PostgreSQL 16+ with pgvector extension
-- This schema serves as your complete CRM/ticket management system
-- =============================================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- =============================================================================
-- CUSTOMERS TABLE (Unified Customer Database)
-- =============================================================================
CREATE TABLE IF NOT EXISTS customers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(50),
    name VARCHAR(255),
    company VARCHAR(255),
    plan_type VARCHAR(50) DEFAULT 'starter', -- starter, professional, enterprise
    is_vip BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_contact_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}'::jsonb,

    CONSTRAINT customers_email_or_phone_required CHECK (email IS NOT NULL OR phone IS NOT NULL)
);

-- =============================================================================
-- CUSTOMER IDENTIFIERS (Cross-Channel Matching)
-- =============================================================================
CREATE TABLE IF NOT EXISTS customer_identifiers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    identifier_type VARCHAR(50) NOT NULL, -- 'email', 'phone', 'whatsapp'
    identifier_value VARCHAR(255) NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    UNIQUE(identifier_type, identifier_value)
);

-- =============================================================================
-- CONVERSATIONS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    initial_channel VARCHAR(50) NOT NULL, -- 'email', 'whatsapp', 'web_form'
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(50) DEFAULT 'active', -- active, resolved, escalated, closed
    sentiment_score DECIMAL(3,2), -- -1.00 to 1.00
    resolution_type VARCHAR(50), -- solved, escalated, abandoned
    escalated_to VARCHAR(255),
    escalation_reason TEXT,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- =============================================================================
-- MESSAGES TABLE (All Channel Messages)
-- =============================================================================
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    channel VARCHAR(50) NOT NULL, -- 'email', 'whatsapp', 'web_form'
    direction VARCHAR(20) NOT NULL, -- 'inbound', 'outbound'
    role VARCHAR(20) NOT NULL, -- 'customer', 'agent', 'system'
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    tokens_used INTEGER,
    latency_ms INTEGER,
    tool_calls JSONB DEFAULT '[]'::jsonb,
    channel_message_id VARCHAR(255), -- External ID (Gmail message ID, Twilio SID)
    delivery_status VARCHAR(50) DEFAULT 'pending', -- pending, sent, delivered, failed, read
    error_message TEXT,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- =============================================================================
-- TICKETS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS tickets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
    customer_id UUID NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    source_channel VARCHAR(50) NOT NULL,
    subject VARCHAR(500),
    category VARCHAR(100), -- account, technical, billing, feature_request, bug_report, etc.
    priority VARCHAR(20) DEFAULT 'medium', -- low, medium, high, critical
    status VARCHAR(50) DEFAULT 'open', -- open, in_progress, resolved, escalated, closed
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolution_notes TEXT,
    assigned_to VARCHAR(255),
    tags TEXT[],
    metadata JSONB DEFAULT '{}'::jsonb
);

-- =============================================================================
-- KNOWLEDGE BASE TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS knowledge_base (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    embedding VECTOR(1536), -- OpenAI text-embedding-3-small dimension
    keywords TEXT[],
    source_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_used_at TIMESTAMP WITH TIME ZONE,
    usage_count INTEGER DEFAULT 0,
    effectiveness_score DECIMAL(3,2), -- How helpful this content is
    metadata JSONB DEFAULT '{}'::jsonb
);

-- =============================================================================
-- CHANNEL CONFIGURATIONS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS channel_configs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    channel VARCHAR(50) UNIQUE NOT NULL,
    enabled BOOLEAN DEFAULT TRUE,
    config JSONB NOT NULL, -- API keys, webhook URLs, etc.
    response_template TEXT,
    max_response_length INTEGER,
    auto_response_enabled BOOLEAN DEFAULT TRUE,
    rate_limit_per_minute INTEGER DEFAULT 60,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================================
-- AGENT METRICS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS agent_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,4) NOT NULL,
    channel VARCHAR(50),
    dimensions JSONB DEFAULT '{}'::jsonb,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================================
-- ESCALATIONS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS escalations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ticket_id UUID NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
    reason VARCHAR(255) NOT NULL,
    urgency VARCHAR(20) DEFAULT 'normal', -- normal, high, critical
    escalated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    assigned_to VARCHAR(255),
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolution_notes TEXT,
    status VARCHAR(50) DEFAULT 'pending', -- pending, in_progress, resolved
    metadata JSONB DEFAULT '{}'::jsonb
);

-- =============================================================================
-- AUDIT LOG TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_type VARCHAR(50) NOT NULL, -- customer, ticket, conversation, etc.
    entity_id UUID NOT NULL,
    action VARCHAR(50) NOT NULL, -- created, updated, deleted, escalated
    actor VARCHAR(255), -- user_id or 'system' or 'ai_agent'
    changes JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================================
-- INDEXES FOR PERFORMANCE
-- =============================================================================

-- Customers
CREATE INDEX idx_customers_email ON customers(email) WHERE email IS NOT NULL;
CREATE INDEX idx_customers_phone ON customers(phone) WHERE phone IS NOT NULL;
CREATE INDEX idx_customers_plan_type ON customers(plan_type);
CREATE INDEX idx_customers_is_vip ON customers(is_vip) WHERE is_vip = TRUE;

-- Customer Identifiers
CREATE INDEX idx_customer_identifiers_customer_id ON customer_identifiers(customer_id);
CREATE INDEX idx_customer_identifiers_value ON customer_identifiers(identifier_value);

-- Conversations
CREATE INDEX idx_conversations_customer_id ON conversations(customer_id);
CREATE INDEX idx_conversations_status ON conversations(status);
CREATE INDEX idx_conversations_channel ON conversations(initial_channel);
CREATE INDEX idx_conversations_started_at ON conversations(started_at DESC);
CREATE INDEX idx_conversations_active ON conversations(customer_id, status) WHERE status = 'active';

-- Messages
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_channel ON messages(channel);
CREATE INDEX idx_messages_created_at ON messages(created_at DESC);
CREATE INDEX idx_messages_channel_message_id ON messages(channel_message_id) WHERE channel_message_id IS NOT NULL;

-- Tickets
CREATE INDEX idx_tickets_customer_id ON tickets(customer_id);
CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_priority ON tickets(priority);
CREATE INDEX idx_tickets_channel ON tickets(source_channel);
CREATE INDEX idx_tickets_category ON tickets(category);
CREATE INDEX idx_tickets_created_at ON tickets(created_at DESC);
CREATE INDEX idx_tickets_open ON tickets(status) WHERE status IN ('open', 'in_progress');

-- Knowledge Base
CREATE INDEX idx_knowledge_base_category ON knowledge_base(category);
CREATE INDEX idx_knowledge_base_keywords ON knowledge_base USING GIN(keywords);
CREATE INDEX idx_knowledge_base_embedding ON knowledge_base USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Escalations
CREATE INDEX idx_escalations_ticket_id ON escalations(ticket_id);
CREATE INDEX idx_escalations_status ON escalations(status);
CREATE INDEX idx_escalations_urgency ON escalations(urgency);
CREATE INDEX idx_escalations_pending ON escalations(status) WHERE status = 'pending';

-- Audit Log
CREATE INDEX idx_audit_log_entity ON audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_log_created_at ON audit_log(created_at DESC);

-- =============================================================================
-- FUNCTIONS AND TRIGGERS
-- =============================================================================

-- Update updated_at timestamp automatically
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to relevant tables
CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON customers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tickets_updated_at BEFORE UPDATE ON tickets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_knowledge_base_updated_at BEFORE UPDATE ON knowledge_base
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Update customer last_contact_at when new message arrives
CREATE OR REPLACE FUNCTION update_customer_last_contact()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE customers
    SET last_contact_at = NEW.created_at
    WHERE id = (
        SELECT customer_id FROM conversations WHERE id = NEW.conversation_id
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_customer_last_contact_trigger
    AFTER INSERT ON messages
    FOR EACH ROW
    WHEN (NEW.direction = 'inbound')
    EXECUTE FUNCTION update_customer_last_contact();

-- =============================================================================
-- INITIAL DATA
-- =============================================================================

-- Insert default channel configurations
INSERT INTO channel_configs (channel, enabled, config, max_response_length) VALUES
    ('email', true, '{"format": "formal"}'::jsonb, 2000),
    ('whatsapp', true, '{"format": "conversational"}'::jsonb, 1600),
    ('web_form', true, '{"format": "semi-formal"}'::jsonb, 1000)
ON CONFLICT (channel) DO NOTHING;

-- =============================================================================
-- VIEWS FOR COMMON QUERIES
-- =============================================================================

-- Active conversations with customer info
CREATE OR REPLACE VIEW active_conversations_view AS
SELECT
    c.id as conversation_id,
    c.customer_id,
    cu.email,
    cu.name,
    cu.plan_type,
    c.initial_channel,
    c.started_at,
    c.sentiment_score,
    COUNT(m.id) as message_count,
    MAX(m.created_at) as last_message_at
FROM conversations c
JOIN customers cu ON c.customer_id = cu.id
LEFT JOIN messages m ON c.id = m.conversation_id
WHERE c.status = 'active'
GROUP BY c.id, c.customer_id, cu.email, cu.name, cu.plan_type, c.initial_channel, c.started_at, c.sentiment_score;

-- Open tickets summary
CREATE OR REPLACE VIEW open_tickets_view AS
SELECT
    t.id as ticket_id,
    t.customer_id,
    cu.email,
    cu.name,
    t.subject,
    t.category,
    t.priority,
    t.source_channel,
    t.created_at,
    EXTRACT(EPOCH FROM (NOW() - t.created_at))/3600 as age_hours
FROM tickets t
JOIN customers cu ON t.customer_id = cu.id
WHERE t.status IN ('open', 'in_progress')
ORDER BY t.priority DESC, t.created_at ASC;

-- Channel performance metrics
CREATE OR REPLACE VIEW channel_metrics_view AS
SELECT
    c.initial_channel as channel,
    COUNT(DISTINCT c.id) as total_conversations,
    COUNT(DISTINCT CASE WHEN c.status = 'resolved' THEN c.id END) as resolved_count,
    COUNT(DISTINCT CASE WHEN c.status = 'escalated' THEN c.id END) as escalated_count,
    AVG(c.sentiment_score) as avg_sentiment,
    AVG(EXTRACT(EPOCH FROM (c.ended_at - c.started_at))/60) as avg_duration_minutes
FROM conversations c
WHERE c.started_at > NOW() - INTERVAL '24 hours'
GROUP BY c.initial_channel;

-- =============================================================================
-- GRANTS (adjust based on your user setup)
-- =============================================================================

-- Grant permissions to application user
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO fte_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO fte_user;
-- GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO fte_user;

-- =============================================================================
-- COMMENTS FOR DOCUMENTATION
-- =============================================================================

COMMENT ON TABLE customers IS 'Unified customer database across all channels';
COMMENT ON TABLE customer_identifiers IS 'Maps multiple identifiers (email, phone) to single customer';
COMMENT ON TABLE conversations IS 'Conversation threads with customers';
COMMENT ON TABLE messages IS 'Individual messages within conversations';
COMMENT ON TABLE tickets IS 'Support tickets for tracking and resolution';
COMMENT ON TABLE knowledge_base IS 'Product documentation with vector embeddings for semantic search';
COMMENT ON TABLE escalations IS 'Escalated issues requiring human intervention';
COMMENT ON COLUMN knowledge_base.embedding IS 'Vector embedding for semantic similarity search (1536 dimensions for text-embedding-3-small)';
COMMENT ON COLUMN conversations.sentiment_score IS 'Overall sentiment score from -1.00 (very negative) to 1.00 (very positive)';

-- =============================================================================
-- END OF SCHEMA
-- =============================================================================
