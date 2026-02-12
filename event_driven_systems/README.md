# Event-Driven Systems (EDS) - Deep Dive Learning Path

Welcome to the comprehensive guide on Event-Driven Systems! This curriculum is designed to take you from foundational concepts to advanced implementation strategies through a structured, three-tier learning path.

---

## 📚 Curriculum Roadmap

### **Tier 1: Foundations (Beginner)**
Master the fundamentals of event-driven architecture:
- **Core Definitions**: What are events, event-driven systems, and why they matter
- **Pub/Sub vs. Message Queuing**: Understanding the key communication patterns
- **Essential Terminology**: Producers, Consumers, Brokers, Topics, and Channels
- **Basic Event Flow**: How events propagate through a system
- **Simple Implementation**: Building your first event producer and consumer

### **Tier 2: Patterns & Architecture (Intermediate)**
Dive into architectural patterns and design considerations:
- **Event Sourcing**: Storing state as a sequence of events
- **CQRS (Command Query Responsibility Segregation)**: Separating reads from writes
- **Saga Pattern**: Managing distributed transactions across services
- **Delivery Guarantees**: At-least-once vs. Exactly-once vs. At-most-once
- **Event Design**: Structuring events for scalability and maintainability
- **Error Handling**: Strategies for dealing with failures in event-driven systems

### **Tier 3: Advanced Implementation & Scalability**
Master production-grade event-driven systems:
- **Backpressure Management**: Handling overwhelming event loads
- **Stream Processing**: Real-time processing with Kafka and Flink
- **Schema Registry**: Managing event schema evolution
- **Observability**: Monitoring, tracing, and debugging distributed events
- **Performance Optimization**: Partitioning, batching, and throughput tuning
- **Security**: Authentication, authorization, and encryption in event systems

---

## 🎓 Tier 1: Foundations - Interactive Lesson

### **What Are Event-Driven Systems?**

An **Event-Driven System** is an architectural pattern where the flow of the program is determined by events—significant changes in state that occur within the system or external triggers that the system must respond to.

**Why Event-Driven Systems?**

Think of event-driven systems like a newsroom:
- **Traditional Systems** are like calling each reporter individually to ask if they have news (polling)
- **Event-Driven Systems** are like reporters shouting "Breaking News!" when something happens, and only interested parties respond (reactive)

This approach offers several advantages:
- **Decoupling**: Components don't need to know about each other directly
- **Scalability**: Easy to add new consumers without changing producers
- **Responsiveness**: Systems react immediately to changes
- **Flexibility**: New functionality can be added by subscribing to existing events

---

### **Core Terminology**

Understanding these fundamental concepts is crucial:

- **Event**: A significant change in state or an occurrence in the system
  - Example: "UserRegistered", "OrderPlaced", "PaymentProcessed"
  
- **Producer (Publisher)**: The component that generates and sends events
  - Example: A registration service that emits "UserRegistered" events
  
- **Consumer (Subscriber)**: The component that receives and processes events
  - Example: An email service that listens for "UserRegistered" to send welcome emails
  
- **Broker (Message Bus)**: The intermediary that routes events from producers to consumers
  - Example: RabbitMQ, Apache Kafka, AWS SNS/SQS
  
- **Topic/Channel**: A named category or stream where events are published
  - Example: "user-events", "order-events"

---

### **Pub/Sub vs. Message Queuing**

Both are messaging patterns, but they serve different purposes:

#### **Publish/Subscribe (Pub/Sub)**
```
Producer → Topic → [Consumer 1, Consumer 2, Consumer 3, ...]
```
**Characteristics:**
- **One-to-Many**: One message reaches multiple consumers
- **Broadcasting**: All subscribers receive all messages
- **Decoupled**: Producers don't know who the consumers are
- **Use Case**: Notifications, real-time updates, event broadcasting

**Real-World Analogy**: Like a radio broadcast—one station (producer) broadcasts to many listeners (consumers).

#### **Message Queuing**
```
Producer → Queue → Consumer 1
               ↓
           (Queue waits)
               ↓
            Consumer 2 (if Consumer 1 fails)
```
**Characteristics:**
- **One-to-One**: Each message consumed by exactly one consumer
- **Load Balancing**: Messages distributed among available consumers
- **Guaranteed Processing**: Messages remain until successfully processed
- **Use Case**: Task distribution, work queues, background jobs

**Real-World Analogy**: Like a customer service queue—each customer (message) is served by one available representative (consumer).

---

### **Event Flow Visualization**

Here's an ASCII representation of a basic event-driven system:

```
┌──────────────┐
│   Producer   │  (Emits events)
│  (User API)  │
└──────┬───────┘
       │
       │ publishes "UserRegistered"
       │
       ▼
┌──────────────────────────────────┐
│         Event Broker             │
│       (Message Bus/Kafka)        │
│   Topic: "user-events"           │
└────┬─────────┬──────────┬────────┘
     │         │          │
     │         │          │
     ▼         ▼          ▼
┌─────────┐ ┌──────────┐ ┌─────────────┐
│ Email   │ │Analytics │ │Notification │  (Consumers)
│ Service │ │ Service  │ │   Service   │
└─────────┘ └──────────┘ └─────────────┘
   │            │              │
   │            │              │
   ▼            ▼              ▼
Sends        Records        Pushes
Welcome      User Stats     Mobile Alert
Email
```

**What's Happening:**
1. User API produces a "UserRegistered" event
2. Event Broker receives and stores the event
3. All subscribed consumers receive the event independently
4. Each consumer processes the event according to its responsibility
5. Failure in one consumer doesn't affect others

---

### **Simple Event Producer Implementation**

Let's build a basic event producer to see event-driven systems in action.

#### **Python Example: Simple Event Producer**

```python
import json
from datetime import datetime
from typing import Dict, Any

class EventProducer:
    """A simple event producer that publishes events."""
    
    def __init__(self, event_topic: str):
        self.event_topic = event_topic
        self.listeners = []  # In production, this would be a message broker
    
    def subscribe(self, listener):
        """Allow consumers to subscribe to events."""
        self.listeners.append(listener)
        print(f"✓ New subscriber added to {self.event_topic}")
    
    def publish_event(self, event_type: str, event_data: Dict[str, Any]):
        """Publish an event to all subscribers."""
        event = {
            "event_id": f"evt_{datetime.now().timestamp()}",
            "event_type": event_type,
            "timestamp": datetime.now().isoformat(),
            "topic": self.event_topic,
            "data": event_data
        }
        
        print(f"\n📢 Publishing event: {event_type}")
        print(f"   Event ID: {event['event_id']}")
        
        # Notify all listeners (in production, broker handles this)
        for listener in self.listeners:
            listener(event)
        
        return event


# Example Usage
def email_service_consumer(event):
    """Consumer that sends emails based on events."""
    if event['event_type'] == 'UserRegistered':
        user_email = event['data']['email']
        print(f"   ✉️  Email Service: Sending welcome email to {user_email}")

def analytics_consumer(event):
    """Consumer that tracks analytics."""
    if event['event_type'] == 'UserRegistered':
        print(f"   📊 Analytics Service: Recording new user signup")

def notification_consumer(event):
    """Consumer that sends push notifications."""
    if event['event_type'] == 'UserRegistered':
        username = event['data']['username']
        print(f"   🔔 Notification Service: Sending push notification to admins about {username}")


# Create producer and register consumers
user_events = EventProducer("user-events")
user_events.subscribe(email_service_consumer)
user_events.subscribe(analytics_consumer)
user_events.subscribe(notification_consumer)

# Simulate user registration
print("=" * 60)
print("SIMULATING USER REGISTRATION EVENT")
print("=" * 60)

user_events.publish_event(
    event_type="UserRegistered",
    event_data={
        "user_id": "12345",
        "username": "johndoe",
        "email": "john@example.com",
        "registration_date": datetime.now().isoformat()
    }
)

print("\n" + "=" * 60)
print("EVENT PROCESSING COMPLETE")
print("=" * 60)
```

**Expected Output:**
```
✓ New subscriber added to user-events
✓ New subscriber added to user-events
✓ New subscriber added to user-events
============================================================
SIMULATING USER REGISTRATION EVENT
============================================================

📢 Publishing event: UserRegistered
   Event ID: evt_1707745234.567890
   ✉️  Email Service: Sending welcome email to john@example.com
   📊 Analytics Service: Recording new user signup
   🔔 Notification Service: Sending push notification to admins about johndoe

============================================================
EVENT PROCESSING COMPLETE
============================================================
```

---

#### **JavaScript Example: Simple Event Producer**

```javascript
class EventProducer {
    constructor(eventTopic) {
        this.eventTopic = eventTopic;
        this.listeners = []; // In production, this would be a message broker
    }
    
    subscribe(listener) {
        this.listeners.push(listener);
        console.log(`✓ New subscriber added to ${this.eventTopic}`);
    }
    
    publishEvent(eventType, eventData) {
        const event = {
            event_id: `evt_${Date.now()}`,
            event_type: eventType,
            timestamp: new Date().toISOString(),
            topic: this.eventTopic,
            data: eventData
        };
        
        console.log(`\n📢 Publishing event: ${eventType}`);
        console.log(`   Event ID: ${event.event_id}`);
        
        // Notify all listeners
        this.listeners.forEach(listener => listener(event));
        
        return event;
    }
}

// Example Usage
const emailServiceConsumer = (event) => {
    if (event.event_type === 'UserRegistered') {
        const userEmail = event.data.email;
        console.log(`   ✉️  Email Service: Sending welcome email to ${userEmail}`);
    }
};

const analyticsConsumer = (event) => {
    if (event.event_type === 'UserRegistered') {
        console.log(`   📊 Analytics Service: Recording new user signup`);
    }
};

const notificationConsumer = (event) => {
    if (event.event_type === 'UserRegistered') {
        const username = event.data.username;
        console.log(`   🔔 Notification Service: Sending push notification to admins about ${username}`);
    }
};

// Create producer and register consumers
const userEvents = new EventProducer('user-events');
userEvents.subscribe(emailServiceConsumer);
userEvents.subscribe(analyticsConsumer);
userEvents.subscribe(notificationConsumer);

// Simulate user registration
console.log('='.repeat(60));
console.log('SIMULATING USER REGISTRATION EVENT');
console.log('='.repeat(60));

userEvents.publishEvent('UserRegistered', {
    user_id: '12345',
    username: 'johndoe',
    email: 'john@example.com',
    registration_date: new Date().toISOString()
});

console.log('\n' + '='.repeat(60));
console.log('EVENT PROCESSING COMPLETE');
console.log('='.repeat(60));
```

---

### **Key Takeaways from Tier 1**

✅ **Events represent significant state changes** in your system

✅ **Producers and Consumers are decoupled** through brokers/message buses

✅ **Pub/Sub broadcasts events** to multiple consumers; **Message Queues distribute work** among consumers

✅ **Event-driven systems are reactive and scalable**, responding to changes as they happen

✅ **Understanding the "why"**: Event-driven systems enable loosely coupled, scalable architectures that can grow organically

---

## 🤔 Knowledge Check

Test your understanding of Event-Driven Systems fundamentals:

### **Question 1: Conceptual Understanding**
You're building an e-commerce platform. When a customer places an order, the system needs to:
- Update inventory
- Charge the payment method
- Send confirmation email
- Notify the shipping department

Would you use **Pub/Sub** or **Message Queuing** for this scenario? Why?

<details>
<summary>💡 Click for Answer & Explanation</summary>

**Answer: Pub/Sub**

**Why:**
- The "OrderPlaced" event needs to reach **multiple independent services** simultaneously
- Each service (inventory, payment, email, shipping) has a different responsibility
- Failure in one service (e.g., email) shouldn't prevent others from processing
- All services need to react to the same event

**Message Queuing would be wrong here** because:
- Only ONE consumer would process the order
- Other services wouldn't be notified
- You'd need complex coordination between services

**Implementation approach:**
```
OrderService → Publish "OrderPlaced" event
                      ↓
          [Inventory, Payment, Email, Shipping]
           (All receive and process independently)
```
</details>

---

### **Question 2: Architecture Decision**
Your team is building a background job processing system where tasks must be processed exactly once (e.g., processing payments). Multiple worker instances are running for scalability. Which pattern is more appropriate?

A) Pub/Sub with multiple subscribers  
B) Message Queue with competing consumers  
C) Both would work equally well  

<details>
<summary>💡 Click for Answer & Explanation</summary>

**Answer: B) Message Queue with competing consumers**

**Why:**
- **Exactly-once processing requirement**: Each payment task should be handled by only ONE worker
- **Message Queues ensure**: Each message is delivered to exactly one consumer
- **Competing consumers pattern**: Multiple workers compete for tasks from the same queue
- **Built-in load balancing**: Work is automatically distributed

**Why Pub/Sub would be wrong:**
- ALL subscribers would receive the event
- Payment would be processed multiple times
- Would cause duplicate charges (disaster!)

**Correct Architecture:**
```
TaskProducer → Queue → [Worker1, Worker2, Worker3]
                       (One worker picks up each task)
```
</details>

---

### **Question 3: Real-World Application**
In the code examples above, we simulated a message broker using a simple list of listeners. In a production environment with microservices deployed across multiple servers, what would be the main limitations of this approach?

<details>
<summary>💡 Click for Answer & Explanation</summary>

**Main Limitations:**

1. **No Network Communication**
   - In-memory listeners only work within a single process
   - Can't communicate across different servers/containers
   - Microservices need network-based message brokers

2. **No Persistence**
   - Events are lost if the process crashes
   - No guarantee of delivery
   - Can't replay events or recover from failures

3. **No Scalability**
   - Can't add consumers dynamically from other servers
   - Limited by single machine's resources
   - No horizontal scaling

4. **No Delivery Guarantees**
   - No at-least-once or exactly-once semantics
   - If a consumer fails, event is lost
   - No retry mechanisms

5. **No Message Ordering or Partitioning**
   - Can't guarantee event processing order
   - Can't partition events by key (e.g., by user_id)

**Production Solution:**
Use a proper message broker like:
- **Apache Kafka**: High-throughput, distributed streaming
- **RabbitMQ**: Feature-rich message queuing
- **AWS SNS/SQS**: Managed cloud messaging
- **Google Pub/Sub**: Scalable, serverless messaging
- **Azure Service Bus**: Enterprise messaging

These provide:
- Network communication
- Persistence and durability
- Delivery guarantees
- Scalability and fault tolerance
- Monitoring and observability
</details>

---

## 🎯 What's Next?

Congratulations on completing **Tier 1: Foundations**! You now understand:
- What event-driven systems are and why they matter
- The difference between Pub/Sub and Message Queuing
- Core terminology and basic event flow
- How to implement a simple event producer

**Ready to advance?** In **Tier 2: Patterns & Architecture**, we'll explore:
- Event Sourcing and CQRS patterns
- The Saga Pattern for distributed transactions
- Delivery guarantees and their trade-offs
- Best practices for event design and error handling

**Stay tuned for Tier 2 content!**

---

## 📚 Additional Resources

- **Books**: "Building Event-Driven Microservices" by Adam Bellemare
- **Documentation**: Apache Kafka, RabbitMQ official docs
- **Articles**: Martin Fowler's blog on Event-Driven Architecture
- **Videos**: Conference talks on microservices and event streaming

---

*This curriculum is part of a comprehensive learning repository. Each tier builds upon the previous one, ensuring a solid foundation for mastering event-driven systems.*
