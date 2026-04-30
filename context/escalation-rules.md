# Escalation Rules - Customer Success FTE

## When to Escalate to Human Support

### Automatic Escalation Triggers

#### 1. Pricing & Financial Matters
**Trigger:** Customer asks about pricing, discounts, refunds, or billing disputes
**Keywords:** price, cost, discount, refund, billing, invoice, payment, charge
**Reason:** Financial decisions require human approval
**Urgency:** Normal
**Example:**
- "How much does the Enterprise plan cost?"
- "I want a refund for last month"
- "Can you give me a discount?"

#### 2. Legal & Compliance
**Trigger:** Customer mentions legal action or compliance requirements
**Keywords:** lawyer, legal, sue, attorney, GDPR, HIPAA, compliance, regulation
**Reason:** Legal matters require specialized handling
**Urgency:** High
**Example:**
- "I'm going to contact my lawyer about this"
- "We need GDPR compliance documentation"
- "This violates our contract"

#### 3. Negative Sentiment
**Trigger:** Sentiment score < 0.3 or aggressive language
**Keywords:** terrible, awful, worst, hate, angry, frustrated, disappointed
**Reason:** Upset customers need empathetic human touch
**Urgency:** High
**Example:**
- "This is RIDICULOUS! Your product is BROKEN!"
- "I'm extremely frustrated with your service"
- "Worst experience ever"

#### 4. Account Termination
**Trigger:** Customer wants to cancel or delete account
**Keywords:** cancel, delete account, close account, terminate, unsubscribe
**Reason:** Retention opportunity for sales team
**Urgency:** High
**Example:**
- "I want to cancel my subscription"
- "Please delete my account"
- "How do I close my account?"

#### 5. Data Loss or Security Issues
**Trigger:** Customer reports data loss, security breach, or unauthorized access
**Keywords:** data loss, deleted files, hacked, security breach, unauthorized access
**Reason:** Critical issues requiring immediate attention
**Urgency:** Critical
**Example:**
- "All my files are missing!"
- "Someone accessed my account without permission"
- "I think we've been hacked"

#### 6. Complex Technical Issues
**Trigger:** Cannot find solution after 2 knowledge base searches
**Reason:** Issue beyond AI's knowledge
**Urgency:** Normal
**Example:**
- Custom integration problems
- Advanced API usage
- System architecture questions

#### 7. Explicit Human Request
**Trigger:** Customer explicitly asks for human support
**Keywords:** human, agent, representative, person, speak to someone, real person
**Reason:** Customer preference
**Urgency:** Normal
**Example:**
- "Can I speak to a human?"
- "I need to talk to a real person"
- "Connect me with an agent"

#### 8. VIP Customers
**Trigger:** Customer is on Enterprise plan or flagged as VIP
**Reason:** Premium service level
**Urgency:** High
**Example:**
- Enterprise plan customers
- High-value accounts
- Strategic partners

## Escalation Workflow

### Step 1: Identify Trigger
- Check message content against trigger keywords
- Analyze sentiment score
- Review customer history and account type

### Step 2: Create Escalation Ticket
- Mark ticket as "escalated" in database
- Include full conversation context
- Add escalation reason and urgency level
- Tag with appropriate category

### Step 3: Notify Human Team
- Send to appropriate Slack channel based on category:
  - #support-escalations (general)
  - #billing-escalations (financial)
  - #legal-escalations (legal matters)
  - #vip-support (VIP customers)
- Email notification to on-call support agent
- Update ticket status in CRM

### Step 4: Inform Customer
- Acknowledge the escalation
- Set expectations for response time
- Provide ticket reference number
- Offer alternative contact methods if urgent

## Response Templates

### General Escalation
```
I understand this requires specialized attention. I've escalated your request to our support team, and a human agent will reach out to you within [timeframe].

Your ticket reference: [TICKET_ID]

For urgent matters, you can also reach us at:
- Email: support@techcorp.com
- WhatsApp: +1 (555) 123-4567
```

### Pricing Inquiry
```
Thank you for your interest in our pricing. I've forwarded your inquiry to our sales team, who can provide detailed pricing information and discuss options that best fit your needs.

A sales representative will contact you within 24 hours.

Ticket reference: [TICKET_ID]
```

### Negative Sentiment
```
I sincerely apologize for the frustration you're experiencing. Your concern is important to us, and I've escalated this to our senior support team for immediate attention.

A support manager will reach out to you within 2 hours to resolve this issue.

Ticket reference: [TICKET_ID]
```

### Legal Matter
```
I understand the seriousness of your concern. I've immediately escalated this to our legal and compliance team.

A representative will contact you within 4 business hours.

Ticket reference: [TICKET_ID]
```

### Data Loss/Security
```
I understand how concerning this is. I've marked this as a critical issue and escalated it to our security team immediately.

A security specialist will contact you within 1 hour.

In the meantime, please:
1. Change your password immediately
2. Review recent account activity
3. Do not share your credentials

Ticket reference: [TICKET_ID]
```

## Do NOT Escalate

### Issues AI Can Handle
1. **Password resets** - Guide through self-service process
2. **How-to questions** - Search knowledge base and provide instructions
3. **Feature explanations** - Explain from product documentation
4. **Bug reports** - Log the issue and provide workaround if available
5. **General feedback** - Thank customer and log feedback
6. **Account settings** - Guide through settings changes
7. **Integration setup** - Provide documentation and step-by-step guide

### When Customer is Just Venting
- If sentiment is negative but customer is asking a valid question
- Acknowledge frustration, then solve the problem
- Only escalate if they explicitly request human help or issue cannot be resolved

## Escalation Metrics

### Target Metrics
- Escalation rate: < 20% of total conversations
- False escalations: < 5%
- Average escalation response time: < 2 hours
- Customer satisfaction after escalation: > 90%

### Review Triggers
- If escalation rate > 25%, review AI training
- If false escalations > 10%, refine escalation rules
- Weekly review of escalated tickets to improve AI responses
