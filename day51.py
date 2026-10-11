"""
Food Delivery Platform Mini Backend System (System Design)
=========================================================
Phase: System Design

Description:
A startup is launching a food delivery platform experiencing rapid order growth. 
This script implements a mini backend simulation handling core entities (Users, 
Restaurants, Orders, Delivery Agents), an event-driven order lifecycle state machine, 
and real-time delivery tracking.

Real-World Impact:
- Hyper-local Logistics: Powering real-time matching engines like Swiggy, Zomato, and Uber Eats.
- High-Throughput Microservices: Managing concurrent state changes, inventory locks, and dispatch queues.
"""

from enum import Enum
import time
import random

class OrderStatus(Enum):
    PLACED = "PLACED"
    ACCEPTED = "ACCEPTED"
    PREPARING = "PREPARING"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class User:
    """Represents a customer using the platform."""
    def __init__(self, user_id: int, name: str, address: str):
        self.user_id = user_id
        self.name = name
        self.address = address


class Restaurant:
    """Represents a restaurant partner with a menu and active order queue."""
    def __init__(self, rest_id: int, name: str, menu: dict[str, float]):
        self.rest_id = rest_id
        self.name = name
        self.menu = menu  # Item name -> Price
        self.is_open = True

    def accept_order(self, order_id: int) -> bool:
        """Simulates restaurant confirming order availability and capacity."""
        if self.is_open:
            print(f"[RESTAURANT] {self.name} accepted Order #{order_id}.")
            return True
        print(f"[RESTAURANT] {self.name} is currently closed. Rejecting Order #{order_id}.")
        return False


class DeliveryAgent:
    """Represents a delivery partner handling pickups and drop-offs."""
    def __init__(self, agent_id: int, name: str):
        self.agent_id = agent_id
        self.name = name
        self.is_available = True
        self.current_location = "Hub Alpha"

    def assign_order(self, order_id: int):
        self.is_available = False
        print(f"[DISPATCH] Agent {self.name} assigned to Order #{order_id}.")

    def complete_delivery(self, order_id: int):
        self.is_available = True
        print(f"[DISPATCH] Agent {self.name} successfully delivered Order #{order_id}.")


class Order:
    """Tracks individual order state, items, and billing."""
    def __init__(self, order_id: int, user: User, restaurant: Restaurant, items: list[str]):
        self.order_id = order_id
        self.user = user
        self.restaurant = restaurant
        self.items = items
        self.status = OrderStatus.PLACED
        self.total_amount = sum(restaurant.menu.get(item, 0.0) for item in items)
        self.assigned_agent: DeliveryAgent | None = None

    def update_status(self, new_status: OrderStatus):
        self.status = new_status
        print(f"[ORDER STATE] Order #{self.order_id} status updated -> {self.status.value}")


class DeliveryPlatformBackend:
    """Orchestrates the entire food delivery ecosystem workflow."""
    def __init__(self):
        self.orders = {}
        self.available_agents = [
            DeliveryAgent(101, "Alex Rider"),
            DeliveryAgent(102, "Sam Wilson")
        ]
        self._order_counter = 1000

    def place_order(self, user: User, restaurant: Restaurant, items: list[str]) -> Order:
        """Handles user checkout and order initialization."""
        order_id = self._order_counter
        self._order_counter += 1
        
        new_order = Order(order_id, user, restaurant, items)
        self.orders[order_id] = new_order
        
        print(f"\n[CHECKOUT] Order #{order_id} placed by {user.name} at {restaurant.name}. Total: ${new_order.total_amount:.2f}")
        return new_order

    def process_order_lifecycle(self, order: Order):
        """Simulates the end-to-end execution flow of an order."""
        # Step 1: Restaurant Acceptance
        if order.restaurant.accept_order(order.order_id):
            order.update_status(OrderStatus.ACCEPTED)
        else:
            order.update_status(OrderStatus.CANCELLED)
            return

        # Step 2: Kitchen Preparation
        order.update_status(OrderStatus.PREPARING)
        time.sleep(0.5) # Simulating kitchen prep time
        print(f"[KITCHEN] {order.restaurant.name} finished preparing items: {', '.join(order.items)}")

        # Step 3: Assign Delivery Agent
        agent = self._find_available_agent()
        if agent:
            order.assigned_agent = agent
            agent.assign_order(order.order_id)
            order.update_status(OrderStatus.OUT_FOR_DELIVERY)
            
            # Step 4: Tracking & Delivery Completion
            time.sleep(0.5)
            agent.complete_delivery(order.order_id)
            order.update_status(OrderStatus.DELIVERED)
        else:
            print(f"[ERROR] No delivery agents available for Order #{order.order_id}!")

    def _find_available_agent(self) -> DeliveryAgent | None:
        for agent in self.available_agents:
            if agent.is_available:
                return agent
        return None


# --- Architecture & System Design Notes ---
"""
--- ARCHITECTURE NOTES (System Design Documentation) ---
1. Scalability & Concurrency:
   - In a production microservice environment, the database layer (PostgreSQL/MySQL) 
   would utilize row-level locking or optimistic concurrency control on the `orders` 
   table to prevent race conditions during restaurant order confirmation.
   - Redis could be used for caching restaurant menus and real-time delivery agent 
   location coordinates (geospatial indexing via Redis GEO).

2. Event-Driven Order Pipeline:
   - Order status transitions (Placed -> Accepted -> Preparing -> Out for Delivery -> Delivered) 
   should be pushed to a message broker (e.g., Apache Kafka or RabbitMQ) to decouple 
   the checkout service, kitchen display system (KDS), and notification service.

3. Fault Tolerance:
   - If a delivery agent drops offline, circuit breakers and fallback timeout mechanisms 
   should automatically re-queue the order for redispatch to nearby active drivers.
"""


# --- Execution and Simulation ---
if __name__ == "__main__":
    print("=== FOOD DELIVERY PLATFORM BACKEND SIMULATOR ===")
    
    # Initialize Backend Platform
    backend = DeliveryPlatformBackend()
    
    # Setup Test Entities
    customer = User(user_id=1, name="Bruce Wayne", address="100 Mountain Drive")
    
    restaurant_menu = {
        "Margherita Pizza": 14.99,
        "Garlic Bread": 6.50,
        "Sparkling Water": 3.00
    }
    gotham_pizzeria = Restaurant(rest_id=501, name="Gotham Pizzeria", menu=restaurant_menu)
    
    # Simulate Order Placement & Lifecycle
    cart_items = ["Margherita Pizza", "Garlic Bread"]
    customer_order = backend.place_order(customer, gotham_pizzeria, cart_items)
    
    # Run Order Pipeline
    backend.process_order_lifecycle(customer_order)
