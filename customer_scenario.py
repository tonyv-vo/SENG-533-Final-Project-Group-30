import logging
from random import randint, choice
from locust import HttpUser, task, between

log_level = "Error"

def log_info(service, res) -> None:
    if res is None:
        if log_level == "Info": logging.info(f"info: {service}")
    elif res.ok:
        if log_level == "Info": logging.info(f"success: {service}")
    else:
        if log_level == "Info" or log_level =="Error" :logging.error(f"failure: {service}, res: {res}")

class UserBehavior(HttpUser):
    logged_in = False
    wait_time = between(5, 10)

    @task
    def visit_home(self) -> None:
        # load landing page
        res = self.client.get('/')
        log_info("vist_home", res)

    @task
    def login(self) -> None:
        # load login page
        res = self.client.get('/login')
        log_info("login_page", res)

        # login random user
        user = randint(1, 99)
        res = self.client.post("/loginAction", params={"username": user, "password": "password"})
        if res.ok: 
            self.logged_in = True
        log_info(f"user_login, user:{user}", res)

    @task(2)
    def browse(self) -> None:
        # execute browsing action randomly up to 5 times
        for _ in range(1, randint(2, 5)):
            # browses random category and page
            category_id = randint(2, 6)
            page = randint(1, 5)
            res = self.client.get("/category", params={"page": page, "category": category_id})
            log_info(f"browse category {category_id}", res)
            if not res.ok: return

            # browses random product
            product_id = randint(7, 506)
            res = self.client.get("/product", params={"id": product_id})
            log_info(f"browse product {product_id}", res)
            if not res.ok: return
            
            choice_add_to_cart = choice([True] * 20 + [False] * 80)  # 20% chance of buying, 80% chance of not buying
            if not choice_add_to_cart: return
            res = self.client.post("/cartAction", params={"addToCart": "", "productid": product_id})
            log_info(f"Add to cart {product_id}", res)

    @task
    def buy(self) -> None:
        choice_buy = choice([True, False])  # 50% chance of buying, 50% chance of not buying
        if not choice_buy: return
        if not self.logged_in: self.login()
        user_data = {
            "firstname": "Jone",
            "lastname": "Doe",
            "adress1": "Road",
            "adress2": "City",
            "cardtype": "visa",
            "cardnumber": "314159265359",
            "expirydate": "12/2030",
            "confirm": "Confirm"
        }
        res = self.client.post("/cartAction", params=user_data)
        log_info("cart checkout", res)

    @task
    def visit_profile(self) -> None:
        if not self.logged_in: self.login()
        res = self.client.get("/profile")
        log_info("visit_profile", res)

    @task
    def logout(self) -> None:
        res = self.client.post("/loginAction", params={"logout": ""})
        if res.ok: 
            self.logged_in = False
        log_info("logout", res)
