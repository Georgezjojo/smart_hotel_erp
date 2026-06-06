import os
import sys
import random
from datetime import date, timedelta, datetime
from decimal import Decimal
from django.utils import timezone

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# When running from the interactive shell, __file__ is not defined.
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    script_dir = os.getcwd()

# Add project root to Python path (one level up from scripts/)
project_root = os.path.abspath(os.path.join(script_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import django
django.setup()

from django.contrib.auth.hashers import make_password
from apps.accounts.models import User
from apps.hotel.models import RoomType, Room
from apps.crm.models import GuestProfile
from apps.reservations.models import Reservation
from apps.restaurant.models import MenuCategory, MenuItem, Table, Order, OrderItem
from apps.kitchen_display.models import KitchenOrder
from apps.inventory.models import Item, PurchaseOrder
from apps.accounting.models import FinancialEntry
from apps.hr.models import Employee, Attendance, Shift
from apps.notifications.models import Notification
from apps.branches.models import Branch
from apps.billing.models import Invoice, Payment
from apps.housekeeping.models import Task
from apps.operations.models import Message
from apps.advanced_features.models import DigitalKey

# ======================= HELPER FUNCTIONS =======================
def create_users():
    """Create staff and guest users with different roles."""
    users = {}
    password = 'password123'

    roles = [
        ('superadmin@example.com', 'super_admin', 'Super', 'Admin'),
        ('owner@example.com', 'owner', 'Hotel', 'Owner'),
        ('manager@example.com', 'manager', 'General', 'Manager'),
        ('reception@example.com', 'receptionist', 'Alice', 'Johnson'),
        ('accountant@example.com', 'accountant', 'Bob', 'Smith'),
        ('storemanager@example.com', 'store_manager', 'Clara', 'Doe'),
        ('chef@example.com', 'chef', 'Gordon', 'Ramsey'),
        ('waiter@example.com', 'waiter', 'James', 'Bond'),
        ('housekeep@example.com', 'housekeeping', 'Maria', 'Lopez'),
        ('security@example.com', 'security', 'Mike', 'Tyson'),
        ('nextjojo2040@gmail.com', 'guest', 'John', 'Doe'),
        ('nextjojo2041@gmail.com', 'guest', 'Jane', 'Smith'),
        ('georgezjojo04@gmail.com', 'guest', 'George', 'Zulu'),
        ('guest4@example.com', 'guest', 'Anna', 'Müller'),
        ('guest5@example.com', 'guest', 'Chen', 'Wei'),
    ]

    for email, role, first, last in roles:
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email,
                'first_name': first,
                'last_name': last,
                'role': role,
                'password': make_password(password),
                'is_active': True,
                'must_change_password': True,
            }
        )
        users[email] = user

    # ✅ SAFE admin superuser creation (will never throw duplicate error)
    admin_user, admin_created = User.objects.get_or_create(
        username='admin@example.com',
        defaults={
            'email': 'admin@example.com',
            'is_superuser': True,
            'is_staff': True,
        }
    )
    # Always ensure the role is set correctly
    admin_user.role = 'super_admin'
    if admin_created:
        admin_user.set_password('Admin123')
    else:
        # update password just in case (idempotent)
        admin_user.set_password('Admin123')
    admin_user.save()

    return users

def create_room_types():
    types = [
        ('Single Standard', Decimal('4500'), 1),
        ('Double Standard', Decimal('5500'), 2),
        ('Deluxe Panorama', Decimal('8500'), 2),
        ('Executive Suite', Decimal('12000'), 3),
        ('Presidential Suite', Decimal('20000'), 4),
    ]
    for name, rate, occ in types:
        RoomType.objects.get_or_create(name=name, defaults={'base_rate': rate, 'max_occupancy': occ})

def create_rooms():
    room_types = {rt.name: rt for rt in RoomType.objects.all()}
    rooms = []
    # Floor 1: 5 singles
    for i in range(1, 6):
        rooms.append(Room.objects.get_or_create(room_number=f'10{i}', defaults={'room_type': room_types['Single Standard'], 'floor': 1})[0])
    # Floor 2: 4 doubles + 1 deluxe
    for i in range(1, 5):
        rooms.append(Room.objects.get_or_create(room_number=f'20{i}', defaults={'room_type': room_types['Double Standard'], 'floor': 2})[0])
    rooms.append(Room.objects.get_or_create(room_number='205', defaults={'room_type': room_types['Deluxe Panorama'], 'floor': 2})[0])
    # Floor 3: 3 deluxe, 1 executive, 1 presidential
    for i in range(1, 4):
        rooms.append(Room.objects.get_or_create(room_number=f'30{i}', defaults={'room_type': room_types['Deluxe Panorama'], 'floor': 3})[0])
    rooms.append(Room.objects.get_or_create(room_number='304', defaults={'room_type': room_types['Executive Suite'], 'floor': 3})[0])
    rooms.append(Room.objects.get_or_create(room_number='305', defaults={'room_type': room_types['Presidential Suite'], 'floor': 3})[0])
    # Floor 4: maintenance room
    rooms.append(Room.objects.get_or_create(room_number='401', defaults={'room_type': room_types['Deluxe Panorama'], 'floor': 4, 'status': 'maintenance'})[0])
    return rooms

def create_guests(users):
    guests = {}
    guest_emails = ['nextjojo2040@gmail.com', 'nextjojo2041@gmail.com', 'georgezjojo04@gmail.com', 'guest4@example.com', 'guest5@example.com']
    for email in guest_emails:
        user = users[email]
        gp, _ = GuestProfile.objects.get_or_create(
            user=user,
            defaults={
                'nationality': random.choice(['Germany', 'USA', 'China', 'Kenya', 'France']),
                'passport_number': f'P{random.randint(100000, 999999)}',
                'passport_expiry': timezone.now().date() + timedelta(days=random.randint(365, 1825)),
                'tier': random.choice(['regular', 'vip', 'regular']),
                'loyalty_points': random.randint(0, 500),
            }
        )
        guests[email] = gp
    return guests

def create_reservations(users, rooms):
    guest_users = [users[e] for e in ['nextjojo2040@gmail.com', 'nextjojo2041@gmail.com', 'georgezjojo04@gmail.com', 'guest4@example.com', 'guest5@example.com']]
    today = timezone.now().date()
    reservations = []

    # Past reservation (checked out)
    r = Reservation.objects.create(
        guest=guest_users[0],
        room=rooms[0],
        check_in=today - timedelta(days=5),
        check_out=today - timedelta(days=2),
        total_amount=Decimal('22500'),
        payment_status='paid',
        status='checked_out'
    )
    reservations.append(r)

    # Current active (checked in)
    r = Reservation.objects.create(
        guest=guest_users[1],
        room=rooms[2],
        check_in=today - timedelta(days=1),
        check_out=today + timedelta(days=2),
        total_amount=Decimal('16500'),
        payment_status='partially_paid',
        status='checked_in'
    )
    reservations.append(r)

    # Arriving today
    r = Reservation.objects.create(
        guest=guest_users[2],
        room=rooms[4],
        check_in=today,
        check_out=today + timedelta(days=3),
        total_amount=Decimal('25500'),
        payment_status='unpaid',
        status='confirmed'
    )
    reservations.append(r)

    # Future
    r = Reservation.objects.create(
        guest=guest_users[3],
        room=rooms[1],
        check_in=today + timedelta(days=7),
        check_out=today + timedelta(days=10),
        total_amount=Decimal('13500'),
        payment_status='unpaid',
        status='confirmed'
    )
    reservations.append(r)

    # VIP guest in suite
    r = Reservation.objects.create(
        guest=guest_users[4],
        room=rooms[10],  # Presidential Suite
        check_in=today + timedelta(days=2),
        check_out=today + timedelta(days=5),
        total_amount=Decimal('60000'),
        payment_status='paid',
        status='confirmed'
    )
    reservations.append(r)
    return reservations

def create_restaurant_data():
    # Categories
    cat1, _ = MenuCategory.objects.get_or_create(name='Appetizers')
    cat2, _ = MenuCategory.objects.get_or_create(name='Main Course')
    cat3, _ = MenuCategory.objects.get_or_create(name='Desserts')
    cat4, _ = MenuCategory.objects.get_or_create(name='Beverages')

    # Menu items (12 items)
    items = [
        MenuItem.objects.get_or_create(name='Caesar Salad', category=cat1, price=Decimal('650'), defaults={'available': True}),
        MenuItem.objects.get_or_create(name='Bruschetta', category=cat1, price=Decimal('450'), defaults={'available': True}),
        MenuItem.objects.get_or_create(name='Grilled Salmon', category=cat2, price=Decimal('1800'), defaults={'available': True}),
        MenuItem.objects.get_or_create(name='Beef Tenderloin', category=cat2, price=Decimal('2200'), defaults={'available': True}),
        MenuItem.objects.get_or_create(name='Pasta Carbonara', category=cat2, price=Decimal('1200'), defaults={'available': True}),
        MenuItem.objects.get_or_create(name='Margherita Pizza', category=cat2, price=Decimal('950'), defaults={'available': True}),
        MenuItem.objects.get_or_create(name='Tiramisu', category=cat3, price=Decimal('700'), defaults={'available': True}),
        MenuItem.objects.get_or_create(name='Chocolate Fondant', category=cat3, price=Decimal('850'), defaults={'available': True}),
        MenuItem.objects.get_or_create(name='Espresso', category=cat4, price=Decimal('250'), defaults={'available': True}),
        MenuItem.objects.get_or_create(name='Fresh Orange Juice', category=cat4, price=Decimal('350'), defaults={'available': True}),
        MenuItem.objects.get_or_create(name='Red Wine Glass', category=cat4, price=Decimal('550'), defaults={'available': True}),
        MenuItem.objects.get_or_create(name='Mineral Water', category=cat4, price=Decimal('150'), defaults={'available': True}),
    ]

    # Tables (8)
    for i in range(1, 9):
        Table.objects.get_or_create(number=f'T{i}', defaults={'capacity': random.choice([2,2,4,4,6,8])})

def create_kitchen_orders():
    # Create a few orders for demonstration
    if KitchenOrder.objects.exists():
        return
    KitchenOrder.objects.create(
        table='T1',
        items='["Caesar Salad", "Grilled Salmon"]',
        priority=False,
        status='pending'
    )
    KitchenOrder.objects.create(
        room='Room 102',
        items='["Beef Tenderloin", "Red Wine Glass"]',
        special_instructions='Well done steak',
        priority=True,
        status='preparing'
    )
    KitchenOrder.objects.create(
        table='T5',
        items='["Pizza Margherita", "Orange Juice"]',
        status='ready'
    )

def create_inventory():
    items = [
        ('Tomatoes', 'ingredient', 50, 'kg', 10, timezone.now().date() + timedelta(days=7), 'Fresh Farms'),
        ('Olive Oil', 'ingredient', 20, 'liters', 5, None, 'OilCo'),
        ('Chicken Breast', 'ingredient', 30, 'kg', 8, timezone.now().date() + timedelta(days=3), 'Poultry Ltd'),
        ('Bed Sheets', 'cleaning', 100, 'pcs', 20, None, 'Linen Supplies'),
        ('Toilet Paper', 'cleaning', 200, 'rolls', 50, None, 'Hygiene Co'),
        ('Shampoo', 'consumables', 150, 'bottles', 30, None, 'Amenities Inc'),
        ('Wine Glass', 'beverage', 60, 'pcs', 15, None, 'Bar Ware'),
        ('Red Wine', 'beverage', 40, 'bottles', 10, None, 'Vineyard'),
        ('Detergent', 'cleaning', 25, 'liters', 5, None, 'Clean Supply'),
        ('Rice', 'ingredient', 75, 'kg', 20, timezone.now().date() + timedelta(days=30), 'Grain Corp'),
        ('Butter', 'ingredient', 15, 'kg', 5, timezone.now().date() + timedelta(days=14), 'Dairy Farm'),
    ]
    for name, cat, qty, unit, reorder, expiry, supplier in items:
        Item.objects.get_or_create(
            name=name,
            defaults={'category': cat, 'quantity': qty, 'unit': unit, 'reorder_level': reorder, 'expiry_date': expiry, 'supplier': supplier}
        )
    # Create one purchase order
    if not PurchaseOrder.objects.exists():
        item = Item.objects.first()
        PurchaseOrder.objects.create(item=item, quantity=50)

def create_financial_entries():
    today = timezone.now().date()
    entries = [
        (today - timedelta(days=5), 'Room revenue - John Doe', Decimal('22500'), 'income'),
        (today - timedelta(days=5), 'Restaurant sales', Decimal('3500'), 'income'),
        (today - timedelta(days=4), 'Electricity bill', Decimal('5000'), 'expense'),
        (today - timedelta(days=3), 'Staff salaries', Decimal('15000'), 'expense'),
        (today - timedelta(days=2), 'Room service tip', Decimal('500'), 'income'),
        (today - timedelta(days=1), 'Maintenance repair', Decimal('4000'), 'expense'),
        (today, 'Jane Smith - partial payment', Decimal('8000'), 'income'),
    ]
    for dt, desc, amt, etype in entries:
        FinancialEntry.objects.get_or_create(date=dt, description=desc, amount=amt, entry_type=etype)

def create_hr(users):
    # Create employees for staff users
    staff_roles = ['reception@example.com', 'accountant@example.com', 'storemanager@example.com', 'chef@example.com', 'waiter@example.com', 'housekeep@example.com', 'security@example.com']
    for email in staff_roles:
        user = users[email]
        Employee.objects.get_or_create(
            user=user,
            defaults={
                'employee_id': f'EMP{random.randint(100,999)}',
                'department': user.get_role_display(),
                'hire_date': timezone.now().date() - timedelta(days=random.randint(30, 365)),
                'salary': Decimal(random.randint(25000, 80000)),
            }
        )
    # Attendance (today's)
    today = timezone.now().date()
    now = timezone.now()
    for emp in Employee.objects.all():
        Attendance.objects.get_or_create(
            employee=emp,
            date=today,
            defaults={'check_in': now.replace(hour=8, minute=0, second=0, microsecond=0), 'check_out': None}
        )
    # Shift
    emp = Employee.objects.first()
    if emp:
        Shift.objects.get_or_create(employee=emp, date=today, defaults={'start_time': '08:00', 'end_time': '16:00'})

def create_notifications(users):
    if Notification.objects.exists():
        return
    for user in User.objects.filter(role__in=['receptionist', 'manager', 'guest']):
        Notification.objects.create(
            recipient=user,
            message='New reservation confirmed for ' + user.get_full_name(),
            channel='in_app'
        )

def create_branches():
    Branch.objects.get_or_create(name='Grand Horizon Nairobi', defaults={'address': 'Nairobi CBD', 'phone': '+254 700 000 001'})
    Branch.objects.get_or_create(name='Grand Horizon Mombasa', defaults={'address': 'Mombasa Beach Road', 'phone': '+254 700 000 002'})

def create_digital_keys(rooms, users):
    guest = users['nextjojo2040@gmail.com']
    room = rooms[0]
    today = timezone.now().date()
    DigitalKey.objects.get_or_create(
        user=guest,
        room=room,
        defaults={
            'qr_code_data': f'KEY-{guest.id}-{room.room_number}',
            'valid_from': today,
            'valid_to': today + timedelta(days=3),
            'is_active': True,
        }
    )

def create_messages(users):
    if Message.objects.exists():
        return
    sender = users['reception@example.com']
    Message.objects.create(sender=sender, text='Guest in Room 102 requested late checkout. Can we accommodate?')
    sender2 = users['manager@example.com']
    Message.objects.create(sender=sender2, text='Yes, the next guest arrives at 6 PM. Update the system.')

def create_housekeeping(rooms, users):
    housekeeper = users['housekeep@example.com']
    for room in rooms[:6]:  # tasks for first 6 rooms
        Task.objects.get_or_create(
            room=room,
            defaults={'assigned_to': housekeeper, 'task_type': 'cleaning', 'status': random.choice(['pending', 'in_progress', 'completed'])}
        )

def create_invoices_and_payments(reservations):
    for res in reservations:
        if res.status in ['checked_out', 'checked_in'] and not Invoice.objects.filter(reservation=res).exists():
            subtotal = res.total_amount
            tax = round(subtotal * Decimal('0.12'), 2)
            service = round(subtotal * Decimal('0.05'), 2)
            total = subtotal + tax + service
            inv = Invoice.objects.create(
                reservation=res,
                invoice_number=f'INV-{res.id:04d}',
                due_date=res.check_out,
                subtotal=subtotal,
                tax=tax,
                service_charge=service,
                total=total,
                paid=(res.payment_status == 'paid'),
                payment_method='card' if res.payment_status == 'paid' else ''
            )
            if res.payment_status == 'paid':
                Payment.objects.create(invoice=inv, amount=total, method='card', transaction_id=f'TXN{random.randint(100000,999999)}')
            elif res.payment_status == 'partially_paid':
                Payment.objects.create(invoice=inv, amount=total/2, method='mpesa', transaction_id=f'MPESA{random.randint(100000,999999)}')

# ======================= MAIN =======================
print('Seeding database...')

# 1. Users
users = create_users()
print('Users created.')

# 2. Room Types & Rooms
create_room_types()
rooms = create_rooms()
print('Rooms created.')

# 3. Guest Profiles
guests = create_guests(users)
print('Guest profiles created.')

# 4. Reservations
reservations = create_reservations(users, rooms)
print('Reservations created.')

# 5. Restaurant
create_restaurant_data()
create_kitchen_orders()
print('Restaurant data created.')

# 6. Inventory
create_inventory()
print('Inventory created.')

# 7. Accounting
create_financial_entries()
print('Financial entries created.')

# 8. HR
create_hr(users)
print('HR data created.')

# 9. Notifications
create_notifications(users)
print('Notifications sent.')

# 10. Branches
create_branches()
print('Branches created.')

# 11. Digital Keys
create_digital_keys(rooms, users)
print('Digital keys generated.')

# 12. Messages
create_messages(users)
print('Chat messages created.')

# 13. Housekeeping
create_housekeeping(rooms, users)
print('Housekeeping tasks assigned.')

# 14. Invoices & Payments
create_invoices_and_payments(reservations)
print('Invoices and payments recorded.')

print('Database seeding completed successfully!')