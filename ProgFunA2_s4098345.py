# Sohan Shirish Wasker S4098345
# Highest level atempted: HD Level
# Problems and requirements not met: Parts:3,5,7-product and order.
from datetime import datetime
class Guest:
    def __init__(self,ID,name,reward):
        self.ID=ID
        self.name=name
        self.reward=int(reward)
        self.reward_rate=1.00 
        self.redeem_rate=0.01  

    def get_ID(self):   
        return self.ID  

    def get_name(self):
        return self.name

    def get_reward_rate(self):
        return self.reward_rate

    def get_redeem_rate(self):
        return self.redeem_rate

    def get_reward(self,total_cost):
        return int(round(total_cost*self.reward_rate))

    def update_reward(self,value):
        self.reward=int(round(float(self.reward)))+value

    def set_reward_rate(self,rate):
        self.reward_rate=rate/100

    def set_redeem_rate(self,rate):
        self.redeem_rate=rate/100

    def display_info(self):
        print(f"ID:{self.ID},Name:{self.name},Reward Rate:{self.reward_rate},Reward:{self.reward},Redeem Rate:{self.redeem_rate}")

class Product:
    def __init__(self,ID,name,price):
        self.ID=ID
        self.name=name
        self.price=price

    def get_ID(self):
        return self.ID

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def display_info(self):
        pass  

class ApartmentUnit(Product):
    def __init__(self,ID,name,price,cap):
        super().__init__(ID,name,price)
        self.cap=cap

    def get_cap(self):
        return self.cap

    def display_info(self):
        print(f"ID:{self.ID},Name:{self.name},Price:{self.price}(Rate per night),Capacity:{self.cap}")
    
class SupplementaryItem(Product):
    def __init__(self,ID,name,price):
        super().__init__(ID,name,price)

    def display_info(self):
        print(f"{'ID':<10}{'Name':<10}{'Price':<10}")
        print(f"{self.ID:<10}{self.name:<30}{self.price}")

class Order:
    def __init__(self,guest,product,quantity,bk_time,ttcost=None,rw=None):
        self.guest=guest
        self.product=product
        self.quantity=quantity
        self.bk_time=bk_time
        self.ttcost=ttcost if ttcost is not None else self.compute_cost()[2]
        self.rw=rw if rw is not None else self.compute_cost()[3]
    

    def compute_cost(self,rwpts=0):
        og_cost=0
        for pro,quan in zip(self.product,self.quantity): 
            og_cost+=(pro.get_price()*quan)

        discount=rwpts*self.guest.get_redeem_rate()
        final_total_cost=og_cost-discount
        earned_reward=self.guest.get_reward(og_cost)

        return og_cost,discount,final_total_cost,earned_reward
    
    def display_info(self):
        print(f"{self.guest.get_name():<10}",end="")
        components=[]
        for prd,qnt in zip(self.product,self.quantity):
            components.append(f"{qnt}x{prd.get_ID()}")

        print(f"{', '.join(components):<40}{round(float(self.ttcost),2):<10}{self.rw:<10}{self.bk_time}") 
    
class Bundle(Product):
    def __init__(self,ID,name,products):
        super().__init__(ID,name,0) 
        self.products=products

    def calculate_price(self):
        total_price=sum([product.get_price() for product in self.products])
        bundle_price=total_price*0.80  
        self.price=bundle_price  
        return bundle_price

    def display_info(self):
        print(f"{self.ID:<10}{self.name:<50}",end="")
        components=[]
        product_quantity={}
        
        for product in self.products:
            if product in product_quantity:
                product_quantity[product]+=1
            else:
                product_quantity[product]=1

        for product,quantity in product_quantity.items():
            if quantity>1:
                components.append(f"{quantity}x{product.get_ID()}")
            else:
                components.append(product.get_ID())
        print(f"{', '.join(components):<40}{round(self.price,2)}") 
              
class Records:
    def __init__(self):
        self.guest_list=[]
        self.product_list=[]
        self.history={}

    def read_order(self,file_name):
        with open(file_name,'r') as f:
            for line in f:
                order_data=line.strip().split(',')
                guest,products,ttcost,rw,bk_time=order_data[0],order_data[1:-3],order_data[-1],order_data[-3],order_data[-2]
                guest_obj=self.find_guest(guest.strip())
                qty=[]
                itms=[]
                for item in products:
                    quantity,pr=item.split('x')
                    itms.append(self.find_product(pr.strip()))
                    qty.append(quantity)

                order=Order(guest_obj,itms,qty,ttcost,rw,bk_time)
                guest_obj.reward=rw
                if guest in self.history:
                    self.history[guest].append(order)
                else:
                    self.history[guest]=[order]    

    def read_guests(self,file_name):
        with open(file_name,'r') as f:
            for line in f:
                guest_data=line.strip().split(',')
                guest=Guest(int(guest_data[0]),guest_data[1],int(guest_data[3]))
                guest.set_reward_rate(float(guest_data[2]))
                guest.set_redeem_rate(float(guest_data[4]))
                self.guest_list.append(guest)

    def read_products(self,file_name):
        with open(file_name,'r') as f:
            for line in f:
                product_data=line.strip().split(',')
                if product_data[0].startswith('U'):
                    product=ApartmentUnit(product_data[0],product_data[1],float(product_data[2]),int(product_data[3]))
                elif product_data[0].startswith('SI'):
                    product=SupplementaryItem(product_data[0],product_data[1],float(product_data[2]))
                elif product_data[0].startswith('B'):  
                    product_ids=product_data[2:-1] 
                    bundle_products=[self.find_product(p_id.strip()) for p_id in product_ids]
                    product=Bundle(product_data[0],product_data[1],bundle_products)
                    product.calculate_price() 
                self.product_list.append(product)

    def find_guest(self,search_value):
        for guest in self.guest_list:
            if guest.get_ID()==search_value or guest.get_name().strip()==search_value:
                return guest
        return None

    def find_product(self,search_value):
        for product in self.product_list:
            if product.get_ID()==search_value or product.get_name().strip()==search_value:
                return product
        return None

    def list_history(self,name=None):
        if name not in self.history and name is not None:
            print("Guest doesnt exist")
            return
        if not name:
            print(f"{'Name':<10}{'Products':<40}{'Cost':<10}{'Rewards':<10}{'Date'}")
            for guest_name, orders in self.history.items():
                for order in orders:
                    order.display_info()
        else:
            for guest_name, orders in self.history.items():
                if guest_name==name:
                    print(f"This is the booking and order history for {guest_name}:")
                    print(f"{'Name':<10}{'Products':<40}{'Cost':<10}{'Rewards':<10}{'Date'}")
                    for order in orders:
                        order.display_info()

    def list_guests(self):
        for guest in self.guest_list:
            guest.display_info()

    def list_products(self,product_type=None):
        for product in self.product_list:
            if product_type=="apartment" and isinstance(product,ApartmentUnit):
                product.display_info()
            elif product_type=="supplementary" and isinstance(product,SupplementaryItem):
                product.display_info()
            elif isinstance(product,Bundle):
                if product_type=="bundle" or product_type is None:
                    product.display_info()

class Operations:
    def __init__(self,records):
        self.records=records

    def display_menu(self):
        print("1. Make a booking")
        print("2. Display existing guests")
        print("3. Display existing apartment units")
        print("4. Display existing supplementary items")
        print("5. Display existing bundles")
        print("6. Add/update information of apartment units")
        print("7. Add/update information of supplimentary items")
        print("8. Add/update information of bundles")
        print("9. Adjust the reward rate of all guests")
        print("10. Adjust the redeem rate of all guests")
        print("11. Display all orders")
        print("12. Display a guest's order history")

        print("0. Exit")

    def start(self):
        try:
            self.records.read_guests('guests.csv')
            self.records.read_products('products.csv')
            self.records.read_order('orders.csv')
        except FileNotFoundError as e:
            print(f"Error:{e}")
            return

        while True:
            self.display_menu()
            choice=input("Enter choice: ")

            if choice=='1':
                self.make_booking()
            elif choice=='2':
                self.records.list_guests()
            elif choice=='3':
                self.records.list_products("apartment")
            elif choice=='4':
                print(f"{'ID':<10}{'Name':<30}{'Price'}")
                self.records.list_products("supplementary")
            elif choice=='5':
                print(f"{'ID':<10}{'Name':<50}{'Components':<40}{'Price'}")
                self.records.list_products("bundle")
            elif choice=='6':
                self.apartment()
            elif choice=='7':
                self.supplement()
            elif choice=='8':
                self.bundle()
            elif choice=='9':
                rate=input("Enter new reward rate")
                self.rewardrate(rate)
            elif choice=='10':
                rate=input("Enter new redeem rate")
                self.reedemrate(rate)
            elif choice=='11':
                self.records.list_history()
            elif choice=='12':
                g_name=input('Enter guest to search record')
                self.records.list_history(g_name)
            elif choice=='0':
                print("Exiting...")
                break

    def make_booking(self):
        # Collecting the guest's information
        while True:
            guest_name=input("Enter guest name: ")
            if guest_name.isalpha():
                break
            else:
                print("Please enter valid name")
           
        guest=self.records.find_guest(guest_name)

        if guest is None:
            print("New guest, creating record...")
            guest_id=len(self.records.guest_list)+1
            reward=0    
            guest=Guest(guest_id,guest_name,int(reward))
            self.records.guest_list.append(guest)
        else:
            print(f"Guest {guest_name} found with {guest.reward} reward points.")

        num_guests=int(input("Enter number of guests: "))

        # Collecting the booking details
        while True:
            ptype=input("Do you wish to buy bundle or not (yes/no)")
            if ptype in ["no","n"]:
                apt_id=input("Enter apartment ID: ")
                apartment=self.records.find_product(apt_id)
                if apartment is None or not isinstance(apartment,ApartmentUnit):
                    print("Invalid apartment ID. Please try again")
                else:
                    bundle=None
                    break
            elif ptype in ["yes","y"]:
                bundle_id=input("Enter bundle ID: ")
                bundle=self.records.find_product(bundle_id)
                if bundle is None or not isinstance(bundle,Bundle):
                    print("Invalid bundle ID. Please try again")
                else:
                    print(f"{'ID':<10}{'Name':<50}{'Components':<40}{'Price'}")
                    bundle.display_info()
                    break
            else:
                print("Enter valid choice")
                ptype=input("Do you wish to buy bundle or not (yes/no)")

        while True:
            ch_in=input("\nEnter check-in date (DD/MM/YYYY): ")
            ch_out=input("Enter check-out date (DD/MM/YYYY): ")
            try:
                ch_in=datetime.strptime(ch_in,"%d/%m/%Y")
                ch_out=datetime.strptime(ch_out,"%d/%m/%Y")
                bk_date=datetime.now() 
                if ch_in<bk_date:
                    print("Check-in date cannot be earlier than the booking date.")
                    continue
                if ch_out<bk_date:
                    print("Check-out date cannot be earlier than the booking date.")
                    continue
                if ch_out<=ch_in:
                    print("Check-out date must be after the check-in date.")
                    continue
                break
            except ValueError as e:
                print("Invalid date format:",e)
        
        bk_date=datetime.now().strftime("%d/%m/%Y %H:%M")
        staylen=(ch_out-ch_in).days
        ch_in=datetime.strftime(ch_in,"%d/%m/%Y")
        ch_out=datetime.strftime(ch_out,"%d/%m/%Y")
        print("Length of stay:",staylen)
        print("Booking date:",bk_date)

        items=[]
        qunt=[]
        if ptype in ["no","n"]:
            items.append(apartment)
            qunt.append(staylen)
            bundle_cost=None
        else:
            for product in bundle.products:
                if product in items:
                    index=items.index(product)
                    qunt[index]+=1
                else:
                    items.append(product)
                    qunt.append(1)
            apartment=items[0] 
            bundle_cost=bundle.get_price()*staylen
            qunt=[q*staylen for q in qunt]
        

        # Checking if any extra beds are required
        extra_beds_needed=max(0,(num_guests-apartment.get_cap()+1)//2)
        
        # Adding extra beds due to requirement 
        if extra_beds_needed>0:
            print(f"Extra beds needed:{extra_beds_needed}")
            
            # Get the supplementary item for the extra bed
            extra_bed=self.records.find_product("SI6")  # Assuming SI6 is the extra bed ID
            
            if extra_bed is None:
                print("Error: Extra bed item not found in the system.")
                return
            
            # Calculating quantity of extra beds based on the length of stay
            extra_bed_quantity=extra_beds_needed*staylen
            print(f"Extra bed quantity required:{extra_bed_quantity}")
            if bundle_cost is not None:
                bundle_cost+=extra_bed.get_price()*extra_bed_quantity
            # Adding the extra bed with its quantity to the booking
            # guest.update_reward(staylen*apartment.get_price())  # Rewards being updated based on stay
            
            items=[apartment,extra_bed]  # List of products in the booking
            qunt=[1,extra_bed_quantity]  # Quantities corresponding to the products
               
        
        while True:
            moresup=input("Do you want suplimentary items?(yes/no)")
            if moresup.lower().strip() in ["no","n"]:
                break
            elif moresup.lower().strip() in ["yes","y"]: 
                
                sup_item_id=input("Enter supplementary item ID: ")
                sup_item=self.records.find_product(sup_item_id)
                if not sup_item:
                    print("Enter valid supplimentary item number")
                    continue
                while True:
                    try:
                        sup_qty=int(input("Enter supplementary item quantity: "))
                        if not sup_qty>0:
                            print("Invalid quantity. Please try again")
                        else:
                            if sup_item_id=="SI1":
                                if sup_qty<=staylen:
                                    print(f"You need car parking for atleast {staylen} nights")
                                    sup_qty=staylen
                                    print(f"Car park quantity updated to: {staylen}")
                                    
                            if bundle_cost is not None:
                                bundle_cost+=sup_item.get_price()*sup_qty
                            qunt.append(sup_qty)
                            items.append(sup_item)
                            break
                    except ValueError:
                        print("Enter integer value")
                moresup=input("Do you want more suplimentary items?(yes/no)")
            else:
                print("Enter valid choice")
        # Calculating the costs
        apt_cost=apartment.get_price()*staylen
        sup_cost=0
        print(items)
        print(qunt)
        for item,quant in zip(items[1:],qunt[1:]):
            sup_cost+=(item.get_price()*quant)
        total_cost=apt_cost+sup_cost

        if bundle is not None:
            existing_reward=guest.reward
            cost=Order(guest,items,qunt,bk_date,bundle_cost,int(guest.get_reward(total_cost)))
            og_cost,discount,final_total_cost,earned_reward=total_cost,0,bundle_cost,int(guest.get_reward(total_cost))
            guest.update_reward(earned_reward)
            if guest in self.records.history:
                self.records.history[guest].append(cost)
            else:
                self.records.history[guest]=[cost]
        else:
            while True:
                # Providing an option to use reward points for discount
                print(f"Total cost before discount: ${total_cost}")
                redeem_points=input(f"Do you want to use {guest.reward} reward points for a discount? (yes/no): ").lower()
                if redeem_points in ["yes","y"]:
                    print('redeem part : ',items)           
                    cost=Order(guest,items,qunt,bk_date)
                    og_cost,discount,final_total_cost,earned_reward=cost.compute_cost(float(guest.reward))
                    existing_reward=guest.reward
                    guest.reward=0
                    guest.update_reward(earned_reward)
                    if guest in self.records.history:
                        self.records.history[guest].append(cost)
                    else:
                        self.records.history[guest]=[cost]
                    print(f"Discount applied: ${discount}")
                    break
                elif redeem_points in ["no","n"]:
                    cost=Order(guest,items,qunt,bk_date)
                    og_cost,discount,final_total_cost,earned_reward=total_cost,0,total_cost,round(total_cost)
                    existing_reward=guest.reward
                    guest.update_reward(earned_reward)
                    if guest in self.records.history:
                        self.records.history[guest].append(cost)
                    else:
                        self.records.history[guest]=[cost]
                    break
                else:
                    print("Enter a valid choice")
                    redeem_points=input(f"Do you want to use {guest.reward} reward points for a discount? (yes/no): ").lower()
 
        # Displaying the receipt
        print()
        print("="*75)
        print(f"Guest name: {guest_name}")
        print(f"Number of guests: {num_guests}")
        print(f"Apartment name: {apartment.get_name()}")
        print(f"Apartment rate: ${apartment.get_price()} (AUD) per night")
        print(f"Check-in date: {ch_in}")
        print(f"Check-out date: {ch_out}")
        print(f"Length of stay: {staylen} night(s)")
        print(f"Booking date: {bk_date}")
        print(f"\nSub-total: ${apt_cost}")
        print("-"*75)
        print("Supplementary items:")
        print(f'{"ID":<10}{"Name":<30}{"Quantity":<10}{"Unit Price $":<20}{"Cost $":<10}')
        for item,quant in zip(items[1:],qunt[1:]):
            print(f"{item.get_ID():<10}{item.get_name():<30}{quant:<10}{item.get_price():<20}{item.get_price()*quant}")

        print(f"Sub-total: ${sup_cost}")
        print("-------------------------------------------------------")
        print(f"Total cost: ${og_cost} (AUD)")
        print(f"Reward points to redeem: {existing_reward}")
        print(f"Discount based on points: ${round(discount)} (AUD)")
        print(f"Final total cost: ${final_total_cost:.2f} (AUD)")
        print(f"Earned reward points: {int(earned_reward)}")
        print("\nThank you for your booking!\nWe hope you have an enjoyable stay.")
        print("="*75)

        # print(self.records.history)
        order_line=f"{guest.get_name().strip()}, "
        components=[]
        for prd,qnt in zip(items,qunt):
            components.append(f"{qnt}x{prd.get_ID()}")

        order_line+=f"{', '.join(components)}, {round(final_total_cost,2)}, {earned_reward}, {bk_date}\n"

        with open('orders.csv','a') as file:
            file.write(order_line)

        guest_line=f"{guest.get_ID()}, {guest.get_name().strip()}, {guest.get_reward_rate()}, {guest.reward}, {guest.get_redeem_rate()}\n"
        with open("guests.csv","r") as file:
            lines=file.readlines()
        flag=False
        with open("guests.csv","w") as file:
            for line in lines:
                gname=line.split(",")[1].strip()
                if guest_name==gname:
                    flag=True
                    file.write(guest_line)
                else:
                    file.write(line)
        if flag==False:
            with open("guests.csv","a") as file:
                file.write(guest_line)


    def apartment(self):
        print("\nAdd/update information of apartment units")
        apt_id=input("Enter apartment details in format: apt_id,rate,capacity ")
        # Checking for correct format and validating the apartment id
        format=apt_id.split(',')
        if len(format)!=4:
            print("Please enter in correct format")
            return
        apt_id,name,rate,cap=format
        
        if not apt_id.startswith('U'):
            print("Apartment id incorrect")
            return
        
        digi=apt_id[1:]
        if not digi:
            print("Apartment id incorrect")
            return
        
        count=0
        while count<len(digi) and digi[count].isdigit():
            count+=1
        
        if count>0 and count<len(digi) and digi[count:].isalpha():
            apartment=self.records.find_product(apt_id)
            if apartment:
                apartment.price=rate
                apartment.cap=cap
            else:
                apartment=ApartmentUnit(apt_id,name,rate,cap)
                self.records.product_list.append(apartment)
            print("Apartment unit upated")    
            return
        else:
            print("Apartment ID incorrect")
            return
    
    def supplement(self):
        print("\nAdd/update information of supplementary items")
        while True:
            # Checking for correct format and validating the supplementary items
            sup=input("Enter supplementary item details in format: item_id name price,item_id name price and so on : ")
            itemdat=sup.split(',')
            itemline=[]
            print(itemdat)
            itemid=[]
            price=[]
            name=[]
            valid=True
            for i in itemdat:
                format=i.split()
                print(format)
                item,nm,pr=format
                itemline.append(f'{item},{nm},{pr}')
                itemid.append(item)
                name.append(nm)
                price.append(pr)
                if float(pr)<0:
                    valid=False
                    break
            
            if(valid==False):
                continue
            for itm,nm,pr in zip(itemid,name,price):
                item=self.records.find_product(itm)
                if item:
                    item.price=pr
                else:
                    item=SupplementaryItem(itm,nm,pr)
                    self.records.product_list.append(item)
                    print(item)
            print("Supplementary item upated")
            return
        
    def bundle(self):
        print("\nAdd/update information of bundles")
        bundle_id=input("Enter bundle details in format: bundle_id,name,products,price ")
        # Checking for correct format and validating the bundle id
        format=bundle_id.split(',')
        bundle_id,name,products,price=format[0],format[1],format[2:-1],format[-1]
        
        if not bundle_id.startswith('B'):
            print("Bundle ID incorrect")
            return
        bundle=self.records.find_product(bundle_id)
        
        pr_list=[]
        for itm in products:
            item=self.records.find_product(itm.strip())
            pr_list.append(item)
                
        if bundle:
            bundle.name=name
            bundle.products=pr_list
            bundle.price=float(price)
        else:
            bundle=Bundle(bundle_id,name,pr_list)
            bundle.price=float(price)
            self.records.product_list.append(bundle)
        print("Bundle upated")
        return
    
    def rewardrate(self,rate):
        for guest in self.records.guest_list:
            guest.set_reward_rate(float(rate))
    
    def redeemrate(self,rate):
        for guest in self.records.guest_list:
            guest.set_redeem_rate(float(rate))

        
records=Records()
operations=Operations(records)
operations.start()


''' Reflection:
    In this assesment I learnt about 1.Implementation of OOP's concepts 
                                     2.File handling
                                     3.Solving logical problems'''
                                     