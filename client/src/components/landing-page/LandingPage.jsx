import NavigationBar from "./NavigationBar"
import './landing-page.css'
import GroceryCard from "../GroceryCard"


function LandingPage() {
    return (
        <main>
            <NavigationBar />
            <img className="background-image" src="./src/img/landing-page-background.jpg" alt="" />
            <div class="featured-items">
                <h1>Featured Items</h1>
                <div>
                    <GroceryCard price="8.99" title="Kirkland Large Farm Eggs, 12 count" weight="1.25" imageURL="./src/img/food/eggs.png" />
                    <GroceryCard price = "13.99" title="Loaf of Nature's Whole Weat Bread" weight="1.25" imageURL="./src/img/food/bread.jpg" />
                    <GroceryCard price = "11.99" title = "Daidy Free Plain Yogurt" weight="2.00" imageURL="./src/img/food/yogurt.png" />
                    <GroceryCard price ="5.99" title="Lunchly Fiesta Nachoes With Prime" weight="2.50" imageURL="./src/img/food/lunchly.png" />
                    <GroceryCard price ="2.99" title ="Signature Select Baby-Cut Carrots" weight="0.50" imageURL="./src/img/food/baby-carrots.png" />
                    <GroceryCard price ="7.99" title="Pavesi Gocciole Chocolate Chip Cookies" weight="1.00" imageURL="./src/img/food/cookies.png" />
                </div>
            </div>
            
        </main>
    )
}

export default LandingPage